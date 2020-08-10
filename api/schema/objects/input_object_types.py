import graphene
from graphene import String

from api.helpers.common import to_enum
from api.models.article_type import ArticleType

ArticleTypeEnum = to_enum(ArticleType, type_name="ArticleTypeEnum")


class UserInput(graphene.InputObjectType):
    id = graphene.ID(description="User Id", required=False)
    username = graphene.String(description="User Name", required=True)
    password = graphene.String(description="User Password", required=True)
    first_name = graphene.String(description="User First Name", required=False)
    last_name = graphene.String(description="User Last Name", required=False)
    email = graphene.String(description="User Email", required=True)
    is_superuser = graphene.Boolean(description="Is SuperUser Status", required=False)
    is_staff = graphene.Boolean(description="Is Staff Status", required=False)
    is_active = graphene.Boolean(description="Is Active Status", required=False)


class CreatorInput(graphene.InputObjectType):
    id = graphene.ID(description="Creator Id", required=True)


class ArticleInput(graphene.InputObjectType):
    id = graphene.ID(description="Article Id", required=False)
    title = graphene.String(description="Article Title", required=True)
    body = graphene.String(description="Article Body", required=True)
    type = ArticleTypeEnum(description="Article Type", required=True)
    tags = graphene.List(String, required=False)
    creator = graphene.Field(CreatorInput, description="Article Creator", required=True)


class RelatedArticleInput(graphene.InputObjectType):
    id = graphene.ID(description="Related Article Id", required=True)


class ArticleImageInput(graphene.InputObjectType):
    id = graphene.ID(description="Article Image Id", required=False)
    name = graphene.String(description="Article Image Name", required=True)
    article = graphene.Field(RelatedArticleInput, description="Related Article", required=True)
