from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models

from api.helpers.validators import alphanumeric
from api.models.article_type import ArticleType
from api.models.entity_model import EntityModel


class Article(EntityModel):
    title = models.CharField(help_text="article title", max_length=255, blank=False, null=False,
                             validators=[alphanumeric, MinLengthValidator(10)])
    body = models.TextField(help_text="article body", max_length=2048, blank=False, null=False,
                            validators=[MinLengthValidator(15)])
    type = models.CharField(help_text="article type", max_length=32, choices=ArticleType.CHOICES,
                            default=ArticleType.IT)
    tags = ArrayField(models.CharField(help_text="article tag", max_length=255, blank=False, null=False), blank=False,
                      null=True)
    creator = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='articles',
                                help_text="article creator")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
