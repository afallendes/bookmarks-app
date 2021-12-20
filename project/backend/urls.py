from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import BookmarkViewSet, TagViewSet, ListBookmarksByTagView

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
