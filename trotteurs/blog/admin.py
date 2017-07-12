from django.contrib import admin
from .models import Article, Tag

# Model the admin manages
admin.site.register(Article)
admin.site.register(Tag)
