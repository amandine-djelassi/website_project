from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^about', TemplateView.as_view(template_name='blog/about.html'), name='about'),
    url(r'^contact', TemplateView.as_view(template_name='blog/contact.html'), name='contact'),
]
