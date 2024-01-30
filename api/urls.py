from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import article_image_view_set, article_view_set, user_login_view_set, user_view_set

router = SimpleRouter()
router.register(r"articles", article_view_set.ArticleViewSet)

urlpatterns = [
    url("", include(router.urls)),
    path(
        "articles/",
        include(
            (
                [
                    path("creator/<int:creator_pk>/", article_view_set.CreatorArticleViewSet.as_view()),
                    path("tags/all/", article_view_set.ArticleTagsViewSet.as_view()),
                    path("tags/<str:tag>/", article_view_set.TagArticleViewSet.as_view()),
                ],
                "api",
            ),
            namespace="articles",
        ),
    ),
    path(
        "article_images/",
        include(
            (
                [
                    path("", article_image_view_set.ArticleImageList.as_view()),
                    path("<int:pk>/", article_image_view_set.ArticleImageDetail.as_view()),
                ],
                "api",
            ),
            namespace="article_images",
        ),
    ),
    path(
        "users/",
        include(
            (
                [
                    path("", user_view_set.UserList.as_view()),
                    path("<int:pk>/", user_view_set.UserDetail.as_view()),
                    path("signup/", user_login_view_set.UserLoginViewSet.as_view()),
                ],
                "api",
            ),
            namespace="users",
        ),
    ),
]
