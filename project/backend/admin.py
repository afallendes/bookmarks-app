from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Bookmark, Tag
from .forms import CustomUserCreationForm, CustomUserChangeForm


admin.site.unregister(Group)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'modified_at',)
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'modified_at',)
    prepopulated_fields = {'slug': ('text',)}


# Ref: https://testdriven.io/blog/django-custom-user-model/ 
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
