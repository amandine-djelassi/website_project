"""trotteurs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Administration page
    url(r'^admin/', admin.site.urls),
    # Access to the blog part
    url(r'^blog/', include('blog.urls')),
    # Pretty editor for the admin part
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #Add Django site authentication urls (for login, logout, password management)
    url('^accounts/', include('django.contrib.auth.urls')),
    # url('^accounts/', include('registration.backends.default.urls')),
    url('^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', \
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
    # Access to the profile
    url('^profile/$', views.ProfileView.as_view(), name="profile"),
    # Static files
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    # Home of the website
    url(r'^$', views.IndexView.as_view(), name='home')
]
# Add static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
