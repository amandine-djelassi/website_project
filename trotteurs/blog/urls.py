from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tag/(?P<slug>[\w-]+)/$', views.TagView.as_view(), name='tag_list'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.ArticleYearArchiveView.as_view(), name="article_year_archive"),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', views.ArticleMonthArchiveView.as_view(month_format='%m'), name="article_month_archive"),
    url(r'^(?P<article_slug>[\w-]+)/(?P<comment_pk>[0-9]+)/delete_comment/$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(), name='detail'),
]
