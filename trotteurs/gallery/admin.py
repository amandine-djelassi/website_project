from django.contrib import admin
from .models import Photo, Album

# Model the admin manages
admin.site.register(Photo)
admin.site.register(Album)
