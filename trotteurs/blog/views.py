from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, Tag

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        """
            Return the last published articles
        """
        return Article.objects.order_by('-date')[:]


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context


class DetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context

class TagView(LoginRequiredMixin, ListView):
    template_name = 'blog/result_list.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        """
            Return the articles, with the given tag
        """
        tags = Tag.objects.filter(slug = self.kwargs['slug'])
        return Article.objects.filter(tags = tags)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TagView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context

class ArticleYearArchiveView(LoginRequiredMixin, YearArchiveView):
    template_name = 'blog/result_list.html'
    context_object_name = 'article_list'

    queryset = Article.objects.all()
    date_field = "date"
    make_object_list = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleYearArchiveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context


class ArticleMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    template_name = 'blog/result_list.html'
    context_object_name = 'article_list'

    queryset = Article.objects.all()
    date_field = "date"
    make_object_list = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleMonthArchiveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context


################################################################################
#                               Static pages                                   #
################################################################################

class StaticView(TemplateView):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StaticView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags_list'] = Tag.objects.all()

        # Archive part
        archive = {}
        date_field = 'date'
        years =  Article.objects.dates(date_field, 'year')[::-1]
        for date_year in years:
            months = Article.objects.filter(date__year=date_year.year).dates(date_field, 'month')
            archive[date_year] = months

        archive = sorted(archive.items(), reverse=True)
        context['archive'] = archive

        return context

class AboutView(StaticView):
    template_name = "blog/about.html"

class ContactView(StaticView):
    template_name = "blog/contact.html"
