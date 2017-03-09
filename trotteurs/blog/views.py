from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Article

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        """
            Return the last five published articles
        """
        return Article.objects.order_by('-date')[:5]

class DetailView(generic.DetailView):
    """
    """
    model = Article
    template_name = 'blog/detail.html'
