from django.contrib import admin
from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'get_tags', 'nb_comments')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
