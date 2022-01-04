from django.urls import path, include

from .views import (
    BookmarkListView,
    BookmarkRecentListView,
    # TagListView,
    BookmarkUpdateView,
    BookmarkDeleteView,
)

app_name = 'frontend'

urlpatterns = [
    path('', BookmarkRecentListView.as_view(), name='bookmarks-recent'), 
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks-list'), 
    path('bookmarks/<pk>/update/', BookmarkUpdateView.as_view(), name='bookmark-update'),
    path('bookmarks/<pk>/delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
    # path('tags/', TagListView.as_view(), name='tags-list'), 
]
