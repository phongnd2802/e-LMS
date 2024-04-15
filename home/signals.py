from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import MaterialDetail, Assignment

@receiver(pre_save, sender=MaterialDetail)
def delete_old_file(sender, instance, **kwargs):
    if instance.pk:
        old_instance = MaterialDetail.objects.get(pk=instance.pk)
        if old_instance.file != instance.file and old_instance.file:
            old_instance.file.delete(save=False)

@receiver([pre_save, pre_delete], sender=Assignment)
def delete_old_file(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Assignment.objects.get(pk=instance.pk)
        if old_instance.file != instance.file and old_instance.file:
            old_instance.file.delete(save=False)
