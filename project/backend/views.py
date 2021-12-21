from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import CustomUser, Bookmark, Tag
from .serializers import BookmarkSerializer, TagSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    List all bookmarks and perform CRUD operations.
    """

    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.all().filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    List all tags and perform CRUD operations.
    """

    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all().filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListBookmarksByTagView(generics.RetrieveAPIView):
    """
    List all bookmarks with specified tag.
    """

    serializer_class = BookmarkSerializer

    lookup_field = 'tags__pk'

    def get_queryset(self):
        return Bookmark.objects.all().filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Overwritten to retrieve more than one filtered instances."""

        queryset = self.get_queryset().filter(**kwargs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    