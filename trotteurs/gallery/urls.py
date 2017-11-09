from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^album/(?P<slug>[\w-]+)/$', views.AlbumPhotoGridView.as_view(), name='album_photo_grid'),
    url(r'^city/(?P<slug>[\w-]+)/$', views.AlbumListView.as_view(), name='album_list'),
    url(r'^$', views.MapView.as_view(), name='map')
]
