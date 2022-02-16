from string import ascii_uppercase

from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView,UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from backend.models import CustomUser, Bookmark, Tag
from frontend.forms import BookmarkForm
from frontend.utils import get_url_title, get_url_favicon


# Base config classes with custom methods and attr based on mixins

class BaseConfig(LoginRequiredMixin):
    enable_create_bookmark_btn = False
    
    def get_enable_create_bookmark_btn(self):
        # Helper for templates to indicate if the New Bookmark button should be rendered.
        if hasattr(self, 'enable_create_bookmark_btn'):
            return self.enable_create_bookmark_btn
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_create_bookmark_btn"] = self.get_enable_create_bookmark_btn()
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BookmarkConfig(BaseConfig):
    model = Bookmark
    enable_create_bookmark_btn = True


class CreateUpdateBookmarkConfig(BookmarkConfig):
    form_class = BookmarkForm

    def get_success_url(self):
        return self.request.GET.get('origin').replace('#bookmark-form', '')
    
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs['user'] = self.request.user # To help the bookmark form filter tags by user

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
        form.instance.user = self.request.user

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


class TagConfig(BaseConfig):
    model = Tag
    enable_create_bookmark_btn = False


# Bookmark views based on config classes

class ListBookmarkView(BookmarkConfig, ListView):
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


class ListRecentBookmarkView(BookmarkConfig, ListView):
    template_name = "frontend/bookmarks_recent.html"
    context_object_name = 'bookmarks'
    most_recent_items = 5

    def get_most_recent_items(self):
        if hasattr(self, 'most_recent_items'):
            return self.most_recent_items
        return 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')[:self.get_most_recent_items()]


class CreateBookmarkView(CreateUpdateBookmarkConfig, CreateView):
    template_name = "frontend/bookmark_create_form.html"


class UpdateBookmarkView(CreateUpdateBookmarkConfig, UpdateView):
    template_name = "frontend/bookmark_update_form.html"
    

class DeleteBookmarkView(BookmarkConfig, DeleteView):
    template_name = "frontend/bookmark_confirm_delete.html"

    def get_success_url(self):
        return self.request.GET.get('origin')


# Tag views based on config classes

class ListTagView(TagConfig, ListView):
    template_name = "frontend/tags.html"
    context_object_name = 'tags_grouped_by_letter'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            count=Count('bookmarks'),
        )
        return [{
            'letter': _,
            'tags': queryset.filter(slug__istartswith=_)
        } for _ in ascii_uppercase ]


class UpdateTagView(TagConfig, UpdateView):
    template_name = "frontend/tag_update_form.html"
    fields = ['text', ]

    def get_success_url(self):
        return self.request.GET.get('origin')


class DeleteTagView(TagConfig, DeleteView):
    template_name = "frontend/tag_confirm_delete.html"

    def get_success_url(self):
        return self.request.GET.get('origin')


# Helper views for specific interactions

@login_required
@require_GET
def get_url_metadata(request):
    """
    View to capture metadata from the url provided as GET param.
    Returns metadata as JSON object with 'title' and 'icon' as attrs.
    """

    url = request.GET.get('url')

    metadata = {
        'title': get_url_title(url),
        'favicon': get_url_favicon(url)
    }

    return JsonResponse(metadata)
