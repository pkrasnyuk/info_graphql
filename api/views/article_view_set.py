from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.helpers.common import ConnectionValidations, NoTitleAutoSchema
from api.models.article import Article
from api.serializers.article_serializer import ArticleSerializer, ArticleTagsSerializer


class ArticlePagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 25


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    queryset = (
        Article.objects.all().cache(ops=["get", "fetch"], timeout=1800)
        if ConnectionValidations.redis_connection_validation()
        else Article.objects.all()
    )
    serializer_class = ArticleSerializer

    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("title",)
    ordering_fields = (
        "created_at",
        "modified_at",
    )
    ordering = ("created_at",)

    swagger_schema = NoTitleAutoSchema


class CreatorArticleViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        creator_pk = self.kwargs["creator_pk"]
        return Article.objects.filter(creator=creator_pk)


class TagArticleViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        tag = self.kwargs["tag"]
        return Article.objects.filter(tags__contains=[tag])


class ArticleTagsViewSet(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_class = [JSONWebTokenAuthentication, OAuth2Authentication]
    serializer_class = ArticleTagsSerializer
    http_method_names = ["get"]

    def get(self, request, **kwargs):
        tag_list = []
        for item in Article.objects.values_list("tags", flat=True).distinct():
            if item is not None:
                tag_list += item

        return Response({"tags": sorted(list(set(tag_list)))}, status=status.HTTP_200_OK)
