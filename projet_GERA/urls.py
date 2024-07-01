"""
URL configuration for projet_GERA project.

the `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gera_back import views as gera_back
from app_GERA import views as app_GERA
from django.contrib.auth import views as auth_views

# from app_GERA.views import PersonnelForm
from gera_back import utils
from gera_back.views import CustomLoginView, CustomLogoutView, ForgotPasswordView, PasswordResetView, PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('dashboard', gera_back.dashboard, name='dashboard'),


    #backend

    #Administration générale 
    path('administration_generale', gera_back.administration_generale, name='administration_generale'),

    # villes
    path('ville_list', gera_back.ville_list, name='ville_list_back'),
    path('ville-form', gera_back.ville_create, name='ville-form'),
    path('<str:encrypted_id>/ville_detail', gera_back.ville_detail, name='ville_detail'),
    path('create_ville', gera_back.ville_create, name='ville_create'),
    path('<str:encrypted_id>/update_ville/', gera_back.ville_update, name='ville_update'),
    path('<str:encrypted_id>/delete_ville/', gera_back.ville_delete, name='ville_delete'),
    
    # #quartiers
    path('quartier_list', gera_back.quartier_list, name='quartier_list'),
    path('<str:encrypted_id>/quartier_detail/', gera_back.quartier_detail, name='quartier_detail'),
    path('create_quartier', gera_back.quartier_create, name='quartier_create'),
    path('<str:encrypted_id>/update_quartier/', gera_back.quartier_update, name='quartier_update'),
    path('<str:encrypted_id>/delete_quartier/', gera_back.quartier_delete, name='quartier_delete'),

    #lieux
    path('lieu_list', gera_back.lieu_list, name='lieu_list'),
    path('<str:encrypted_id>/lieu_detail/', gera_back.lieu_detail, name='lieu_detail'),
    path('create_lieu', gera_back.lieu_create, name='lieu_create'),
    path('<str:encrypted_id>/update_lieu/', gera_back.lieu_update, name='lieu_update'),
    path('<str:encrypted_id>/delete_lieu/', gera_back.lieu_delete, name='lieu_delete'),
    
    #evenements
    path('evenement_list', gera_back.evenement_list, name='evenement_list'),
    path('export-pdf/', gera_back.export_pdf, name='export_pdf'),
    path('export-selected-pdf/', gera_back.export_pdf_selected_events, name='export_pdf_selected_events'),
    path('export-pdf-upcoming-invitation/', gera_back.export_pdf_upcoming_invitation, name='export_pdf_upcoming_invitation'),

    path('evenement_publier_list', gera_back.evenement_publier_list, name='evenement_publier_list'),
    path('evenement_sans_article', gera_back.evenement_sans_article_list, name='evenement_sans_article'),

    path('<str:encrypted_id>/evenement_detail/', gera_back.evenement_detail, name='evenement_detail'),
    path('create_evenement/invitation', gera_back.evenement_invitation_create, name='create_evenement_invitation'),
    path('create_evenement/audience', gera_back.evenement_audience_create, name='create_evenement_audience'),
    path('create_evenement/apublier', gera_back.evenement_a_publier_create, name='create_evenement_a_publier'),

    path('create_evenement', gera_back.evenement_create, name='evenement_create'),
    path('<str:encrypted_id>/update_evenement', gera_back.evenement_update, name='evenement_update'),
    path('<str:encrypted_id>/evenement_publie_update', gera_back.evenement_publie_update, name='evenement_publie_update'),
    path('<str:encrypted_id>/delete_evenement', gera_back.evenement_delete, name='evenement_delete'),
    path('evenement/mark_done/', gera_back.mark_event_done, name='evenement_mark_done'),

    #inscription événement
    path('inscription_suivi', gera_back.inscription_evenement_list, name='inscription_suivi'),
    path('get-inscrits-by-evenement/', gera_back.get_inscrits_by_evenement, name='get_inscrits_by_evenement'),
    path('historique_inscriptions', gera_back.historique_inscriptions, name='historique_inscriptions'),
    path('detail-inscription/<str:encrypted_id>', gera_back.detail_inscription, name='detail_inscription'),

    # interlocuteurs
    path('interlocuteur_list', gera_back.interlocuteur_list, name='interlocuteur_list_back'),
    path('<str:encrypted_id>/interlocuteur_detail', gera_back.interlocuteur_detail, name='interlocuteur_detail'),
    path('create_interlocuteur', gera_back.interlocuteur_create, name='interlocuteur_create'),
    path('<str:encrypted_id>/update_interlocuteur/', gera_back.interlocuteur_update, name='interlocuteur_update'),
    path('<str:encrypted_id>/delete_interlocuteur/', gera_back.interlocuteur_delete, name='interlocuteur_delete'),

    # personnels
    path('personnel_list', gera_back.personnel_list, name='personnel_list_back'),
    path('personnel-form', gera_back.personnel_create, name='personnel_create'),
    path('<str:encrypted_id>/personnel_detail', gera_back.personnel_detail, name='personnel_detail'),
    path('<str:encrypted_id>/update_personnel/', gera_back.personnel_update, name='personnel_update'),
    path('<str:encrypted_id>/delete_personnel/', gera_back.personnel_delete, name='personnel_delete'),


    #Notification
    path('send_notification/', gera_back.send_notification, name='send_notification'),
    path('envoi_notification_mail', gera_back.envoi_notification_mail_list, name='envoi_notification_mail'),
    path('get_progress/', gera_back.get_progress, name='get_progress'),
    path('message_history', gera_back.message_history, name='message_history'),
    path('notification/detail/<str:encrypted_id>/', gera_back.message_history_detail, name='message_history_detail'),
    
    #Notification admin
    path('check_notifications/', gera_back.check_notifications, name='check_notifications'),
    path('admin_notifications/', gera_back.admin_notifications, name='admin_notifications'),
    path('mark_all_notif_read/', gera_back.mark_all_as_read, name='mark_all_notif_read'),

    #articles 
    path('<str:encrypted_id>/create_article', gera_back.article_create, name='article_create'),
    path('article_list', gera_back.article_list, name='article_list'),
    path('article-form', gera_back.article_create, name='article-form'),
    path('<str:encrypted_id>/article_detail', gera_back.article_detail, name='article_detail'),
    path('<str:encrypted_id>/update_article/', gera_back.article_update, name='article_update'),
    path('<str:encrypted_id>/delete_article/', gera_back.article_delete, name='article_delete'),
    # path('evenement_list?category=apublier', name='article_red'),

    # categorieEvenements
    path('categorieEvenement_list', gera_back.categorieEvenement_list, name='categorieEvenement_list_back'),
    path('categorieEvenement-form', gera_back.categorieEvenement_create, name='categorieEvenement-form'),
    path('<str:encrypted_id>/categorieEvenement_detail', gera_back.categorieEvenement_detail, name='categorieEvenement_detail'),
    path('create_categorieEvenement', gera_back.categorieEvenement_create, name='categorieEvenement_create'),
    path('<str:encrypted_id>/update_categorieEvenement/', gera_back.categorieEvenement_update, name='categorieEvenement_update'),
    path('<str:encrypted_id>/delete_categorieEvenement/', gera_back.categorieEvenement_delete, name='categorieEvenement_delete'),

    # typeEvenements
    path('typeEvenement_list', gera_back.typeEvenement_list, name='typeEvenement_list_back'),
    path('<str:encrypted_id>/typeEvenement_detail', gera_back.typeEvenement_detail, name='typeEvenement_detail'),
    # path('create_typeEvenement', gera_back.typeEvenement_create, name='typeEvenement_create'),
    # path('<str:encrypted_id>/update_typeEvenement/', gera_back.typeEvenement_update, name='typeEvenement_update'),
    # path('<str:encrypted_id>/delete_typeEvenement/', gera_back.typeEvenement_delete, name='typeEvenement_delete'),

    # typeMembres
    path('typeMembre_list', gera_back.typeMembre_list, name='typeMembre_list_back'),
    path('<str:encrypted_id>/typeMembre_detail', gera_back.typeMembre_detail, name='typeMembre_detail'),
    # path('create_typeMembre', gera_back.typeMembre_create, name='typeMembre_create'),
    # path('<str:encrypted_id>/update_typeMembre/', gera_back.typeMembre_update, name='typeMembre_update'),
    # path('<str:encrypted_id>/delete_typeMembre/', gera_back.typeMembre_delete, name='typeMembre_delete'),

    # posts du personnel
    path('posteDuPersonnel_list', gera_back.posteDuPersonnel_list, name='posteDuPersonnel_list_back'),
    path('posteDuPersonnel-form', gera_back.posteDuPersonnel_create, name='posteDuPersonnel-form'),
    path('<str:encrypted_id>/posteDuPersonnel_detail', gera_back.posteDuPersonnel_detail, name='posteDuPersonnel_detail'),
    path('create_posteDuPersonnel', gera_back.posteDuPersonnel_create, name='posteDuPersonnel_create'),
    path('<str:encrypted_id>/update_posteDuPersonnel/', gera_back.posteDuPersonnel_update, name='posteDuPersonnel_update'),
    path('<str:encrypted_id>/delete_posteDuPersonnel/', gera_back.posteDuPersonnel_delete, name='posteDuPersonnel_delete'),

    # # #personnels
    # path('personnel_list', gera_back.personnel_list, name='personnel_list'),
    # path('<str:encrypted_id>/personnel_detail/', gera_back.personnel_detail, name='personnel_detail'),
    # path('create_personnel', gera_back.personnel_create, name='personnel_create'),
    # path('<str:encrypted_id>/update_personnel/', gera_back.personnel_update, name='personnel_update'),
    # path('<str:encrypted_id>/delete_personnel/', gera_back.personnel_delete, name='personnel_delete'),
   
    # # utilisateurSimples
    # path('utilisateurSimple_list', gera_back.utilisateurSimple_list, name='utilisateurSimple_list_back'),
    # path('<str:encrypted_id>/delete_utilisateurSimple/', gera_back.utilisateurSimple_delete, name='utilisateurSimple_delete'),
    
    #mail
    path('envoyer_mail/', gera_back.envoyer_mail, name='envoyer_mail'),
    
    #publication évenement
    path('evenement_non_publie_calendrier/', gera_back.evenement_non_publie_calendrier, name='evenement_non_publie_calendrier'),
    path('<str:encrypted_id>/publier_evenement/', gera_back.publier_evenement, name='publier_evenement'),

    #api frontend
    
    #villes
    path('api/ville-list/', app_GERA.ville_list, name='ville_list'),
    path('api/ville-detail/<int:pk>/', app_GERA.ville_detail, name='ville_detail'),
    
    #événements
    path('api/prochain-evenement/', app_GERA.prochain_evenement, name='prochain-evenement'),
    # path('api/inscription/Personnel/<str:matricule>/check/', app_GERA.check_matricule_existence, name='check_matricule_existence'),
    path('api/articles/', app_GERA.get_published_articles, name='get_published_articles'),
    path('api/evenement-detail/<int:pk>/', app_GERA.evenement_detail, name='evenement_detail'),
    path('api/article-detail/<int:pk>/', app_GERA.article_detail, name='article_detail'),
    #Inscription :
    # path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),
    # Connexion
    path('api/login/', app_GERA.member_login, name='login'),
    path('api/logout/', app_GERA.member_logout, name='logout'),
    path('api/check_login/', app_GERA.check_login, name='member_check_login'),

    path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),

    # path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),
    path('api/inscription/membre-simple/', app_GERA.register_utilisateur_simple, name='register_utilisateur_simple'),

    path('api/evenements_personnel/', app_GERA.evenements_personnel, name='evenements_personnel'),
    path('api/evenements_public/', app_GERA.evenements_public, name='evenements_public'),
    # path('api/inscription-evenement/', app_GERA.inscription_evenement, name='inscription_evenement'),
    path('api/inscription-evenement/<int:pk>/', app_GERA.inscription_evenement, name='inscription_evenement'),

    # Notifications
    path('api/notifications/', app_GERA.get_notifications, name='get_notifications'),
    path('api/notifications/mark-all-as-read/', app_GERA.mark_all_as_read, name='mark_all_as_read'),
    

    #connexion et déconnexion back
    path('adminlogin', CustomLoginView.as_view(), name='adminlogin'),
    path('adminlogout', CustomLogoutView.as_view(), name='adminlogout'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password', PasswordResetView.as_view(), name='reset_password'),
    path('change-password', PasswordChangeView.as_view(), name='change_password'),

    path('',  CustomLoginView.as_view(), name='homepage'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

