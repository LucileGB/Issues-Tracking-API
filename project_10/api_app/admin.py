from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Contributor, Project, Issue, Comment
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Personal details', {'fields': ('first_name', 'last_name',
                            'email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1',
            'password2', 'is_staff', 'is_active',)}
            ),
        )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
