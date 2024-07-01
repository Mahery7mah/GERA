from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from django.shortcuts import render
from .utils import encrypt_id, decrypt_id
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from app_GERA.models import Ville, Quartier, Adresse, Evenement, Lieu, CategorieEvenement, TypeEvenement, PosteDuPersonnel, Membre, TypeMembre, Article, InscriptionEvenement, Notification, Interlocuteur
from .forms import VilleForm, QuartierForm, LieuForm, EvenementForm, CategorieEvenementForm, TypeEvenementForm, PosteDuPersonnelForm, MailForm, EvenementInvitationForm, EvenementAudienceForm, EvenementAPublierForm, ArticleForm, InterlocuteurForm, PersonnelForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Max
from django.db import connection
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import os
import random
from django.db.models import Count
from django.db import connection
from django.db.models.functions import ExtractMonth
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models.functions import Lower
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
import base64
from io import BytesIO
import itertools
from collections import defaultdict
from django.db.models import Count
from django.db.models.functions import TruncDate
from wkhtmltopdf.views import PDFTemplateResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views import View
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User



SECRET_KEY = settings.SECRET_KEY

progress_tracker = {}  # Dictionnaire pour stocker la progression


@login_required
def dashboard(request):
    # Total new members
    total_new_members = Membre.objects.count()
    
    # Statistics for events
    total_events = Evenement.objects.count()
    total_invitation_events = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation').count()
    upcoming_invitation_events = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation', Date_Debut_E__gte=timezone.now()).count()
    past_invitation_events = total_invitation_events - upcoming_invitation_events

    total_audience_events = Evenement.objects.filter(ID_Categorie_E__isnull=True).count()
    completed_audience_events = Evenement.objects.filter(ID_Categorie_E__isnull=True, Est_Fait=True).count()
    audience_completion_rate = (completed_audience_events / total_audience_events * 100) if total_audience_events > 0 else 0

    total_apublier_events = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier').count()
    upcoming_apublier_events = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier', Date_Debut_E__gte=timezone.now()).count()
    published_apublier_events = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier', Publie_E=True).count()

    # Member statistics
    total_clients = Membre.objects.filter(ID_TypeMembre__Nom_Type_M='membre_simple').count()
    total_personnel = Membre.objects.filter(ID_TypeMembre__Nom_Type_M='membre_personnel').count()
    total_published_events = Evenement.objects.filter(Publie_E=True).count()

    # Calculate the participation rates
    total_client_inscriptions = InscriptionEvenement.objects.filter(ID_Membre__ID_TypeMembre__Nom_Type_M='membre_simple').count()
    total_personnel_inscriptions = InscriptionEvenement.objects.filter(ID_Membre__ID_TypeMembre__Nom_Type_M='membre_personnel').count()

    client_participation_rate = (total_client_inscriptions / total_clients * 100) if total_clients > 0 else 0
    personnel_participation_rate = (total_personnel_inscriptions / total_personnel * 100) if total_personnel > 0 else 0

    # Ensure rates are between 0 and 100
    client_participation_rate = min(max(client_participation_rate, 0), 100)
    personnel_participation_rate = min(max(personnel_participation_rate, 0), 100)
    audience_completion_rate = min(max(audience_completion_rate, 0), 100)

    # Replace commas with dots for correct CSS width values
    client_participation_rate = str(client_participation_rate).replace(',', '.')
    personnel_participation_rate = str(personnel_participation_rate).replace(',', '.')
    audience_completion_rate = str(audience_completion_rate).replace(',', '.')

    # Article statistics
    total_articles = Article.objects.count()
    total_published_articles = Article.objects.filter(Publie_A=True).count()

    # Event frequency by month
    event_frequency_by_month = Evenement.objects.annotate(month=ExtractMonth('Date_Debut_E')).values('month').annotate(event_count=Count('ID_Evenement')).order_by('month')

    data = {
        'labels': [item['month'] for item in event_frequency_by_month],
        'data': [item['event_count'] for item in event_frequency_by_month],
    }

    # Number of upcoming events (consider filtering by publication status if applicable)
    upcoming_events = Evenement.objects.filter(Date_Debut_E__gte=timezone.now()).order_by('Date_Debut_E')
    upcoming_event_counts = {
        'invitation': upcoming_events.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation').count(),
        'audience': upcoming_events.filter(ID_Categorie_E__isnull=True).count(),
        'apublier': upcoming_events.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier').count(),
    }

    context = {
        'total_new_members': total_new_members,
        'total_events': total_events,
        'total_invitation_events': total_invitation_events,
        'upcoming_invitation_events': upcoming_invitation_events,
        'past_invitation_events': past_invitation_events,
        'total_audience_events': total_audience_events,
        'audience_completion_rate': audience_completion_rate,
        'upcoming_event_counts': upcoming_event_counts,
        'total_apublier_events': total_apublier_events,
        'upcoming_apublier_events': upcoming_apublier_events,
        'published_apublier_events': published_apublier_events,
        'total_clients': total_clients,
        'client_participation_rate': client_participation_rate,
        'total_personnel': total_personnel,
        'personnel_participation_rate': personnel_participation_rate,
        'total_published_events': total_published_events,
        'total_articles': total_articles,
        'total_published_articles': total_published_articles,
        'data_json': json.dumps(data),
    }

    return render(request, 'dashboard/dashboard.html', context)

# ville :
@login_required
def ville_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_Ville')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_Ville']  
    default_sort_field = 'Nom_Ville'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        Ville_list = Ville.objects.filter(Q(Nom_Ville__icontains=search_query)).order_by(order_by_field)
    else:
        Ville_list = Ville.objects.all().order_by(order_by_field)

    paginator = Paginator(Ville_list, 10)
    page = request.GET.get('page')
    villes = paginator.get_page(page)

    subtitle = 'Liste des villes'

    return render(request, 'ville/Ville_list.html', {'villes': villes, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def ville_detail(request, encrypted_id):
    ID_Ville = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_Ville is not None:
        ville = get_object_or_404(Ville, pk=ID_Ville)
        subtitle = 'Détail de la ville'
        return render(request, 'ville/ville_detail.html', {'ville': ville, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')
    
@login_required
def ville_create(request):
    if request.method == 'POST':
        form = VilleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ville ajouté avec succès.')
            return redirect('ville_list_back')
    else:
        form = VilleForm()
    subtitle = 'Ajouter des ville'
    return render(request, 'ville/ville_form.html', {'form': form, 'subtitle': subtitle})

# ville_update 
@login_required
def ville_update(request, encrypted_id):
    try:
        ville_id = decrypt_id(encrypted_id, SECRET_KEY)
        ville = get_object_or_404(Ville, pk=ville_id)

        if request.method == 'POST':
            form = VilleForm(request.POST, instance=ville)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ville modifié avec succès.')
                return redirect('ville_list_back')
        else:
            form = VilleForm(instance=ville)
        subtitle = 'Modifier des ville'
        return render(request, 'ville/ville_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in ville_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du ville.')
        return render(request, 'erreur/404.html')

# ville_delete 
@login_required
def ville_delete(request, encrypted_id):
    ville_id = decrypt_id(encrypted_id, SECRET_KEY)

    if ville_id is not None:
        ville = get_object_or_404(Ville, pk=ville_id)
        ville.delete()
        messages.success(request, 'Ville supprimée avec succès.')
        return redirect('ville_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du ville.')
        return render(request, 'erreur/404.html')

#Quartier
@login_required
def quartier_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_Quartier')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_Quartier'] 
    default_sort_field = 'Nom_Quartier'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        quartier_list = Quartier.objects.filter(Q(Nom_Quartier__icontains=search_query)).order_by(order_by_field)
    else:
        quartier_list = Quartier.objects.all().order_by(order_by_field)

    paginator = Paginator(quartier_list, 10)
    page = request.GET.get('page')
    quartiers = paginator.get_page(page)

    subtitle = 'Liste des quartiers'

    return render(request, 'quartiers/quartier_list.html', {'quartiers': quartiers, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def quartier_detail(request, encrypted_id):
    quartier_id = decrypt_id(encrypted_id, SECRET_KEY)

    if quartier_id is not None:
        quartier = get_object_or_404(Quartier, pk=quartier_id)
        subtitle = 'Détail de la quartier'
        return render(request, 'quartiers/quartier_detail.html', {'quartier': quartier, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def quartier_create(request):
    if request.method == 'POST':
        form = QuartierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'quartier ajoutée avec succès.')
            return redirect('quartier_list')
    else:
        form = QuartierForm()
    subtitle = 'Ajouter une quartier'
    return render(request, 'quartiers/quartier_form.html', {'form': form, 'subtitle': subtitle})

@login_required
def quartier_update(request, encrypted_id):
    try:
        quartier_id = decrypt_id(encrypted_id, SECRET_KEY)
        quartier = get_object_or_404(Quartier, pk=quartier_id)

        if request.method == 'POST':
            form = QuartierForm(request.POST, instance=quartier)
            if form.is_valid():
                form.save()
                messages.success(request, 'quartier modifiée avec succès.')
                return redirect('quartier_list')
        else:
            form = QuartierForm(instance=quartier)
        subtitle = 'Modifier une quartier'
        return render(request, 'quartiers/quartier_form.html', {'form': form, 'subtitle': subtitle})
    except Exception as e:
        print(f"Error in quartier_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification de la quartier.')
        return render(request, 'erreur/404.html')

@login_required
def quartier_delete(request, encrypted_id):
    quartier_id = decrypt_id(encrypted_id, SECRET_KEY)

    if quartier_id is not None:
        quartier = get_object_or_404(Quartier, pk=quartier_id)
        quartier.delete()
        messages.success(request, 'quartier supprimée avec succès.')
        return redirect('quartier_list')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression de la quartier.')
        return render(request, 'erreur/404.html')
    
    
    
#Lieux
@login_required
def lieu_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Lieu')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Lieu', 'Capacite_Lieu']  # Add 'Capacite_Lieu' for sorting by capacity
    default_sort_field = 'Lieu'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        lieu_list = Lieu.objects.filter(Q(Lieu__icontains=search_query)).order_by(order_by_field)
    else:
        lieu_list = Lieu.objects.all().order_by(order_by_field)

    paginator = Paginator(lieu_list, 10)
    page = request.GET.get('page')
    lieux = paginator.get_page(page)

    subtitle = 'Liste des lieux'

    return render(request, 'lieu/lieu_list.html', {'lieux': lieux, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def lieu_detail(request, encrypted_id):
    lieu_id = decrypt_id(encrypted_id, SECRET_KEY)

    if lieu_id is not None:
        lieu = get_object_or_404(Lieu, pk=lieu_id)
        subtitle = 'Détail du lieu'
        return render(request, 'lieu/lieu_detail.html', {'lieu': lieu, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')
    
@login_required
def lieu_create(request):
    if request.method == 'POST':
        form = LieuForm(request.POST)
        if form.is_valid():
            quartier_id = form.cleaned_data['ID_Quartier'].ID_Quartier
            rue = form.cleaned_data['Rue']
            adresse = Adresse.objects.create(Rue=rue, ID_Quartier_id=quartier_id)
            lieu = form.save(commit=False)
            lieu.ID_Adresse = adresse
            lieu.save()
            messages.success(request, 'Lieu ajouté avec succès.')
            return redirect('lieu_list')
    else:
        form = LieuForm()
    subtitle = 'Ajouter un lieu'
    return render(request, 'lieu/lieu_form.html', {'form': form, 'subtitle': subtitle})

@login_required
def lieu_update(request, encrypted_id):
    try:
        lieu_id = decrypt_id(encrypted_id, SECRET_KEY)
        lieu = get_object_or_404(Lieu, pk=lieu_id)

        if request.method == 'POST':
            form = LieuForm(request.POST, instance=lieu)
            if form.is_valid():
                adresse = lieu.ID_Adresse
                adresse.ID_Quartier_id = form.cleaned_data['ID_Quartier'].ID_Quartier
                adresse.Rue = form.cleaned_data['Rue']
                adresse.save()
                lieu = form.save(commit=False)
                lieu.ID_Adresse = adresse
                lieu.save()
                messages.success(request, 'Lieu modifié avec succès.')
                return redirect('lieu_list')
        else:
            form = LieuForm(instance=lieu, initial={'Rue': lieu.ID_Adresse.Rue, 'ID_Quartier': lieu.ID_Adresse.ID_Quartier})
        subtitle = 'Modifier un lieu'
        return render(request, 'lieu/lieu_form.html', {'form': form, 'subtitle': subtitle})
    except Exception as e:
        print(f"Error in lieu_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du lieu.')
        return render(request, 'erreur/404.html')

@login_required
def lieu_delete(request, encrypted_id):
    lieu_id = decrypt_id(encrypted_id, SECRET_KEY)

    if lieu_id is not None:
        lieu = get_object_or_404(Lieu, pk=lieu_id)
        lieu.delete()
        messages.success(request, 'Lieu supprimé avec succès.')
        return redirect('lieu_list')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du lieu.')
        return render(request, 'erreur/404.html')



#Evenement
@login_required
def evenement_list(request):
    subtitle = 'Liste des événements'

    # Récupérer la catégorie sélectionnée (par défaut Invitation)
    category = request.GET.get('category', 'invitation')

    # Filtrer les événements en fonction de la catégorie
    if category == 'invitation':
        evenement_list = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation')
        fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E']
    elif category == 'audience':
        evenement_list = Evenement.objects.filter(ID_Categorie_E__isnull=True)
        fields = ['Num_Audience', 'Titre_E', 'Description_E', 'Date_Arrive_E', 'ID_Interlocuteur']
    elif category == 'apublier':
        evenement_list = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier')
        fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E', 'ID_Interlocuteur', 'Image_E', 'Publie_E']
    else:
        evenement_list = Evenement.objects.all()
        fields = ['Titre_E', 'Description_E', 'Date_Arrive_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E']

    # Appliquer la recherche et le tri
    search_query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by', 'Titre_E')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = fields  
    default_sort_field = 'Titre_E'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        # Filtrer les événements en fonction de la requête de recherche
        evenement_list = evenement_list.filter(
            Q(Titre_E__icontains=search_query) |
            Q(Description_E__icontains=search_query)
        ).distinct()

    if start_date and end_date:
        # Convertir les dates en objets datetime
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # Filtrer les événements entre les dates spécifiées
        evenement_list = evenement_list.filter(Date_Arrive_E__range=[start_date, end_date])

    elif start_date:
        # Filtrer les événements pour une seule date précise
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        evenement_list = evenement_list.filter(Date_Arrive_E=start_date)

    else:
        # Vérifier si la catégorie est valide
        valid_categories = ['invitation', 'audience', 'apublier']
        if category not in valid_categories:
            return HttpResponseBadRequest("Catégorie d'événements invalide.")

    # Pas de recherche effectuée, afficher simplement la liste des événements
    if category == 'audience':
        evenement_list = evenement_list.order_by('Num_Audience', order_by_field)
    else:
        evenement_list = evenement_list.order_by(order_by_field)

    # Paginer les résultats
    paginator = Paginator(evenement_list, 10)
    page = request.GET.get('page')
    evenements = paginator.get_page(page)

    return render(request, 'evenement/evenement_list.html', {'evenements': evenements, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'start_date': start_date, 'end_date': end_date, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle, 'category': category})

@login_required
def evenement_publier_list(request):
    subtitle = 'Liste de publication des événements'
    evenement_list = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier')
    fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E', 'ID_Interlocuteur', 'Image_E', 'Publie_E']
    
    # Appliquer la recherche et le tri
    search_query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by', 'Date_Debut_E')
    direction = request.GET.get('direction', 'desc')  # Modifier la direction par défaut à 'desc'

    valid_sort_fields = fields  
    default_sort_field = 'Date_Debut_E'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'desc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        # Filtrer les événements en fonction de la requête de recherche
        evenement_list = evenement_list.filter(
            Q(Titre_E__icontains=search_query) |
            Q(Description_E__icontains=search_query)
        ).distinct()

    if start_date and end_date:
        # Convertir les dates en objets datetime
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # Filtrer les événements entre les dates spécifiées
        evenement_list = evenement_list.filter(Date_Debut_E__range=[start_date, end_date])

    elif start_date:
        # Filtrer les événements pour une seule date précise
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        evenement_list = evenement_list.filter(Date_Debut_E=start_date)

    # Pas de recherche effectuée, afficher simplement la liste des événements
    evenement_list = evenement_list.order_by(order_by_field)

    # Paginer les résultats
    paginator = Paginator(evenement_list, 5)
    page = request.GET.get('page')
    evenements = paginator.get_page(page)

    return render(request, 'evenement/evenement_publier_list.html', {'evenements': evenements, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'start_date': start_date, 'end_date': end_date, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def evenement_detail(request, encrypted_id):
    ID_Evenement = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_Evenement is not None:
        evenement = get_object_or_404(Evenement, pk=ID_Evenement)
        subtitle = 'Détail de l\'événement'
        return render(request, 'evenement/evenement_detail.html', {'evenement': evenement, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def evenement_create(request):

    subtitle = 'Ajouter un événement'
    return render(request, 'evenement/evenement_selection.html', {'subtitle': subtitle})

@login_required
def administration_generale(request):

    subtitle = 'Administration générale'
    return render(request, 'administration/administration_generale.html', {'subtitle': subtitle})

@login_required
def evenement_update(request, encrypted_id):
    try:
        evenement_id = decrypt_id(encrypted_id, SECRET_KEY)
        evenement = get_object_or_404(Evenement, pk=evenement_id)

        if request.method == 'POST':
            form = get_update_form_for_event(request, evenement)(request.POST, instance=evenement)
            if form.is_valid():
                evenement = form.save(commit=False)
                if 'Image_E' in request.FILES:
                    image = request.FILES['Image_E']
                    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', image.name)
                    with open(image_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    evenement.Image_E = f'img/{image.name}'
                evenement = form.save()
                messages.success(request, 'Événement modifié avec succès.')
                return redirect('evenement_list')
        else:
            form = get_update_form_for_event(request, evenement)(instance=evenement)
        subtitle = 'Modifier un événement'
        return render(request, 'evenement/evenement_form.html', {'form': form, 'subtitle': subtitle})
    except Exception as e:
        print(f"Error in evenement_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification de l\'événement.')
        return render(request, 'erreur/404.html')


@login_required
def evenement_publie_update(request, encrypted_id):
    try:
        evenement_id = decrypt_id(encrypted_id, SECRET_KEY)
        evenement = get_object_or_404(Evenement, pk=evenement_id)

        if request.method == 'POST':
            form = get_update_form_for_event(request, evenement)(request.POST, instance=evenement)
            if form.is_valid():
                evenement = form.save(commit=False)
                if 'Image_E' in request.FILES:
                    image = request.FILES['Image_E']
                    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', image.name)
                    with open(image_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    evenement.Image_E = f'img/{image.name}'
                evenement = form.save()
                messages.success(request, 'Événement modifié avec succès.')
                return redirect('evenement_publier_list')
        else:
            form = get_update_form_for_event(request, evenement)(instance=evenement)
        subtitle = 'Modifier un événement'
        return render(request, 'evenement/evenement_form.html', {'form': form, 'subtitle': subtitle})
    except Exception as e:
        print(f"Error in evenement_publie_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification de l\'événement.')
        return render(request, 'erreur/404.html')

def get_update_form_for_event(request, evenement):
    if evenement.ID_Categorie_E:
        if evenement.ID_Categorie_E.ID_Type_E.Nom_Type_E == 'Invitation':
            return EvenementInvitationForm
        elif evenement.ID_Categorie_E.ID_Type_E.Nom_Type_E == 'Apublier':
            return EvenementAPublierForm
    else:
        return EvenementAudienceForm



@login_required
def evenement_delete(request, encrypted_id):
    evenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if evenement_id is not None:
        evenement = get_object_or_404(Evenement, pk=evenement_id)
        evenement.delete()
        messages.success(request, 'Événement supprimé avec succès.')
        return redirect('evenement_list')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression de l\'événement.')
        return render(request, 'erreur/404.html')

@csrf_exempt
def mark_event_done(request):
    if request.method == 'POST':
        event_id = request.POST.get('id_evenement')
        try:
            event = Evenement.objects.get(ID_Evenement=event_id)
            event.Est_Fait = True
            event.save()
            return JsonResponse({'success': True})
        except Evenement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Evenement not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
    
@login_required
def evenement_invitation_create(request):
    if request.method == 'POST':
        form = EvenementInvitationForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.save()
            messages.success(request, 'Événement d\'invitation ajouté avec succès.')
            return HttpResponseRedirect(reverse('evenement_list') + '?category=invitation')
    else:
        form = EvenementInvitationForm()
    subtitle = 'Enregistrer une invitation'
    return render(request, 'evenement/evenement_form.html', {'form': form, 'subtitle': subtitle})

@login_required
def evenement_audience_create(request):
    if request.method == 'POST':
        form = EvenementAudienceForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.save()
            messages.success(request, 'Événement audience ajouté avec succès.')
            return HttpResponseRedirect(reverse('evenement_list') + '?category=audience')
    else:
        form = EvenementAudienceForm()
    subtitle = 'Enregistrer une audience'
    return render(request, 'evenement/evenement_form.html', {'form': form, 'subtitle': subtitle})

@login_required
def evenement_a_publier_create(request):
    if request.method == 'POST':
        form = EvenementAPublierForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)
            if 'Image_E' in request.FILES:
                image = request.FILES['Image_E']
                image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                evenement.Image_E = f'img/{image.name}'
            evenement.save()
            messages.success(request, 'Événement ajouté avec succès.')
            return redirect('evenement_publier_list')
    else:
        form = EvenementAPublierForm()
    subtitle = 'Ajouter un événement à publier'
    return render(request, 'evenement/evenement_form.html', {'form': form, 'subtitle': subtitle})

@xframe_options_exempt
@login_required
def export_pdf(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')

    valid_categories = ['invitation', 'audience']
    if category not in valid_categories:
        return HttpResponseBadRequest("Catégorie d'événements invalide.")

    if category == 'invitation':
        evenement_list = Evenement.objects.filter(
            ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation',
            Date_Arrive_E__range=[start_date, end_date]
        )
    elif category == 'audience':
        evenement_list = Evenement.objects.filter(
            ID_Categorie_E__isnull=True,
            Date_Arrive_E__range=[start_date, end_date]
        )

    evenement_list = evenement_list.annotate(date_arrive_trunc=TruncDate('Date_Arrive_E')).values('date_arrive_trunc').annotate(count=Count('ID_Evenement')).order_by('date_arrive_trunc')

    current_date = timezone.now()
    context = {
        'evenement_list': evenement_list,
        'current_date': current_date,
        'category': category,
    }

    # Récupérer tous les événements pour chaque date d'arrivée
    for group in evenement_list:
        group['evenement_list'] = Evenement.objects.filter(
            Date_Arrive_E=group['date_arrive_trunc']
        )

    # Chemin de l'image dans le dossier static
    image_path = 'gera_back/static/img/logo_mesup1.png'
    # Lire les données binaires de l'image
    with default_storage.open(image_path, 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode('utf-8')

    # Ajouter logo_data au contexte
    context['logo_data'] = logo_data
    
    response = PDFTemplateResponse(
        request=request,
        template='evenement/export_pdf_template.html',
        context=context,
        cmd_options={
            'encoding': 'utf-8',
        }
    )

    return response


@xframe_options_exempt
@login_required
def export_pdf_upcoming_invitation(request):
    current_date = timezone.now().date()
    evenement_list = Evenement.objects.filter(
        ID_Categorie_E__ID_Type_E__Nom_Type_E='Invitation',
        Date_Debut_E__gt=current_date
    ).annotate(date_debut_trunc=TruncDate('Date_Debut_E')).values('date_debut_trunc').annotate(count=Count('ID_Evenement')).order_by('date_debut_trunc')

    context = {
        'evenement_list': evenement_list,
        'current_date': current_date,
        'category': 'invitation',
    }

    for group in evenement_list:
        group['evenement_list'] = Evenement.objects.filter(
            Date_Debut_E=group['date_debut_trunc']
        )

    # Chemin de l'image dans le dossier static
    image_path = 'gera_back/static/img/logo_mesup1.png'
    # Lire les données binaires de l'image
    with default_storage.open(image_path, 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode('utf-8')

    # Ajouter logo_data au contexte
    context['logo_data'] = logo_data

    response = PDFTemplateResponse(
        request=request,
        template='evenement/evenement_pdf.html',
        context=context,
        cmd_options={
            'encoding': 'utf-8',
        }
    )

    return response    

@xframe_options_exempt
@csrf_exempt
@login_required
def export_pdf_selected_events(request):
    if request.method == 'POST':
        selected_event_ids = json.loads(request.POST.get('selected_events', '[]'))
    elif request.method == 'GET':
        selected_event_ids = json.loads(request.GET.get('selected_events', '[]'))
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
    if not selected_event_ids:
        return HttpResponseBadRequest("Veuillez sélectionner des événements.")
    
    category = request.POST.get('category') if request.method == 'POST' else request.GET.get('category')

    # Logs for debugging
    print(f"Selected Event IDs: {selected_event_ids}")
    print(f"Category: {category}")

    evenement_list = Evenement.objects.filter(ID_Evenement__in=selected_event_ids)
    valid_categories = ['invitation', 'audience']
    if category not in valid_categories:
        return HttpResponseBadRequest("Catégorie d'événements invalide.")

    evenement_list = evenement_list.annotate(date_arrive_trunc=TruncDate('Date_Arrive_E')).values('date_arrive_trunc').annotate(count=Count('ID_Evenement')).order_by('date_arrive_trunc')

    current_date = timezone.now()
    context = {
        'evenement_list': evenement_list,
        'current_date': current_date,
        'category': category,
    }

    # Récupérer tous les événements pour chaque date d'arrivée
    for group in evenement_list:
        group['evenement_list'] = Evenement.objects.filter(
            Date_Arrive_E=group['date_arrive_trunc']
        )

    # Chemin de l'image dans le dossier static
    image_path = 'gera_back/static/img/logo_mesup1.png'
    with default_storage.open(image_path, 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode('utf-8')

    context['logo_data'] = logo_data

    response = PDFTemplateResponse(
        request=request,
        template='evenement/export_pdf_template.html',
        context=context,
        cmd_options={
            'encoding': 'utf-8',
        }
    )

    return response

@login_required
def evenement_sans_article_list(request):
    subtitle = 'Liste des événements sans article'

    evenement_list = Evenement.objects.filter(article__isnull=True, ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier',
)
    fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E', 'ID_Interlocuteur', 'Image_E', 'Publie_E']

    # Appliquer la recherche et le tri
    search_query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by', 'Titre_E')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = fields  
    default_sort_field = 'Titre_E'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        # Filtrer les événements en fonction de la requête de recherche
        evenement_list = evenement_list.filter(
            Q(Titre_E__icontains=search_query) |
            Q(Description_E__icontains=search_query)
        ).distinct()

    if start_date and end_date:
        # Convertir les dates en objets datetime
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # Filtrer les événements entre les dates spécifiées
        evenement_list = evenement_list.filter(Date_Debut_E__range=[start_date, end_date])

    elif start_date:
        # Filtrer les événements pour une seule date précise
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        evenement_list = evenement_list.filter(Date_Debut_E=start_date)

    # Pas de recherche effectuée, afficher simplement la liste des événements
    evenement_list = evenement_list.order_by(order_by_field)

    # Paginer les résultats
    paginator = Paginator(evenement_list, 5)
    page = request.GET.get('page')
    evenements = paginator.get_page(page)

    return render(request, 'evenement/evenement_sans_article_list.html', {'evenements': evenements, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'start_date': start_date, 'end_date': end_date, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})


#Interlocuteur professionnel : 

# interlocuteur :
@login_required
def interlocuteur_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_I')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_I', 'Prenom_I', 'Description_I', 'Mail_I', 'Tel_I']  
    default_sort_field = 'Nom_I'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        Interlocuteur_list = Interlocuteur.objects.filter(Q(Nom_Interlocuteur__icontains=search_query)).order_by(order_by_field)
    else:
        Interlocuteur_list = Interlocuteur.objects.all().order_by(order_by_field)

    paginator = Paginator(Interlocuteur_list, 10)
    page = request.GET.get('page')
    interlocuteurs = paginator.get_page(page)

    subtitle = 'Liste des interlocuteurs'

    return render(request, 'interlocuteur/Interlocuteur_list.html', {'interlocuteurs': interlocuteurs, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def interlocuteur_detail(request, encrypted_id):
    ID_Interlocuteur = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_Interlocuteur is not None:
        interlocuteur = get_object_or_404(Interlocuteur, pk=ID_Interlocuteur)
        subtitle = 'Détail de la interlocuteur'
        return render(request, 'interlocuteur/interlocuteur_detail.html', {'interlocuteur': interlocuteur, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')
    
@login_required
def interlocuteur_create(request):
    if request.method == 'POST':
        form = InterlocuteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interlocuteur ajouté avec succès.')
            return redirect('interlocuteur_list_back')
    else:
        form = InterlocuteurForm()
    subtitle = 'Ajouter des interlocuteur'
    return render(request, 'interlocuteur/interlocuteur_form.html', {'form': form, 'subtitle': subtitle})

# interlocuteur_update 
@login_required
def interlocuteur_update(request, encrypted_id):
    try:
        interlocuteur_id = decrypt_id(encrypted_id, SECRET_KEY)
        interlocuteur = get_object_or_404(Interlocuteur, pk=interlocuteur_id)

        if request.method == 'POST':
            form = InterlocuteurForm(request.POST, instance=interlocuteur)
            if form.is_valid():
                form.save()
                messages.success(request, 'Interlocuteur modifié avec succès.')
                return redirect('interlocuteur_list_back')
        else:
            form = InterlocuteurForm(instance=interlocuteur)
        subtitle = 'Modifier des interlocuteur'
        return render(request, 'interlocuteur/interlocuteur_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in interlocuteur_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du interlocuteur.')
        return render(request, 'erreur/404.html')

# interlocuteur_delete 
@login_required
def interlocuteur_delete(request, encrypted_id):
    interlocuteur_id = decrypt_id(encrypted_id, SECRET_KEY)

    if interlocuteur_id is not None:
        interlocuteur = get_object_or_404(Interlocuteur, pk=interlocuteur_id)
        interlocuteur.delete()
        messages.success(request, 'Interlocuteur supprimée avec succès.')
        return redirect('interlocuteur_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du interlocuteur.')
        return render(request, 'erreur/404.html')


# categorieEvenement :
@login_required
def categorieEvenement_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Categorie_E')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Categorie_E']  
    default_sort_field = 'Categorie_E'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        CategorieEvenement_list = CategorieEvenement.objects.filter(Q(Categorie_E__icontains=search_query)).order_by(order_by_field)
    else:
        CategorieEvenement_list = CategorieEvenement.objects.all().order_by(order_by_field)

    paginator = Paginator(CategorieEvenement_list, 10)
    page = request.GET.get('page')
    categorieEvenements = paginator.get_page(page)

    subtitle = 'Liste des categorieEvenements'

    return render(request, 'categorieEvenement/CategorieEvenement_list.html', {'categorieEvenements': categorieEvenements, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def categorieEvenement_detail(request, encrypted_id):
    categorieEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if categorieEvenement_id is not None:
        categorieEvenement = get_object_or_404(CategorieEvenement, pk=categorieEvenement_id)
        subtitle = 'Détail de la categorieEvenement'
        return render(request, 'categorieEvenement/categorieEvenement_detail.html', {'categorieEvenement': categorieEvenement, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def categorieEvenement_create(request):
    if request.method == 'POST':
        form = CategorieEvenementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'CategorieEvenement ajouté avec succès.')
            return redirect('categorieEvenement_list_back')
    else:
        form = CategorieEvenementForm()
    subtitle = 'Ajouter des categorieEvenement'
    return render(request, 'categorieEvenement/categorieEvenement_form.html', {'form': form, 'subtitle': subtitle})

# categorieEvenement_update 
@login_required
def categorieEvenement_update(request, encrypted_id):
    try:
        categorieEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)
        categorieEvenement = get_object_or_404(CategorieEvenement, pk=categorieEvenement_id)

        if request.method == 'POST':
            form = CategorieEvenementForm(request.POST, instance=categorieEvenement)
            if form.is_valid():
                form.save()
                messages.success(request, 'CategorieEvenement modifié avec succès.')
                return redirect('categorieEvenement_list_back')
        else:
            form = CategorieEvenementForm(instance=categorieEvenement)
        subtitle = 'Modifier des categorieEvenement'
        return render(request, 'categorieEvenement/categorieEvenement_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in categorieEvenement_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du categorieEvenement.')
        return render(request, 'erreur/404.html')

# categorieEvenement_delete
@login_required
def categorieEvenement_delete(request, encrypted_id):
    categorieEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if categorieEvenement_id is not None:
        categorieEvenement = get_object_or_404(CategorieEvenement, pk=categorieEvenement_id)
        categorieEvenement.delete()
        messages.success(request, 'CategorieEvenement supprimée avec succès.')
        return redirect('categorieEvenement_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du categorieEvenement.')
        return render(request, 'erreur/404.html')
    
#TypeMembre 
@login_required
def typeEvenement_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_Type_E')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_Type_E']  
    default_sort_field = 'Nom_Type_E'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        TypeEvenement_list = TypeEvenement.objects.filter(Q(Nom_Type_E__icontains=search_query)).order_by(order_by_field)
    else:
        TypeEvenement_list = TypeEvenement.objects.all().order_by(order_by_field)

    paginator = Paginator(TypeEvenement_list, 10)
    page = request.GET.get('page')
    typeEvenements = paginator.get_page(page)

    subtitle = 'Liste des typeEvenements'

    return render(request, 'typeEvenement/TypeEvenement_list.html', {'typeEvenements': typeEvenements, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def typeEvenement_detail(request, encrypted_id):
    typeEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if typeEvenement_id is not None:
        typeEvenement = get_object_or_404(TypeEvenement, pk=typeEvenement_id)
        subtitle = 'Détail de la typeEvenement'
        return render(request, 'typeEvenement/typeEvenement_detail.html', {'typeEvenement': typeEvenement, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def typeEvenement_create(request):
    if request.method == 'POST':
        form = TypeEvenementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'TypeEvenement ajouté avec succès.')
            return redirect('typeEvenement_list_back')
    else:
        form = TypeEvenementForm()
    subtitle = 'Ajouter des typeEvenement'
    return render(request, 'typeEvenement/typeEvenement_form.html', {'form': form, 'subtitle': subtitle})

# typeEvenement_update 
@login_required
def typeEvenement_update(request, encrypted_id):
    try:
        typeEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)
        typeEvenement = get_object_or_404(TypeEvenement, pk=typeEvenement_id)

        if request.method == 'POST':
            form = TypeEvenementForm(request.POST, instance=typeEvenement)
            if form.is_valid():
                form.save()
                messages.success(request, 'TypeEvenement modifié avec succès.')
                return redirect('typeEvenement_list_back')
        else:
            form = TypeEvenementForm(instance=typeEvenement)
        subtitle = 'Modifier des typeEvenement'
        return render(request, 'typeEvenement/typeEvenement_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in typeEvenement_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du typeEvenement.')
        return render(request, 'erreur/404.html')

# typeEvenement_delete
@login_required
def typeEvenement_delete(request, encrypted_id):
    typeEvenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if typeEvenement_id is not None:
        typeEvenement = get_object_or_404(TypeEvenement, pk=typeEvenement_id)
        typeEvenement.delete()
        messages.success(request, 'TypeEvenement supprimée avec succès.')
        return redirect('typeEvenement_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du typeEvenement.')
        return render(request, 'erreur/404.html')


@login_required
def personnel_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_M')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_M']
    default_sort_field = 'Nom_M'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        personnel_list = Membre.objects.filter(Q(Nom_M__icontains=search_query), ID_TypeMembre__Nom_Type_M='membre_personnel').order_by(order_by_field)
    else:
        personnel_list = Membre.objects.filter(ID_TypeMembre__Nom_Type_M='membre_personnel').order_by(order_by_field)

    paginator = Paginator(personnel_list, 10)
    page = request.GET.get('page')
    personnels = paginator.get_page(page)

    subtitle = 'Liste des personnels'

    return render(request, 'personnel/personnel_list.html', {'personnels': personnels, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def personnel_detail(request, encrypted_id):
    ID_Membre = decrypt_id(encrypted_id, settings.SECRET_KEY)

    if ID_Membre is not None:
        personnel = get_object_or_404(Membre, pk=ID_Membre)
        subtitle = 'Détail du personnel'
        return render(request, 'personnel/personnel_detail.html', {'personnel': personnel, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def personnel_create(request):
    type_membre_personnel = TypeMembre.objects.get(Nom_Type_M='membre_personnel')
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            personnel = form.save(commit=False)
            personnel.ID_TypeMembre = type_membre_personnel
            personnel.save()
            messages.success(request, 'Personnel ajouté avec succès.')
            return redirect('personnel_list_back')
    else:
        form = PersonnelForm(initial={'ID_TypeMembre': type_membre_personnel})
    subtitle = 'Ajouter du personnel'
    return render(request, 'personnel/personnel_form.html', {'form': form, 'subtitle': subtitle})

@login_required
def personnel_update(request, encrypted_id):
    try:
        personnel_id = decrypt_id(encrypted_id, settings.SECRET_KEY)
        personnel = get_object_or_404(Membre, pk=personnel_id)

        if request.method == 'POST':
            form = PersonnelForm(request.POST, instance=personnel)
            if form.is_valid():
                form.save()
                messages.success(request, 'Personnel modifié avec succès.')
                return redirect('personnel_list_back')
        else:
            form = PersonnelForm(instance=personnel)
        subtitle = 'Modifier le personnel'
        return render(request, 'personnel/personnel_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in personnel_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du personnel.')
        return render(request, 'erreur/404.html')

@login_required
def personnel_delete(request, encrypted_id):
    personnel_id = decrypt_id(encrypted_id, settings.SECRET_KEY)

    if personnel_id is not None:
        personnel = get_object_or_404(Membre, pk=personnel_id)
        personnel.delete()
        messages.success(request, 'Personnel supprimé avec succès.')
        return redirect('personnel_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du personnel.')
        return render(request, 'erreur/404.html')

# posteDuPersonnel :
@login_required
def posteDuPersonnel_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Poste_P')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Poste_P']  
    default_sort_field = 'Poste_P'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        PosteDuPersonnel_list = PosteDuPersonnel.objects.filter(Q(Poste_P__icontains=search_query)).order_by(order_by_field)
    else:
        PosteDuPersonnel_list = PosteDuPersonnel.objects.all().order_by(order_by_field)

    paginator = Paginator(PosteDuPersonnel_list, 10)
    page = request.GET.get('page')
    posteDuPersonnels = paginator.get_page(page)

    subtitle = 'Liste des posteDuPersonnels'

    return render(request, 'posteDuPersonnel/PosteDuPersonnel_list.html', {'posteDuPersonnels': posteDuPersonnels, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def posteDuPersonnel_detail(request, encrypted_id):
    ID_PosteDuPersonnel = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_PosteDuPersonnel is not None:
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=ID_PosteDuPersonnel)
        subtitle = 'Détail de la posteDuPersonnel'
        return render(request, 'posteDuPersonnel/posteDuPersonnel_detail.html', {'posteDuPersonnel': posteDuPersonnel, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def posteDuPersonnel_create(request):
    if request.method == 'POST':
        form = PosteDuPersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poste_P du personnel ajouté avec succès.')
            return redirect('posteDuPersonnel_list_back')
    else:
        form = PosteDuPersonnelForm()
    subtitle = 'Ajouter des postes du personnel'
    return render(request, 'posteDuPersonnel/posteDuPersonnel_form.html', {'form': form, 'subtitle': subtitle})

# posteDuPersonnel_update
@login_required
def posteDuPersonnel_update(request, encrypted_id):
    try:
        posteDuPersonnel_id = decrypt_id(encrypted_id, SECRET_KEY)
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=posteDuPersonnel_id)

        if request.method == 'POST':
            form = PosteDuPersonnelForm(request.POST, instance=posteDuPersonnel)
            if form.is_valid():
                form.save()
                messages.success(request, 'poste du personnel modifié avec succès.')
                return redirect('posteDuPersonnel_list_back')
        else:
            form = PosteDuPersonnelForm(instance=posteDuPersonnel)
        subtitle = 'Modifier des posteDuPersonnel'
        return render(request, 'posteDuPersonnel/posteDuPersonnel_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in posteDuPersonnel_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du posteDuPersonnel.')
        return render(request, 'erreur/404.html')

# posteDuPersonnel_delete
@login_required
def posteDuPersonnel_delete(request, encrypted_id):
    posteDuPersonnel_id = decrypt_id(encrypted_id, SECRET_KEY)

    if posteDuPersonnel_id is not None:
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=posteDuPersonnel_id)
        posteDuPersonnel.delete()
        messages.success(request, 'PosteDuPersonnel supprimée avec succès.')
        return redirect('posteDuPersonnel_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du posteDuPersonnel.')
        return render(request, 'erreur/404.html')


# posteDuPersonnel :
@login_required
def posteDuPersonnel_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Poste_P')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Poste_P']  
    default_sort_field = 'Poste_P'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        PosteDuPersonnel_list = PosteDuPersonnel.objects.filter(Q(Poste_P__icontains=search_query)).order_by(order_by_field)
    else:
        PosteDuPersonnel_list = PosteDuPersonnel.objects.all().order_by(order_by_field)

    paginator = Paginator(PosteDuPersonnel_list, 10)
    page = request.GET.get('page')
    posteDuPersonnels = paginator.get_page(page)

    subtitle = 'Liste des postes du personnel'

    return render(request, 'posteDuPersonnel/PosteDuPersonnel_list.html', {'posteDuPersonnels': posteDuPersonnels, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def posteDuPersonnel_detail(request, encrypted_id):
    ID_PosteDuPersonnel = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_PosteDuPersonnel is not None:
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=ID_PosteDuPersonnel)
        subtitle = 'Détail de la posteDuPersonnel'
        return render(request, 'posteDuPersonnel/posteDuPersonnel_detail.html', {'posteDuPersonnel': posteDuPersonnel, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')

@login_required
def posteDuPersonnel_create(request):
    if request.method == 'POST':
        form = PosteDuPersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'poste du personnel ajouté avec succès.')
            return redirect('posteDuPersonnel_list_back')
    else:
        form = PosteDuPersonnelForm()
    subtitle = 'Ajouter des posteDuPersonnel'
    return render(request, 'posteDuPersonnel/posteDuPersonnel_form.html', {'form': form, 'subtitle': subtitle})

# posteDuPersonnel_update
@login_required
def posteDuPersonnel_update(request, encrypted_id):
    try:
        posteDuPersonnel_id = decrypt_id(encrypted_id, SECRET_KEY)
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=posteDuPersonnel_id)

        if request.method == 'POST':
            form = PosteDuPersonnelForm(request.POST, instance=posteDuPersonnel)
            if form.is_valid():
                form.save()
                messages.success(request, 'poste du personnel modifié avec succès.')
                return redirect('posteDuPersonnel_list_back')
        else:
            form = PosteDuPersonnelForm(instance=posteDuPersonnel)
        subtitle = 'Modifier des posteDuPersonnel'
        return render(request, 'posteDuPersonnel/posteDuPersonnel_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in posteDuPersonnel_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du posteDuPersonnel.')
        return render(request, 'erreur/404.html')

# posteDuPersonnel_delete
@login_required
def posteDuPersonnel_delete(request, encrypted_id):
    posteDuPersonnel_id = decrypt_id(encrypted_id, SECRET_KEY)

    if posteDuPersonnel_id is not None:
        posteDuPersonnel = get_object_or_404(PosteDuPersonnel, pk=posteDuPersonnel_id)
        posteDuPersonnel.delete()
        messages.success(request, 'poste du personnel supprimée avec succès.')
        return redirect('posteDuPersonnel_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du posteDuPersonnel.')
        return render(request, 'erreur/404.html')


#Publication évenement
@login_required
def evenement_non_publie_calendrier(request):
    evenements_non_publies = Evenement.objects.filter(Publie_E=False, Date_Heure_Debut__gte=timezone.now()).order_by('Date_Debut_E')
    return render(request, 'evenement/evenement_non_publie_calendrier.html', {'evenements_non_publies': evenements_non_publies, 'SECRET_KEY': settings.SECRET_KEY})

@login_required
def publier_evenement(request, evenement_id):
    evenement = Evenement.objects.get(pk=evenement_id)
    evenement.Publie_E = True
    evenement.save()
    messages.success(request, f"Événement '{evenement.Titre_E}' publié avec succès.")
    return redirect('evenement_non_publie_calendrier')

@login_required
def envoyer_mail(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            destinataires = [utilisateur.Email for utilisateur in Membre.objects.all() if utilisateur.Email]
            send_mail(sujet, message, settings.EMAIL_HOST_USER, destinataires)
            # Redirection ou autre action après l'envoi du mail
            messages.success(request, 'email envoyé à toutes les utilsiateurs avec succès')
            return redirect ('envoyer_mail')
    else:
        form = MailForm()
        
    subtitle = 'Envoie des mails à toutes les utilisateurs'
    return render(request, 'mail/mailForm.html', {'form': form, 'subtitle': subtitle})

    
# typeMembre :
@login_required
def typeMembre_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Nom_Type_M')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Nom_Type_M']  
    default_sort_field = 'Nom_Type_M'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        TypeMembre_list = TypeMembre.objects.filter(Q(Nom_Type_M__icontains=search_query)).order_by(order_by_field)
    else:
        TypeMembre_list = TypeMembre.objects.all().order_by(order_by_field)

    paginator = Paginator(TypeMembre_list, 10)
    page = request.GET.get('page')
    typeMembres = paginator.get_page(page)

    subtitle = 'Liste des typeMembres'

    return render(request, 'typeMembre/TypeMembre_list.html', {'typeMembres': typeMembres, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def typeMembre_detail(request, encrypted_id):
    ID_TypeMembre = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_TypeMembre is not None:
        typeMembre = get_object_or_404(TypeMembre, pk=ID_TypeMembre)
        subtitle = 'Détail de la typeMembre'
        return render(request, 'typeMembre/typeMembre_detail.html', {'typeMembre': typeMembre, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')
    
@login_required
def typeMembre_create(request):
    if request.method == 'POST':
        form = TypeMembreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'TypeMembre ajouté avec succès.')
            return redirect('typeMembre_list_back')
    else:
        form = TypeMembreForm()
    subtitle = 'Ajouter des typeMembre'
    return render(request, 'typeMembre/typeMembre_form.html', {'form': form, 'subtitle': subtitle})

# typeMembre_update method in views.py
@login_required
def typeMembre_update(request, encrypted_id):
    try:
        typeMembre_id = decrypt_id(encrypted_id, SECRET_KEY)
        typeMembre = get_object_or_404(TypeMembre, pk=typeMembre_id)

        if request.method == 'POST':
            form = TypeMembreForm(request.POST, instance=typeMembre)
            if form.is_valid():
                form.save()
                messages.success(request, 'TypeMembre modifié avec succès.')
                return redirect('typeMembre_list_back')
        else:
            form = TypeMembreForm(instance=typeMembre)
        subtitle = 'Modifier des typeMembre'
        return render(request, 'typeMembre/typeMembre_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in typeMembre_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du typeMembre.')
        return render(request, 'erreur/404.html')

# typeMembre_delete method in views.py
@login_required
def typeMembre_delete(request, encrypted_id):
    typeMembre_id = decrypt_id(encrypted_id, SECRET_KEY)

    if typeMembre_id is not None:
        typeMembre = get_object_or_404(TypeMembre, pk=typeMembre_id)
        typeMembre.delete()
        messages.success(request, 'TypeMembre supprimée avec succès.')
        return redirect('typeMembre_list_back')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du typeMembre.')
        return render(request, 'erreur/404.html')

@login_required
def article_list(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'Titre_Article')
    direction = request.GET.get('direction', 'asc')

    valid_sort_fields = ['Titre_Article', 'Date_Publication_A']
    default_sort_field = 'Titre_Article'

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    if direction not in ['asc', 'desc']:
        direction = 'asc'

    order_by_field = f'{sort_by}' if direction == 'asc' else f'-{sort_by}'

    if search_query:
        Article_list = Article.objects.filter(Q(Titre_Article__icontains=search_query)).order_by(order_by_field)
    else:
        Article_list = Article.objects.all().order_by(order_by_field)

    paginator = Paginator(Article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    subtitle = 'Liste des articles'

    return render(request, 'article/Article_list.html', {'articles': articles, 'SECRET_KEY': settings.SECRET_KEY, 'search_query': search_query, 'sort_by': sort_by, 'direction': direction, 'subtitle': subtitle})

@login_required
def article_detail(request, encrypted_id):
    ID_Article = decrypt_id(encrypted_id, SECRET_KEY)

    if ID_Article is not None:
        article = get_object_or_404(Article, pk=ID_Article)
        subtitle = 'Détail de la article'
        return render(request, 'article/article_detail.html', {'article': article, 'subtitle': subtitle})
    else:
        return render(request, 'erreur/404.html')


@login_required
def article_create(request, encrypted_id):
    evenement_id = decrypt_id(encrypted_id, SECRET_KEY)
    evenement = Evenement.objects.get(pk=evenement_id)
    subtitle = 'Rédiger un article'

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.ID_Evenement = evenement
            article.save()
            messages.success(request, 'Article créé avec succès.')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article/article_form.html', {'form': form, 'subtitle': subtitle})


# article_update method in views.py
@login_required
def article_update(request, encrypted_id):
    try:
        article_id = decrypt_id(encrypted_id, SECRET_KEY)
        article = get_object_or_404(Article, pk=article_id)

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                messages.success(request, 'Article modifié avec succès.')
                return redirect('article_list')
        else:
            form = ArticleForm(instance=article)
        subtitle = 'Modifier des article'
        return render(request, 'article/article_form.html', {'form': form,'subtitle': subtitle})
    except Exception as e:
        print(f"Error in article_update: {e}")
        messages.error(request, 'Une erreur s\'est produite lors de la modification du article.')
        return render(request, 'erreur/404.html')

# article_delete method in views.py
@login_required
def article_delete(request, encrypted_id):
    article_id = decrypt_id(encrypted_id, SECRET_KEY)

    if article_id is not None:
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        messages.success(request, 'Article supprimée avec succès.')
        return redirect('article_list')
    else:
        messages.error(request, 'Une erreur s\'est produite lors de la suppression du article.')
        return render(request, 'erreur/404.html')
    
@login_required
def inscription_evenement_list(request):
    # Récupérer la liste des événements publiés et dont la date limite d'inscription n'est pas encore atteinte
    evenement_list = Evenement.objects.filter(Publie_E=True, Inscription_E=True, Date_Limite_Inscription__gte=timezone.now().date())
    subtitle = 'Liste d\'inscriptions à un événement'

    context = {'evenement_list': evenement_list, 'SECRET_KEY': settings.SECRET_KEY, 'subtitle': subtitle}
    return render(request, 'inscriptionEvenement/inscription_evenement_list.html', context)

@csrf_exempt
def get_inscrits_by_evenement(request):
    if request.method == 'POST':
        evenement_id = request.POST.get('evenement_id')
        if evenement_id:
            inscrits = InscriptionEvenement.objects.filter(ID_Evenement=evenement_id).select_related('ID_Membre').values(
                'ID_Membre__Nom_M', 'ID_Membre__Prenom_M', 'Date_Inscription_E', 'ID_Evenement__Date_Limite_Inscription', 'ID_Evenement__Date_Debut_E'
            )
            return JsonResponse(list(inscrits), safe=False)
        else:
            return JsonResponse({'error': 'Evenement ID is required'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def historique_inscriptions(request):
    membre_simple = TypeMembre.objects.get(Nom_Type_M='membre_simple')
    membre_personnel = TypeMembre.objects.get(Nom_Type_M='membre_personnel')

    evenements_publics = Evenement.objects.filter(Publie_E=True, Inscription_E=True, ID_Categorie_E__Categorie_E='public').order_by('-Date_Debut_E')
    evenements_personnels = Evenement.objects.filter(Publie_E=True, Inscription_E=True, ID_Categorie_E__Categorie_E='personnel').order_by('-Date_Debut_E')

    context = {
        'evenements_publics': evenements_publics,
        'evenements_personnels': evenements_personnels,
        'membre_simple': membre_simple,
        'membre_personnel': membre_personnel,
        'SECRET_KEY': settings.SECRET_KEY
    }
    return render(request, 'inscriptionEvenement/historique_inscription.html', context)

@login_required
def detail_inscription(request, encrypted_id):
    evenement_id = decrypt_id(encrypted_id, SECRET_KEY)

    if evenement_id is not None:
        evenement = get_object_or_404(Evenement, pk=evenement_id)
        inscrits = InscriptionEvenement.objects.filter(ID_Evenement=evenement).select_related('ID_Membre')

        context = {
            'evenement': evenement,
            'inscrits': inscrits,
        }
        return render(request, 'inscriptionEvenement/detail_inscription.html', context)
    else:
        return render(request, 'erreur/404.html')

@login_required
def envoi_notification_mail_list(request):
    evenements = Evenement.objects.filter(
        Inscription_E=True,
        Publie_E=True,
    ).annotate(
        total_inscrits=Count('inscriptionevenement')
    )

    context = {'evenements': evenements}
    return render(request, 'notification/envoi_notification_mail.html', context)

@csrf_exempt
@login_required
def send_notification(request):
    if request.method == 'POST':
        evenement_id = request.POST.get('evenement_id')
        objet = request.POST.get('objet')
        message = request.POST.get('message')

        if evenement_id and objet and message:
            evenement = get_object_or_404(Evenement, pk=evenement_id)
            inscrits = InscriptionEvenement.objects.filter(ID_Evenement=evenement)
            total_inscrits = inscrits.count()

            progress_key = f'progress_{evenement_id}'
            request.session[progress_key] = 0

            for i, inscrit in enumerate(inscrits):
                membre = inscrit.ID_Membre
                notification = Notification.objects.create(
                    Message=message,
                    Date_Envoi=timezone.now(),
                    Est_Lu=False,
                    ID_Evenement=evenement,
                    ID_Membre=membre
                )
                if membre.Mail_M:
                    send_mail(
                        objet,
                        message,
                        'zorojuro1299@gmail.com',
                        [membre.Mail_M],
                        fail_silently=False,
                    )

                # Mise à jour de la progression
                request.session[progress_key] = int((i + 1) / total_inscrits * 100)

            return JsonResponse({'success': 'Notification envoyée avec succès', 'total_inscrits': total_inscrits}, status=200)
        else:
            return JsonResponse({'error': 'Tous les champs sont obligatoires'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def get_progress(request):
    evenement_id = request.GET.get('evenement_id')
    progress_key = f'progress_{evenement_id}'
    progress = request.session.get(progress_key, 0)
    return JsonResponse({'progress': progress})

@login_required
def message_history(request):
    subtitle = 'Historique des notifications envoyées'
    
    notifications = Notification.objects.values(
        'ID_Evenement',
        'ID_Evenement__Titre_E',
        'Message'
    ).annotate(
        latest_date=Max('Date_Envoi'),
        count=Count('ID_Notification')
    ).order_by('-latest_date')

    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    notification_messages = paginator.get_page(page)

    return render(request, 'notification/historique_message.html', {
        'notification_messages': notification_messages,
        'subtitle': subtitle,
        'SECRET_KEY': settings.SECRET_KEY
    })

@login_required
def message_history_detail(request, encrypted_id):
    evenement_id = decrypt_id(encrypted_id, settings.SECRET_KEY)
    notifications = Notification.objects.filter(ID_Evenement=evenement_id).order_by('-Date_Envoi')

    if notifications.exists():
        evenement = notifications.first().ID_Evenement
        grouped_notifications = notifications.values('Message').annotate(
            latest_date=Max('Date_Envoi')
        ).order_by('-latest_date')

        # Préparez les membres pour chaque notification
        notifications_with_members = []
        for notification in grouped_notifications:
            members = Notification.objects.filter(
                ID_Evenement=evenement,
                Message=notification['Message']
            ).values('ID_Membre__Nom_M', 'ID_Membre__Mail_M').distinct()
            notifications_with_members.append({
                'Message': notification['Message'],
                'latest_date': notification['latest_date'],
                'members': members
            })

        subtitle = f'Détail des notifications pour {evenement.Titre_E}'

        return render(request, 'notification/detail_message.html', {
            'notifications_with_members': notifications_with_members,
            'evenement': evenement,
            'subtitle': subtitle
        })
    else:
        return render(request, 'erreur/404.html')


#Notification 

@login_required
def check_notifications(request):
    # Notification pour les événements sur le point de se terminer
    upcoming_events = Evenement.objects.filter(Date_Debut_E__lte=timezone.now() + timedelta(days=3), Date_Fin_E__gte=timezone.now(), Est_Fait=False)
    for event in upcoming_events:
        Notification.objects.get_or_create(
            Message=f"L'événement '{event.Titre_E}' est sur le point de se terminer.",
            Date_Envoi=timezone.now(),
            ID_Evenement=event,
            Est_Lu_Admin=False,
            ID_Membre=None  # Notification pour administrateur
        )

    # Notification pour les audiences non marquées comme faites
    past_audiences = Evenement.objects.filter(ID_Categorie_E__isnull=True, Date_Arrive_E__lt=timezone.now(), Est_Fait=False)
    for audience in past_audiences:
        Notification.objects.get_or_create(
            Message=f"L'audience '{audience.Titre_E}' n'est pas marquée comme faite.",
            Date_Envoi=timezone.now(),
            ID_Evenement=audience,
            Est_Lu_Admin=False,
            ID_Membre=None  # Notification pour administrateur
        )

    # Autres notifications importantes
    # Par exemple, événements à publier qui ne sont pas encore publiés
    unpublished_events = Evenement.objects.filter(Publie_E=False, Date_Debut_E__lte=timezone.now() + timedelta(days=7))
    for event in unpublished_events:
        Notification.objects.get_or_create(
            Message=f"L'événement '{event.Titre_E}' doit être publié.",
            Date_Envoi=timezone.now(),
            ID_Evenement=event,
            Est_Lu_Admin=False,
            ID_Membre=None  # Notification pour administrateur
        )

    return JsonResponse({'status': 'ok'})

@login_required
def admin_notifications(request):
    notifications = Notification.objects.filter(Est_Lu_Admin=False, ID_Membre=None).order_by('-Date_Envoi')
    return render(request, 'notification/notifications.html', {'notifications': notifications})

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(Est_Lu_Admin=False, ID_Membre=None).update(Est_Lu_Admin=True)
    return redirect('admin_notifications')

def base(request):
    notifications = Notification.objects.filter(Est_Lu_Admin=False, ID_Membre=None).order_by('-Date_Envoi')
    notifications_count = notifications.count()
    return render(request, 'base.html', {'notifications': notifications, 'notifications_count': notifications_count})


#Connexion
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Connexion'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Connexion réussie.')
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('adminlogin')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, 'Déconnexion réussie.')
        return response
    


class ForgotPasswordView(View):
    template_name = 'forgot_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            code = get_random_string(length=6, allowed_chars='1234567890')
            request.session['reset_code'] = code
            request.session['reset_email'] = email
            send_mail(
                'Password Reset Code',
                f'Your password reset code is {code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, f'A code has been sent to {email}')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid email address')
            return render(request, self.template_name)

class PasswordResetView(View):
    template_name = 'reset_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('code')
        if code == request.session.get('reset_code'):
            messages.success(request, 'Code verified, please change your password')
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid code')
            return render(request, self.template_name)

class PasswordChangeView(View):
    template_name = 'change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('adminlogin')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, self.template_name)