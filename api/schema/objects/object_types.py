from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from api.models.article import Article
from api.models.article_image import ArticleImage


class ArticleObjectType(DjangoObjectType):
    class Meta:
        model = Article


class ArticleImageObjectType(DjangoObjectType):
    class Meta:
        model = ArticleImage


class UserObjectType(DjangoObjectType):
    class Meta:
        model = User
