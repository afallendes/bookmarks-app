from django import forms

from backend.models import Bookmark, Tag

class BookmarkForm(forms.ModelForm):

    # This custom bookmark form is required to be able to filter tags choices
    # by their corresponding current user. A 'user' value is passed from the
    # create/edit views to the form kwargs.
    # REF: https://forum.djangoproject.com/t/altering-queryset-in-a-field-of-generic-createview-form/4737/7

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') # This needs to be captured before __init__
        super().__init__(*args, **kwargs)
        # Passing user to filter tags
        self.fields['tags'].queryset = Tag.objects.filter(user=user).distinct()

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'favicon', 'comments', 'tags']
