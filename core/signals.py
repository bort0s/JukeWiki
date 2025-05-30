from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profilo

@receiver(post_save, sender=User)
def crea_profilo(sender, instance, created, **kwargs):
    if created:
        Profilo.objects.create(utente=instance)
