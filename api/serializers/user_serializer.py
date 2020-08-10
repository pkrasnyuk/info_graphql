import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.helpers.validators import alphanumeric, letters_only


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, max_length=128)
    is_superuser = serializers.BooleanField(default=False)
    username = serializers.CharField(required=True, max_length=150, min_length=4,
                                     validators=[alphanumeric, UniqueValidator(queryset=User.objects.all(),
                                                                               message="A user with that username "
                                                                                       "already exists.")])
    first_name = serializers.CharField(required=False, max_length=30, min_length=6, validators=[letters_only])
    last_name = serializers.CharField(required=False, max_length=150, min_length=6, validators=[letters_only])
    email = serializers.EmailField(required=True, max_length=254,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="A user with that email already exists.")])
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)

    def validate(self, data):
        password = data.get('password')
        errors = dict()

        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
