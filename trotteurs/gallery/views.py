from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'photo_list'


    def get_queryset(self):
        """
            Return the last published articles
        """
        return Photo.objects.order_by('-date')[:]
