Ouvrir la barre latérale
ChatGPT

Alors pour une application de gestion des événements avec redaction des articles voici mes codes : 

extrait de mon settings.py :
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static')
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'gera_back/static'),
]


extrait de mon urls.py : 
    # villes
    path('ville_list', gera_back.ville_list, name='ville_list_back'),
    path('ville-form', gera_back.ville_create, name='ville-form'),
    path('<str:encrypted_id>/ville_detail', gera_back.ville_detail, name='ville_detail'),
    path('create_ville', gera_back.ville_create, name='ville_create'),
    path('<str:encrypted_id>/update_ville/', gera_back.ville_update, name='ville_update'),
    path('<str:encrypted_id>/delete_ville/', gera_back.ville_delete, name='ville_delete'),
    
extrait de models.py : 
class Evenement(models.Model):
    ID_Evenement = models.AutoField(primary_key=True)
    Titre_E = models.CharField(max_length=255, null=True)
    Description_E = models.CharField(max_length=255, null=True)
    Date_Arrive_E = models.DateField(null=True)
    Date_Debut_E = models.DateField(null=True)
    Heure_Debut_E = models.TimeField(null=True)
    Date_Fin_E = models.DateField(null=True)
    Heure_Fin_E = models.TimeField(null=True)
    Publie_E = models.BooleanField(default=None, null=True)
    Image_E = models.ImageField(upload_to='evenement_images/', null=True, blank=True)
    ID_Lieu = models.ForeignKey('Lieu', null=True, on_delete=models.PROTECT)
    ID_Categorie_E = models.ForeignKey('CategorieEvenement', null=True, on_delete=models.CASCADE)
    ID_Interlocuteur = models.ForeignKey('Interlocuteur', null=True, on_delete=models.PROTECT)
    Inscription_E = models.BooleanField(default=None, null=True)
    Date_Limite_Inscription = models.DateField(null=True)
    Est_Fait = models.BooleanField(null=True)
    Num_Audience = models.IntegerField (null = True)
    def __str__(self):
        return self.Titre_E
    class Meta:
        db_table = "Evenement"

class CategorieEvenement(models.Model):
    ID_Categorie_E = models.AutoField(primary_key=True)
    Categorie_E = models.CharField(max_length=50)
    ID_Type_E = models.ForeignKey('TypeEvenement', on_delete=models.CASCADE)
    def __str__(self):
        return self.Categorie_E
    class Meta:
        db_table = "CategorieEvenement"
        
class TypeEvenement(models.Model):
    ID_Type_E = models.AutoField(primary_key=True)
    Nom_Type_E = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_Type_E
    class Meta:
        db_table = "TypeEvenement"


gera_back/views.py : 

@login_required
def evenement_publier_list(request):
    subtitle = 'Liste de publication des événements'
    evenement_list = Evenement.objects.filter(ID_Categorie_E__ID_Type_E__Nom_Type_E='Apublier')
    fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E', 'ID_Interlocuteur', 'Image_E', 'Publie_E']
    # Appliquer la recherche et le tri
    search_query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by', 'Titre_E')
    direction = request.GET.get('direction', 'asc')

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


templates/evenement/evenement_publier_list.html :
{% extends 'base.html' %}
{% load custom_filters %}
{% load static %}

{% block search %}

<div class="col-md-7 mt-5">
  <form class="d-flex justify-content-between align-items-center" action="{% url 'evenement_publier_list' %}" method="GET">
    <input class="form-control" type="text" name="q" placeholder="Rechercher...">
    <input class="form-control" type="date" name="start_date" placeholder="Date de début">
    <input class="form-control" type="date" name="end_date" placeholder="Date de fin">
    <button type='submit' class='btn btn-link text-dark btn-block custom-btn-link'>
      <i class='mdi mdi-magnify icon-size'></i></button>
  </form>
</div>
{% endblock search %}

{% block content %}

<!-- Ajouter un champ select pour choisir la catégorie lors de l'export PDF -->


<!-- Tableau des événements à publier -->
<div class="row">
  <div class="col-md-12">
    <table class="table table-dark table-striped">
      <thead>
        <tr>
          <th><a href="">Titre</a></th>
          <th><a href="">Date Debut</a></th>
          <th><a href="">Date Fin</a></th>
          <th><a href="">Lieu</a></th>
          <th><a href="">Catégorie</a></th>
          <th><a href="">Image</a></th>
          <th><a href="">Publié</a></th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for evenement in evenements %}
        <tr>
          <td>{{ evenement.Titre_E }}</td>
          <td>{{ evenement.Date_Debut_E }}</td>
          <td>{{ evenement.Date_Fin_E|default:"-" }}</td>
          <td>{{ evenement.ID_Lieu }} {{ evenement.ID_Lieu.ID_Adresse.ID_Quartier.Nom_Quartier }}</td>
          <td>{{ evenement.ID_Categorie_E }}</td>
          <td><img src="{% static evenement.Image_E %}" alt="Image de l'événement" width="75" height="75"></td>
          <td>{{ evenement.Publie_E }}</td>
          <td class="action">
            <a class="btn btn-link text-light btn-block custom-btn-link" href="{% url 'evenement_detail' encrypted_id=evenement.ID_Evenement|encrypt_id:SECRET_KEY %}"><i class='mdi mdi-eye'></i></a> |
            <a class="btn btn-link text-primary btn-block custom-btn-link" href="{% url 'evenement_publie_update' encrypted_id=evenement.ID_Evenement|encrypt_id:SECRET_KEY %}" onclick="return confirm('Voulez-vous vraiment modifier ce evenement ?')"><i class='mdi mdi-border-color'></i></a> |
            <a class="btn btn-link custom-btn-link text-danger btn-block" href="{% url 'evenement_delete' encrypted_id=evenement.ID_Evenement|encrypt_id:SECRET_KEY %}" onclick="return confirm('Voulez-vous vraiment supprimer cette evenement ?')"><i class='mdi mdi-delete'></i></a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% if evenements.has_other_pages %}
    <ul class="pagination justify-content-center">
      {% if evenements.has_previous %}
      <li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>
      <li class="page-item"><a class="page-link" href="?page={{ evenements.previous_page_number }}">{{ evenements.previous_page_number }}</a></li>
      {% endif %}
      <li class="page-item active"><a class="page-link" href="?page={{ evenements.number }}">{{ evenements.number }}</a></li>
      {% if evenements.has_next %}
      <li class="page-item"><a class="page-link" href="?page={{ evenements.next_page_number }}">{{ evenements.next_page_number }}</a></li>
      <li class="page-item"><a class="page-link" href="?page={{ evenements.paginator.num_pages }}">&raquo;</a></li>
      {% endif %}
    </ul>
    {% endif %}
  </div>
</div>

<!-- Modal pour la sélection de la plage de dates -->
<div class="modal fade" id="dateRangeModal" tabindex="-1" role="dialog" aria-labelledby="dateRangeModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="dateRangeModalLabel">Sélectionner la plage de dates</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form id="dateRangeForm">
          <div class="form-group">
            <label for="startDate">Date de début</label>
            <input type="date" class="form-control" id="startDate">
          </div>
          <div class="form-group">
            <label for="endDate">Date de fin</label>
            <input type="date" class="form-control" id="endDate">
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
        <button type="button" class="btn btn-primary" id="export-pdf-confirm">OK</button>
      </div>
    </div>
  </div>
</div>
{% endblock content %}

{% block scripts %}
<script>
  $(document).ready(function() {
    $('#export-pdf').click(function() {
      $('#dateRangeModal').modal('show');
    });

    $('#export-pdf-confirm').click(function() {
      var startDate = $('#startDate').val();
      var endDate = $('#endDate').val();
      var category = $('#pdf-category').val();
      
      // Redirection vers l'URL d'export en PDF avec les dates et la catégorie sélectionnées
      window.location.href = '/export-pdf/?start_date=' + startDate + '&end_date=' + endDate + '&category=' + category;
    });
  });
</script>
{% endblock scripts %}

Fonctionnalités à mettre à jour : 
Alors l'ordre des événements sur la liste des événements à publier sont en désordre donc veuillez le à l'ordre decroissant s'il vous plait, c'est à dire afficher les événements recents à venir (Date_Debut_E) tout en haut de la liste et ainsi de suite s'il vous plait.

Donc veuillez donner le code au grand complet sans exception de ce qui sont à modifier pour faire ces mise à jour au grand complet sans exception s'il vous plait.

ChatGPT
Pour mettre à jour votre application afin que la liste des événements soit affichée en ordre décroissant par la date de début (Date_Debut_E), il vous suffit de modifier l'ordre de tri dans la vue evenement_publier_list. Voici le code mis à jour avec les modifications nécessaires :

settings.py
Aucune modification nécessaire pour cette tâche spécifique.

urls.py
Aucune modification nécessaire pour cette tâche spécifique.

models.py
Aucune modification nécessaire pour cette tâche spécifique.

views.py
Mettons à jour votre fichier views.py pour trier les événements en ordre décroissant par Date_Debut_E.

python
Copier le code
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Evenement

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
evenement_publier_list.html
Aucune modification nécessaire pour cette tâche spécifique.

Conclusion
Les modifications apportées au fichier views.py trient les événements par Date_Debut_E en ordre décroissant par défaut. Assurez-vous que le champ de tri (sort_by) et la direction (direction) sont correctement définis dans votre logique de vue pour refléter cette modification.

Cela devrait répondre à votre demande de trier les événements de manière à afficher les événements récents à venir en haut de la liste.







Message ChatGPT

ChatGPT peut faire des erreurs. Envisagez de vérifier les informations importantes.
ChatGPT
