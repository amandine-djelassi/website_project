from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin
from django.urls import reverse

from .models import Article, Tag, Comment

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    paginate_by = 10

    def get_queryset(self):
        """
            Return the last published articles
        """
        return Article.objects.order_by('-date')[:]


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags'] = Tag.objects.all()

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


class DetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Article
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags'] = Tag.objects.all
        # add of the form
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.order_by('-created_date')

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

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            article = get_object_or_404(Article, slug=self.object.slug)
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return self.form_valid(comment)
        else:
            return self.form_invalid(comment)

    def form_valid(self, comment):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super(DetailView, self).form_valid(comment)

class TagView(LoginRequiredMixin, ListView):
    template_name = 'blog/result_list.html'
    context_object_name = 'article_list'
    paginate_by = 10

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
        context['tags'] = Tag.objects.all()

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

    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleYearArchiveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags'] = Tag.objects.all()

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

    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleMonthArchiveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tags'] = Tag.objects.all()

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
from django.http import HttpResponseRedirect
def delete_comment(request, article_slug, comment_pk):
    p = Comment.objects.get(pk=comment_pk)
    p.delete()
    return HttpResponseRedirect(reverse('blog:detail', args=(article_slug,)))
def reply_comment(request, article_slug, comment_pk):
    article = get_object_or_404(Article, slug=self.object.slug)
    comment = form.save(commit=False)
    comment.article = article
    comment.parent = comment_pk
    comment.save()
    return self.form_valid(comment)

    p = Comment.objects.get(pk=comment_pk)
    p.delete()
    return HttpResponseRedirect(reverse('blog:detail', args=(article_slug,)))
