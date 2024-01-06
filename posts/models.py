import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver

User = get_user_model()


def upload_to(instance: "Note", filename: str) -> str:
    """Путь для файла относительно корня медиа хранилища."""
    return f"{instance.uuid}/{filename}"


class Note(models.Model):
    # Стандартный ID для каждой таблицы можно не указывать, Django по умолчанию это добавит.

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(null=True, default=None)
    autor = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, null=True, verbose_name='Изображение')

    # auto_now_add=True автоматически добавляет текущую дату и время.

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Note)
def delete_image_after_delete_post(sender, instance: Note, **kwargs):
    file_path = (settings.MEDIA_ROOT / str(instance.uuid))
    if file_path.exists():
        for file in file_path.iterdir():
            file.unlink(missing_ok=False)
        file_path.rmdir()


@receiver(pre_save, sender=Note)
def delete_old_image(sender, instance: Note, **kwargs):
    file_path = (settings.MEDIA_ROOT / str(instance.uuid))
    if file_path.exists():
        for file in file_path.iterdir():
            file.unlink(missing_ok=False)
