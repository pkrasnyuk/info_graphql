from rest_framework import serializers

from api.models.article_image import ArticleImage
from api.serializers.article_serializer import ArticleSerializer


class ArticleImageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["article"] = ArticleSerializer(instance.article).data
        return representation

    class Meta:
        model = ArticleImage
        fields = ("id", "name", "image", "thumbnail_image", "article", "created_at", "modified_at")
        read_only_fields = ("thumbnail_image", "created_at", "modified_at")
