from django.db import models


class EntityModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="entity created at")
    modified_at = models.DateTimeField(auto_now=True, help_text="entity modified at")

    class Meta:
        abstract = True
