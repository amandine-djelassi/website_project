from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo, Album, Country, City

class AlbumPhotoGridView(LoginRequiredMixin, ListView):
    template_name = 'gallery/photo_grid.html'
    context_object_name = 'album_photo'


    def get_queryset(self):
        """
            Return all the photos
        """
        return Album.objects.filter(slug = self.kwargs['slug'])[0]


class AlbumListView(LoginRequiredMixin, ListView):
    template_name = 'gallery/album_list.html'
    context_object_name = 'album_list'


    def get_queryset(self):
        """
            Return all the albums
        """
        city = City.objects.filter(slug = self.kwargs['slug'])[0]
        return Album.objects.filter(city = city).order_by('-title')[:]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of the city
        context['city'] = City.objects.filter(slug = self.kwargs['slug'])[0]
        return context

class MapView(LoginRequiredMixin, ListView):
    template_name = 'gallery/map.html'
    context_object_name = 'country_list'


    def get_queryset(self):
        """
            Return all the countries
        """
        return Country.objects.order_by('-name')[:]
