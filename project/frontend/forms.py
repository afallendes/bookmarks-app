from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
        required=True,
        min_length=1,
        max_length=50
    )
