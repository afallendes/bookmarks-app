from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

# Ref: https://testdriven.io/blog/django-custom-user-model/
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
