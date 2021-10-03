from django.db import models
from django.utils.translation import gettext_lazy as _
from config.models import CreationModificationDateBase


class ImageModel(CreationModificationDateBase):
    name = models.CharField(_("Name"), max_length=51)
    image = models.ImageField(_("image"), upload_to='images')
    description = models.TextField()

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.name
