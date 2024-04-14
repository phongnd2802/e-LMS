from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import MaterialDetail

@receiver(pre_save, sender=MaterialDetail)
def delete_old_file(sender, instance, **kwargs):
    if instance.pk:
        old_instance = MaterialDetail.objects.get(pk=instance.pk)
        if old_instance.file != instance.file and old_instance.file:
            old_instance.file.delete(save=False)


