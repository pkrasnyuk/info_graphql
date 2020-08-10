import graphene
from django.contrib.auth.models import User
from django.db.models import Q
from graphene import ObjectType

from api.models.article import Article
from api.models.article_image import ArticleImage
from api.schema.objects.object_types import UserObjectType, ArticleObjectType, ArticleImageObjectType


class Query(ObjectType):
    user = graphene.Field(UserObjectType, id=graphene.Int())
    article = graphene.Field(ArticleObjectType, id=graphene.Int())
    articleImage = graphene.Field(ArticleImageObjectType, id=graphene.Int())
    users = graphene.List(UserObjectType)
    articles = graphene.List(ArticleObjectType)
    articleImages = graphene.List(ArticleImageObjectType)
    articleList = graphene.List(ArticleObjectType, search=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_user(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return User.objects.get(pk=_id)

        return None

    def resolve_article(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return Article.objects.get(pk=_id)

        return None

    def resolve_articleImage(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return ArticleImage.objects.get(pk=_id)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_articles(self, info, **kwargs):
        return Article.objects.all()

    def resolve_articleImages(self, info, **kwargs):
        return ArticleImage.objects.all()

    def resolve_articleList(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Article.objects.all()

        if search:
            article_filter = (
                    Q(title__icontains=search) |
                    Q(body__icontains=search)
            )
            qs = qs.filter(article_filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs
