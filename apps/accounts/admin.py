from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Group, Worker
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'is_user_active',
                    'created_date')
    date_hierarchy = 'created_date'
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        ("Personal Datas", {"fields": ('first_name', 'last_name', 'avatar')}),
        ("Permissions", {"fields": ('is_active', 'is_staff', 'is_user_active', 'is_superuser', 'groups',)}),
        ("Imported Dates", {"fields": ('last_login', 'modified_date', 'created_date')})
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ('last_login', 'modified_date', 'created_date')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    filter_horizontal = ()
    list_editable = ('is_active', 'is_staff', 'is_superuser', 'is_user_active')
    ordering = ()


class GroupAdmin(TranslationAdmin):
    model = Group
    list_display = ('id',)
    date_hierarchy = 'created_date'
