from django.contrib import admin
from .models import Photo, Album, Country, City

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_cities')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'latitude', 'longitude')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'get_albums', 'date', 'legend')

admin.site.register(Album, AlbumAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Country)
