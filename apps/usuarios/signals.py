from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def asignar_grupo_por_defecto(sender, instance, created, **kwargs):
    if created:
        try:
            grupo_miembro = Group.objects.get(name='Miembro')
            instance.groups.add(grupo_miembro)
        except Group.DoesNotExist:
            # Si el grupo no existe, no hacemos nada (o podríamos crearlo)
            pass
