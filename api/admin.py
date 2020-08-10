from django.contrib import admin

from api.models.article import Article
from api.models.article_image import ArticleImage

# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleImage)
