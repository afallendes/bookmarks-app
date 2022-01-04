from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import BookmarkViewSet, TagViewSet, ListBookmarksByTagView

app_name = 'backend'

router = SimpleRouter()
router.register('bookmarks', BookmarkViewSet, basename='bookmarks')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'bookmarks/tag/<int:tags__pk>/',
        ListBookmarksByTagView.as_view(),
        name='bookmarks-by-tag'
    ),
]
