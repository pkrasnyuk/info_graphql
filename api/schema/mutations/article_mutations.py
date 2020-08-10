import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from api.models.article import Article
from api.schema.objects.input_object_types import ArticleInput
from api.schema.objects.object_types import ArticleObjectType


class CreateArticle(graphene.Mutation):
    class Arguments:
        _input = ArticleInput(required=True)

    ok = graphene.Boolean()
    article = graphene.Field(ArticleObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _input=None):
        ok = True
        creator = User.objects.get(pk=_input.creator.id)
        if creator is None:
            return CreateArticle(ok=False, article=None)
        article_instance = Article(
            title=_input.title,
            body=_input.body,
            tags=_input.tags,
            type=_input.type,
            creator=creator
        )

        try:
            article_instance.full_clean()
        except ValidationError as ex:
            raise GraphQLError(str(ex))

        article_instance.save()
        return CreateArticle(ok=ok, article=article_instance)


class UpdateArticle(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)
        _input = ArticleInput(required=True)

    ok = graphene.Boolean()
    article = graphene.Field(ArticleObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _id, _input=None):
        ok = False
        article_instance = Article.objects.get(pk=_id)
        if article_instance:
            ok = True
            creator = User.objects.get(pk=_input.creator.id)
            if creator is None:
                return UpdateArticle(ok=False, article=None)
            if _input.title:
                article_instance.title = _input.title
            if _input.body:
                article_instance.body = _input.body
            if _input.type:
                article_instance.type = _input.type
            if _input.tags:
                article_instance.tags = _input.tags
            article_instance.creator = creator

            try:
                article_instance.full_clean()
            except ValidationError as ex:
                raise GraphQLError(str(ex))

            article_instance.save()
            return UpdateArticle(ok=ok, article=article_instance)
        return UpdateArticle(ok=ok, article=None)


class DeleteArticle(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, _id):
        ok = False
        article_instance = Article.objects.get(pk=_id)
        if article_instance:
            ok = True
            article_instance.delete()
        return DeleteArticle(ok=ok)
