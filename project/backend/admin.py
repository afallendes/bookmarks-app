from django.contrib import admin
from backend.models import Bookmark, Tag


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

