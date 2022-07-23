from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from django.core.exceptions import BadRequest, PermissionDenied
from .models import Article, Section, Status

class ArticleNavbarHelper:
    def __init__(self, context):
        self.set_sections(context)
        self.set_statuses(context)

    def set_sections(self, context):
        context["sections"] = Section.objects.all()

    def set_statuses(self, context):
        context["statuses"] = Status.objects.all()

class ArticleListView(LoginRequiredMixin, ListView):
    template_name = "articles/list.html"
    model = Article

    def get_article_list_context(self, context, section, status):
        context["article_list"] = Article.objects.filter(
                section=section
            ).filter(
                status=status
            ).order_by("created_on").reverse()
        return context


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_id = self.kwargs.get("status")
        section_id = self.kwargs.get("section")
        status = Status.objects.get(id=status_id)
        section = Section.objects.get(id=section_id)
        ArticleNavbarHelper(context)
        if status.id == 1: #id1 is published
            return self.get_article_list_context(context, section, status)
        if self.request.user.role.id > 1:
            return self.get_article_list_context(context, section, status)
        raise PermissionDenied("You are not authorized to view this page.")


class ArticleDraftListView(LoginRequiredMixin, ListView):
    template_name = "articles/list.html"
    model = Article


class ArticleDetailView(DetailView): 
    template_name = "articles/detail.html"
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "articles/new.html"
    model = Article
    fields = ["title", "subtitle", "body", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user #this line of code is populating the author line with the user that is currently logged in.
        if form.instance.status == "published":
            raise BadRequest("You are not authorized to publish; Request a review first.")
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "articles/edit.html"
    model = Article
    fields = ['title', 'subtitle', 'body', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user #this line of code is populating the author line with the user that is currently logged in.
        if form.instance.status == "published":
            raise BadRequest("You are not authorized to publish; Request a review first.")
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "articles/delete.html"
    model = Article
    success_url = reverse_lazy("articles_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user