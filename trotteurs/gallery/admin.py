from django.contrib import admin
from .models import Photo, Album, Country, City

# Model the admin manages
admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Country)
admin.site.register(City)
