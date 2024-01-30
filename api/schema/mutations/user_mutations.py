import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from graphql_jwt.decorators import login_required, superuser_required

from api.schema.objects.input_object_types import UserInput
from api.schema.objects.object_types import UserObjectType


class CreateUser(graphene.Mutation):
    class Arguments:
        _input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _input=None):
        ok = True
        user_instance = User(
            username=_input.username,
            password=make_password(_input.password),
            first_name=_input.first_name,
            last_name=_input.last_name,
            email=_input.email,
            is_superuser=_input.is_superuser,
            is_staff=_input.is_staff,
            is_active=_input.is_active,
        )

        try:
            user_instance.full_clean()
        except ValidationError as ex:
            raise GraphQLError(str(ex))

        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)
        _input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, _id, _input=None):
        ok = False
        user_instance = User.objects.get(pk=_id)
        if user_instance:
            ok = True
            if _input.username:
                user_instance.username = _input.username
            if _input.password:
                user_instance.password = make_password(_input.password)
            if _input.first_name:
                user_instance.first_name = _input.first_name
            if _input.last_name:
                user_instance.last_name = _input.last_name
            if _input.email:
                user_instance.email = _input.email
            if _input.is_superuser:
                user_instance.is_superuser = _input.is_superuser
            if _input.is_staff:
                user_instance.is_staff = _input.is_staff
            if _input.is_active:
                user_instance.is_active = _input.is_active

            try:
                user_instance.full_clean()
            except ValidationError as ex:
                raise GraphQLError(str(ex))

            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        _id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @superuser_required
    def mutate(root, info, _id):
        ok = False
        user_instance = User.objects.get(pk=_id)
        if user_instance:
            ok = True
            user_instance.delete()
        return UpdateUser(ok=ok)
