import os
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django_cleanup import cleanup
from PIL import Image

from api.helpers.image_helper import name_file
from api.models.article import Article
from api.models.entity_model import EntityModel


@cleanup.ignore
class ArticleImage(EntityModel):
    name = models.CharField(help_text="article image name", max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to=name_file, max_length=254, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to=name_file, max_length=300, blank=True, null=True)
    article = models.ForeignKey(
        Article, blank=False, null=False, on_delete=models.CASCADE, related_name="images", help_text="related article"
    )

    def __str__(self):
        return self.name

    def create_thumbnail(self, thumbnails=None):
        if thumbnails is None:
            thumbnails = []
        image = Image.open(self.image.file.file)
        file_name, ext = os.path.splitext(self.image.name)
        for w, h in thumbnails:
            image.thumbnail(size=(w, h))
            image_file = BytesIO()
            image.save(image_file, image.format)
            self.thumbnail_image.save(
                f"{file_name}_{w}x{h}{ext}",
                InMemoryUploadedFile(
                    image_file,
                    None,
                    "",
                    self.image.file.content_type,
                    image.size,
                    self.image.file.charset,
                ),
                save=False,
            )

    def save(self, *args, **kwargs):
        if self.image and not self.thumbnail_image:
            self.create_thumbnail(thumbnails=[(128, 128)])
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
