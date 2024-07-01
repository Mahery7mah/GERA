from django import forms
from app_GERA.models import Ville, Quartier, Adresse, Lieu, Evenement, CategorieEvenement, Interlocuteur, PosteDuPersonnel, Membre, TypeEvenement, Article, AuteurArticle, TypeMembre
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django_ckeditor_5.widgets import CKEditor5Widget


class EvenementSearchForm(forms.Form):
    q = forms.CharField(max_length=255, required=False, label='Rechercher')
    category = forms.ChoiceField(choices=[('invitation', 'Invitation'), ('audience', 'Audience'), ('apublier', 'A publier')], required=False, label='Catégorie')


#Villes
class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = ['Nom_Ville', 'CodePostal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nom_Ville'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['CodePostal'].widget.attrs['class'] = 'form-control custom-width'


#Quartiers
class QuartierForm(forms.ModelForm):
    ID_Ville = forms.ModelChoiceField(
        queryset=Ville.objects.all(),
        label='Ville',
        widget=forms.Select(attrs={'class': 'form-control custom-width'}),
    )
    class Meta:
        model = Quartier
        fields = ['Nom_Quartier', 'ID_Ville']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nom_Quartier'].widget.attrs['class'] = 'form-control custom-width'
        
#Lieux
class LieuForm(forms.ModelForm):
    # Supprimer le champ 'Adresse' et ajouter les champs 'Rue' et 'Quartier'
    Rue = forms.CharField(max_length=255, label='Rue', widget=forms.TextInput(attrs={'class': 'form-control custom-width'}))
    ID_Quartier = forms.ModelChoiceField(queryset=Quartier.objects.all(), required=False, label='Quartier', widget=forms.Select(attrs={'class': 'form-control custom-width'}))
    Disponibilite_Lieu = forms.BooleanField(label='Disponible',required=False, widget=forms.CheckboxInput(attrs={'class': ''}))
    Capacite_Lieu = forms.IntegerField(label='Capacité',required=False)
    Rue = forms.CharField(label='Rue',required=False)

    class Meta:
        model = Lieu
        # Mettre à jour la liste des champs
        fields = ['Lieu', 'Capacite_Lieu', 'Disponibilite_Lieu'
        , 'Rue', 'ID_Quartier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mettre à jour les classes des champs
        self.fields['Lieu'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['Rue'].widget.attrs['class'] = 'form-control custom-width'

        self.fields['Capacite_Lieu'].widget.attrs['class'] = 'form-control custom-width'

#Evenements
class EvenementForm(forms.ModelForm):
    Titre_E = forms.CharField(max_length=255, label='Titre de l\'événement', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description = forms.CharField(max_length=255, label='Description de l\'événement', widget=forms.Textarea(attrs={'class': 'form-control'}))
    Date_Debut_E = forms.DateTimeField(label='Date de début', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    Date_Fin_E = forms.TimeField(label='Date de fin', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    ID_Lieu = forms.ModelChoiceField(queryset=Lieu.objects.all(), label='Lieu', widget=forms.Select(attrs={'class': 'form-control'}))
    ID_Categorie_E = forms.ModelChoiceField(queryset=CategorieEvenement.objects.all(), label='Catégorie', widget=forms.Select(attrs={'class': 'form-control'}))
    ID_Interlocuteur = forms.ModelChoiceField(queryset=Interlocuteur.objects.all(), label='Interlocuteur', widget=forms.Select(attrs={'class': 'form-control'}))
    Image_E = forms.ImageField(label='Image de l\'événement', required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'directory': 'assets/images/'}))
    Publie_E = forms.BooleanField(label='Publié', required=False)
    assigned_personnel = forms.ModelMultipleChoiceField(queryset=Membre.objects.filter(ID_TypeMembre='1'), required=False, label='Personnels assignés', widget=forms.SelectMultiple(attrs={'class': 'form-control'}))


    class Meta:
        model = Evenement
        fields = ['Titre_E', 'Description', 'Date_Debut_E', 'Date_Fin_E', 'ID_Lieu', 'ID_Categorie_E', 'ID_Interlocuteur', 'Image_E', 'Publie_E']
        widgets = {
            'Date_Debut_E': forms.DateTimeInput(attrs={'class': 'form-', 'type': 'datetime-local'}),
            'Date_Fin_E': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'Image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}) # Ajoutez cet attribut pour accepter uniquement les images
        }
    
class EvenementInvitationForm(forms.ModelForm):
    Titre_E = forms.CharField(max_length=255, label='Titre de l\'événement', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description_E = forms.CharField(max_length=255, label='Description de l\'événement', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    Date_Arrive_E = forms.DateField(label='Date d\'arrivée', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    Date_Debut_E = forms.DateField(label='Date de début', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    Heure_Debut_E = forms.TimeField(label='Heure de debut',required=False, widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'))
    Heure_Fin_E = forms.TimeField(label='Heure de fin',required=False, widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'))

    Date_Fin_E = forms.DateField(label='Date de Fin', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    ID_Lieu = forms.ModelChoiceField(queryset=Lieu.objects.all(), label='Lieu', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    ID_Categorie_E = forms.ModelChoiceField(queryset=CategorieEvenement.objects.filter(
        ID_Type_E__in=TypeEvenement.objects.filter(Nom_Type_E='Invitation')
    ), label='Catégorie', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Evenement
        fields = ['Titre_E', 'Description_E', 'Date_Arrive_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'ID_Lieu', 'ID_Categorie_E']

class EvenementAudienceForm(forms.ModelForm):

    Titre_E = forms.CharField(max_length=255, label='Titre de l\'événement', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description_E = forms.CharField(required=False, label='Description de l\'événement', widget=forms.Textarea(attrs={'class': 'auto-expand form-control'}))
    Date_Arrive_E = forms.DateField(label='Date d\'arrivée', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    ID_Interlocuteur = forms.ModelChoiceField(queryset=Interlocuteur.objects.all(), label='Interlocuteur', widget=forms.Select(attrs={'class': 'form-control'}))
    Num_Audience = forms.IntegerField(label='Capacité',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}) )

    class Meta:
        model = Evenement
        fields = ['Num_Audience', 'Titre_E', 'Description_E', 'Date_Arrive_E', 'ID_Interlocuteur', 'Est_Fait']

class EvenementAPublierForm(forms.ModelForm):
    Titre_E = forms.CharField(max_length=255, label='Titre de l\'événement', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description_E = forms.CharField(label='Description de l\'événement', widget=forms.Textarea(attrs={'class': 'form-control'}))
    Date_Debut_E = forms.DateField(label='Date de début', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    Date_Fin_E = forms.DateField(label='Date de Fin', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    Heure_Debut_E = forms.TimeField(label='Heure de debut',required=False, widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'))
    Heure_Fin_E = forms.TimeField(label='Heure de fin',required=False, widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'))

    ID_Lieu = forms.ModelChoiceField(queryset=Lieu.objects.all(), label='Lieu', widget=forms.Select(attrs={'class': 'form-control'}))
    ID_Categorie_E = forms.ModelChoiceField(queryset=CategorieEvenement.objects.filter(
        ID_Type_E__in=TypeEvenement.objects.filter(Nom_Type_E='Apublier')
    ), label='Catégorie', widget=forms.Select(attrs={'class': 'form-control'}))
    Image_E = forms.ImageField(label='Image de l\'événement', required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'directory': 'assets/images/'}))
    Publie_E = forms.BooleanField(label='Publié', required=False)
    Inscription_E = forms.BooleanField(label='Inscription', required=False)
    Date_Limite_Inscription = forms.DateTimeField(label='Date de limite d\'inscription',required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Evenement
        fields = ['Titre_E', 'Description_E', 'Date_Debut_E', 'Heure_Debut_E', 'Date_Fin_E', 'Heure_Fin_E', 'Publie_E', 'Image_E', 'ID_Categorie_E', 'ID_Lieu', 'Inscription_E', 'Date_Limite_Inscription' ]

#Interlocuteurs
class InterlocuteurForm(forms.ModelForm):
    class Meta:
        model = Interlocuteur
        fields = ['Nom_I', 'Prenom_I', 'Description_I', 'Mail_I', 'Tel_I']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nom_I'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['Prenom_I'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['Description_I'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['Mail_I'].widget.attrs['class'] = 'form-control custom-width'
        self.fields['Tel_I'].widget.attrs['class'] = 'form-control custom-width'

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['Matricule_M', 'Nom_M', 'Prenom_M', 'ID_Poste_P', 'Mail_M', 'Tel_M', 'ID_TypeMembre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['Tel_M'].widget.attrs['pattern'] = r'\d{3} \d{2} \d{3} \d{2}'
        self.fields['ID_TypeMembre'].widget.attrs['readonly'] = True
        self.fields['ID_TypeMembre'].widget.attrs['hidden'] = True


#CategorieEvenement
class CategorieEvenementForm(forms.ModelForm):
    ID_Type_E = forms.ModelChoiceField(
        queryset=TypeEvenement.objects.all(),
        label='Type',
        widget=forms.Select(attrs={'class': 'form-control custom-width'}),
    )
    class Meta:
        model = CategorieEvenement
        fields = ['Categorie_E', 'ID_Type_E']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Categorie_E'].widget.attrs['class'] = 'form-control custom-width'

#TypeEvenement 
class TypeEvenementForm(forms.ModelForm):
    class Meta:
        model = TypeEvenement
        fields = ['Nom_Type_E']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nom_Type_E'].widget.attrs['class'] = 'form-control custom-width'

#TypeMembre 
class TypeMembreForm(forms.ModelForm):
    class Meta:
        model = TypeMembre
        fields = ['Nom_Type_M']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nom_Type_M'].widget.attrs['class'] = 'form-control custom-width'


#PosteDuPersonnels
class PosteDuPersonnelForm(forms.ModelForm):
    class Meta:
        model = PosteDuPersonnel
        fields = ['Poste_P']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Poste_P'].widget.attrs['class'] = 'form-control custom-width'

#connexion
class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'


class MailForm(forms.Form):
    sujet = forms.CharField(max_length=100, label='Sujet du mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Message')

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields['message'].required = False
        
class ArticleForm(forms.ModelForm):
    Titre_Article = forms.CharField(max_length=255, label="Titre de l'article", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Date_Publication_A = forms.DateField(label="Date de publication", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    ID_Auteur = forms.ModelChoiceField(
        queryset=AuteurArticle.objects.all(),
        label='Auteur',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control custom-width'}),
    )
    Publie_A = forms.BooleanField(label='Publier article',required=False, widget=forms.CheckboxInput(attrs={'class': 'icon-lg'}))

    class Meta:
        model = Article
        fields = ['Titre_Article', 'Contenu_Article', 'Date_Publication_A', 'ID_Auteur', 'Publie_A']
        widgets = {
            "Contenu_Article": CKEditor5Widget(config_name="extends", attrs={"class": "django_ckeditor_5"}),
        }
        ckeditor5_config = {
            'image': {
                'resizeOptions': [
                    {
                        'name': 'resizeImage:25',
                        'value': '25',
                        'icon': 'small'
                    }
                ]
            }
        }