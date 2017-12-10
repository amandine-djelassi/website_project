from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo, Album, Country, City

class AlbumPhotoGridView(LoginRequiredMixin, ListView):
    """
        Create a view with all the photos of a specific album
    """
    template_name = 'gallery/photo_grid.html'
    context_object_name = 'album_photo'


    def get_queryset(self):
        """
            Return all the photos
        """
        return Album.objects.filter(slug = self.kwargs['slug'])[0]


class AlbumCityListView(LoginRequiredMixin, ListView):
    """
        Create a view with all the albums of a specific city
    """
    template_name = 'gallery/album_city_list.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        """
            Return all the albums
        """
        city = City.objects.filter(slug = self.kwargs['slug'])[0]
        return Album.objects.filter(city = city).order_by('-title')[:]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumCityListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of the city
        context['city'] = City.objects.filter(slug = self.kwargs['slug'])[0]
        return context

class AllAlbumListView(LoginRequiredMixin, ListView):
    """
        Create a view with all the albums
    """
    template_name = 'gallery/all_album_list.html'
    context_object_name = 'country_list'

    def get_queryset(self):
        """

        """
        return Country.objects.order_by('-name')[:]


class MapView(LoginRequiredMixin, ListView):
    """
        Create a view with all the countries in the db
    """
    template_name = 'gallery/map.html'
    context_object_name = 'country_list'


    def get_queryset(self):
        """
            Return all the countries
        """
        return Country.objects.order_by('-name')[:]
