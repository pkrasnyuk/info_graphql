import graphene
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from api.models.article import Article
from api.models.article_image import ArticleImage
from api.schema.objects.input_object_types import ArticleImageInput
from api.schema.objects.object_types import ArticleImageObjectType


class CreateArticleImage(graphene.Mutation):
    class Arguments:
        _input = ArticleImageInput(required=True)

    ok = graphene.Boolean()
    articleImage = graphene.Field(ArticleImageObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _input=None):
        ok = True
        article = Article.objects.get(pk=_input.article.id)
        if article is None:
            return CreateArticleImage(ok=False, articleImage=None)
        article_image_instance = ArticleImage(name=_input.name, article=article)

        try:
            article_image_instance.full_clean()
        except ValidationError as ex:
            raise GraphQLError(str(ex))

        article_image_instance.save()
        return CreateArticleImage(ok=ok, articleImage=article_image_instance)


class UpdateArticleImage(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)
        _input = ArticleImageInput(required=True)

    ok = graphene.Boolean()
    articleImage = graphene.Field(ArticleImageObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _id, _input=None):
        ok = False
        article_image_instance = ArticleImage.objects.get(pk=_id)
        if article_image_instance:
            ok = True
            article = Article.objects.get(pk=_input.article.id)
            if article is None:
                return UpdateArticleImage(ok=False, articleImage=None)
            if _input.name:
                article_image_instance.name = _input.name
            article_image_instance.article = article

            try:
                article_image_instance.full_clean()
            except ValidationError as ex:
                raise GraphQLError(str(ex))

            article_image_instance.save()
            return UpdateArticleImage(ok=ok, articleImage=article_image_instance)
        return UpdateArticleImage(ok=ok, articleImage=None)


class DeleteArticleImage(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, _id):
        ok = False
        article_image_instance = ArticleImage.objects.get(pk=_id)
        if article_image_instance:
            ok = True
            article_image_instance.delete()
        return DeleteArticleImage(ok=ok)
