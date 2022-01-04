from string import ascii_uppercase
from django.db import models

from django.db.models import Count, F, fields
from django.views.generic import ListView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from backend.models import CustomUser, Bookmark, Tag
from frontend.forms import SearchForm


class BaseListView(LoginRequiredMixin, ListView):
    """
    Base class for the following custom list views.
    """
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().order_by('-created_at').filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(label_suffix='')
        return context


class BookmarkListView(BaseListView):
    """
    List bookmarks sorted by created_at and paginated.
    If a 'search' or 'tag' GET param is passed the queryset is filtered.
    """

    model = Bookmark
    template_name = "frontend/bookmarks.html"
    context_object_name = 'bookmarks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        if 'search' in self.request.GET:
            return queryset.filter(title__icontains=self.request.GET['search'])
        if 'tag' in self.request.GET:
            return queryset.filter(tags__slug=self.request.GET['tag'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_param': self.request.GET.get('search'),
            'tag_param': self.request.GET.get('search'),
        })
        return context


class BookmarkRecentListView(BaseListView):
    """
    List the most recent bookmarks sorted by created_at.
    By default it lists last 5.
    """

    model = Bookmark
    template_name = "frontend/bookmarks_recent.html"
    context_object_name = 'bookmarks'
    recent_items_num = 5

    def get_recent_items_num(self):
        return self.recent_items_num
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset[:self.get_recent_items_num()]


# class TagListView(BaseListView):
#     model = Tag
#     context_object_name = 'letters'
#     template_name = 'frontend/tags.html'

#     def get_queryset(self):
#         queryset = super().get_queryset().annotate(
#             count=Count('bookmarks'),
#         )
#         return { _:queryset.filter(slug__istartswith=_) for _ in ascii_uppercase }


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    template_name = "frontend/bookmark_update_form.html"
    fields = ['title', 'url', 'tags']

    def get_success_url(self):
        return self.request.get_full_path()


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    template_name = "frontend/bookmark_confirm_delete.html"

    def get_success_url(self):
        return self.request.GET.get('next')


class BookmarkCreateView(CreateView):
    model = Bookmark
    template_name = "frontend/bookmark_create_form.html"
    fields = ('title', 'url', 'tags',)
    success_url = reverse_lazy('frontend:bookmarks-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
