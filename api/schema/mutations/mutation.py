import graphene

from api.schema.mutations.article_image_mutations import CreateArticleImage, UpdateArticleImage, DeleteArticleImage
from api.schema.mutations.article_mutations import CreateArticle, UpdateArticle, DeleteArticle
from api.schema.mutations.user_mutations import CreateUser, UpdateUser, DeleteUser


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
    create_article_image = CreateArticleImage.Field()
    update_article_image = UpdateArticleImage.Field()
    delete_article_image = DeleteArticleImage.Field()
