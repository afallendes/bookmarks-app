from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(verbose_name='URL', max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return self.title[:80]
    

class Tag(models.Model):
    slug = models.SlugField(unique=True)
    bookmarks = models.ManyToManyField(Bookmark)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug
