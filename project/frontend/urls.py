from django.urls import path, include

from .views import (
    DeleteTagView,
    ListBookmarkView,
    ListRecentBookmarkView,
    CreateBookmarkView,
    UpdateBookmarkView,
    DeleteBookmarkView,
    ListTagView,
    UpdateTagView,
    DeleteTagView,
    get_url_metadata
)

app_name = 'frontend'

urlpatterns = [
    path('', ListRecentBookmarkView.as_view(), name='bookmarks-recent'), 
    path('bookmarks/', ListBookmarkView.as_view(), name='bookmarks-list'), 
    path('bookmarks/create/', CreateBookmarkView.as_view(), name='bookmark-create'), 
    path('bookmarks/<pk>/update/', UpdateBookmarkView.as_view(), name='bookmark-update'),
    path('bookmarks/<pk>/delete/', DeleteBookmarkView.as_view(), name='bookmark-delete'),
    path('tags/', ListTagView.as_view(), name='tags-list'), 
    path('tags/<pk>/update/', UpdateTagView.as_view(), name='tag-update'),
    path('tags/<pk>/delete/', DeleteTagView.as_view(), name='tag-delete'),
    path('helpers/get-url-metadata/', get_url_metadata, name='get-url-metadata'),
]
