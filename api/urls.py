from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter

from api import views

router = SimpleRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url('', include(router.urls)),
    path('articles/', include(([
                                   path('creator/<int:creator_pk>/',
                                        views.article_view_set.CreatorArticleViewSet.as_view()),
                                   path('tags/all/', views.article_view_set.ArticleTagsViewSet.as_view()),
                                   path('tags/<str:tag>/', views.article_view_set.TagArticleViewSet.as_view()),
                               ], 'api'), namespace='articles')),
    path('article_images/', include(([
                                         path('', views.article_image_view_set.ArticleImageList.as_view()),
                                         path('<int:pk>/', views.article_image_view_set.ArticleImageDetail.as_view()),
                                     ], 'api'), namespace='article_images')),
    path('users/', include(([
                                path('', views.user_view_set.UserList.as_view()),
                                path('<int:pk>/', views.user_view_set.UserDetail.as_view()),
                                path('signup/', views.UserLoginViewSet.as_view()),
                            ], 'api'), namespace='users')),
]
