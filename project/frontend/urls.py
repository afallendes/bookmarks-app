from django.urls import path, include

from .views import (
    BookmarkListView,
    BookmarkRecentListView,
    # TagListView
)

app_name = 'frontend'

urlpatterns = [
    path('', BookmarkRecentListView.as_view(), name='bookmarks-recent'), 
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks-list'), 
    # path('tags/', TagListView.as_view(), name='tags-list'), 
]
