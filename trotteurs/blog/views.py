from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin
from django.urls import reverse
from .models import Article, Tag
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from trotteurs.views import LastVisitMixin

class IndexView(LastVisitMixin, LoginRequiredMixin, ListView):
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


class DetailView(LastVisitMixin, LoginRequiredMixin, FormMixin, DetailView):
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
        context['comments'] = Comment.objects.filter_by_instance(self.object)

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
        self.object = self.get_object()
        instance = get_object_or_404(Article, slug=self.object.slug)
        form = CommentForm(request.POST or None)#, initial=initial_data)
        if form.is_valid():

            c_type = form.cleaned_data.get("content_type").lower()
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id= parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    parent_obj = parent_qs.first()
            new_comment, created = Comment.objects.get_or_create(
                user = request.user,
                content_type = content_type,
                object_id = obj_id,
                content = content_data,
                parent = parent_obj,
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        self.object = self.get_object()
        instance = get_object_or_404(Article, slug=self.object.slug)
        initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id,
        }

        return initial_data

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super(DetailView, self).form_valid(form)

class TagView(LastVisitMixin, LoginRequiredMixin, ListView):
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

class ArticleYearArchiveView(LastVisitMixin, LoginRequiredMixin, YearArchiveView):
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


class ArticleMonthArchiveView(LastVisitMixin, LoginRequiredMixin, MonthArchiveView):
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

def delete_comment(request, article_slug, comment_pk):
    p = Comment.objects.get(pk=comment_pk)
    p.children().delete()
    p.delete()
    return HttpResponseRedirect(reverse('blog:detail', args=(article_slug,)))
