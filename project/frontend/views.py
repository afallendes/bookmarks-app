from email.mime import text
from string import ascii_uppercase
from django.db import models

from django.db.models import Count, F, fields
from django.views.generic import ListView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from backend.models import CustomUser, Bookmark, Tag


class BaseListView(LoginRequiredMixin, ListView):
    """
    Base class for the following custom list views.
    """
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().order_by('-created_at').filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_new_bookmark_button"] = True
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


class BookmarkUpdateView(LoginRequiredMixin, UpdateView):
    model = Bookmark
    template_name = "frontend/bookmark_update_form.html"
    fields = ['url', 'title', 'comments',  'tags']

    def get_success_url(self):
        return self.request.GET.get('next')


class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Bookmark
    template_name = "frontend/bookmark_confirm_delete.html"

    def get_success_url(self):
        return self.request.GET.get('next')


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    template_name = "frontend/bookmark_create_form.html"
    fields = ('url', 'title', 'comments', 'tags',)
    success_url = reverse_lazy('frontend:bookmarks-list')

    extra_tags = None

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        if 'data' in form_kwargs:
            data = form_kwargs['data'].copy()
            
            # Capture new tags passed from form 'extra-tags' field
            extras = {}
            for _ in data.getlist('extra-tags'):
                k, v = _.split('|')
                k = k[2:] # remove '**' helper at the start of the string
                extras.update({k: v})
            self.extra_tags = extras
            
            # Remove already captured extra-tags from the 'tags' data. This
            # is to allow the form instance to properly passed as valid. Any 
            # options that are not part of the original options will make
            # validation fail.
            pks = []
            for _ in data.getlist('tags'):
                if not _.startswith('**'):
                    pks.append(_)
            
            data.setlist('tags', pks)

            form_kwargs['data'] = data
        return form_kwargs


    def form_valid(self, form):
        user = self.request.user
        
        form.instance.user = user

        # need to run form_valid() first to create/save form instance, and then
        # attach the extra tags. This is required due to m-2-m implementation.
        # REF: https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        
        form_valid_return = super().form_valid(form)

        bookmark = self.object # tried with get_object() but didn't work
        extra_tags = self.extra_tags
        if extra_tags:
            for slug, text  in extra_tags.items():
                tag = Tag.objects.create(user=bookmark.user, slug=slug, text=text)
                bookmark.tags.add(tag)
        
        return form_valid_return
    
    