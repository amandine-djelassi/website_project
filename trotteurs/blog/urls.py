from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tag/(?P<slug>[\w-]+)/$', views.TagView.as_view(), name='tag_list'),
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.ArticleYearArchiveView.as_view(), name="article_year_archive"),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', views.ArticleMonthArchiveView.as_view(month_format='%m'), name="article_month_archive"),
    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(), name='detail'),
]
