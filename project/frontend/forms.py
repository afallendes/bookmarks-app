from django import forms

from backend.models import Bookmark, Tag

class BookmarkForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(user=user).distinct()

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'comments', 'tags']
