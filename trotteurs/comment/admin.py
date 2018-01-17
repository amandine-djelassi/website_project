from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'content_object', 'get_username', 'content', 'timestamp')

admin.site.register(Comment, CommentAdmin)
