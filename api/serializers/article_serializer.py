from rest_framework import serializers

from api.models.article import Article
from api.serializers.user_serializer import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["creator"] = UserSerializer(instance.creator).data
        return representation

    class Meta:
        model = Article
        fields = ("id", "title", "body", "type", "tags", "creator", "created_at", "modified_at")
        read_only_fields = ("created_at", "modified_at")
        extra_kwargs = {"creator": {"default": serializers.CurrentUserDefault()}}


class ArticleTagsSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField(help_text="article tag", max_length=255), read_only=True)
