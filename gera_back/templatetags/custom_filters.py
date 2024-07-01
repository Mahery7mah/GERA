# templatetags/custom_filters.py
from django import template
from gera_back.utils import encrypt_id

register = template.Library()

@register.filter(name='encrypt_id')
def encrypt_id_filter(value, secret_key):
    encrypted_id = encrypt_id(value, secret_key)  # Décodez l'objet bytes en str
    return encrypted_id


@register.filter
def get_prev_date(evenement_list, counter):
    prev_index = counter - 1
    if prev_index >= 0:
        return evenement_list[prev_index].Date_arrive
    else:
        return None