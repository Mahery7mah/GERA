from django.contrib.auth.backends import BaseBackend
from .models import Membre

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Membre.objects.get(Nom_Utilisateur=username)
            if user.check_password(password):
                return user
        except Membre.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Membre.objects.get(pk=user_id)
        except Membre.DoesNotExist:
            return None