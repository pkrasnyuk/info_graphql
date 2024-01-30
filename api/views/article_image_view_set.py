from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.helpers.common import ConnectionValidations, NoTitleAutoSchema
from api.models.article_image import ArticleImage
from api.serializers.article_image_serializer import ArticleImageSerializer
from api.serializers.article_serializer import ArticleTagsSerializer


class ArticleImageList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    queryset = (
        ArticleImage.objects.all().cache(ops=["get", "fetch"], timeout=1800)
        if ConnectionValidations.redis_connection_validation()
        else ArticleImage.objects.all()
    )
    serializer_class = ArticleTagsSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("article",)
    ordering_fields = (
        "created_at",
        "modified_at",
    )
    ordering = ("created_at",)

    swagger_schema = NoTitleAutoSchema


class ArticleImageDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    queryset = (
        ArticleImage.objects.all().cache(ops=["get", "fetch"], timeout=1800)
        if ConnectionValidations.redis_connection_validation()
        else ArticleImage.objects.all()
    )
    serializer_class = ArticleImageSerializer
