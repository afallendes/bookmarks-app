from django.urls import path, include

from .views import (
    BookmarkListView,
    BookmarkRecentListView,
    # TagListView,
    BookmarkCreateView,
    BookmarkUpdateView,
    BookmarkDeleteView,
    get_url_metadata
)

app_name = 'frontend'

urlpatterns = [
    path('', BookmarkRecentListView.as_view(), name='bookmarks-recent'), 
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks-list'), 
    path('bookmarks/create/', BookmarkCreateView.as_view(), name='bookmark-create'), 
    path('bookmarks/<pk>/update/', BookmarkUpdateView.as_view(), name='bookmark-update'),
    path('bookmarks/<pk>/delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
    # path('tags/', TagListView.as_view(), name='tags-list'),
    path('helpers/get-url-metadata/', get_url_metadata, name='get-url-metadata'),
]
