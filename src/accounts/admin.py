from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.sites.models import Site
# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display_links = ['email']
    readonly_fields = ["date_joined", 'last_login']
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id', 'email', 'phone', 'user_type']
    list_filter = ['user_type']
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'country_code', 'phone', 'password')}
         ),
        ('Autherization', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}
         ),
        ('Status', {
            'fields': ('is_email_varified', 'is_phone_varified',)}
         ),
        ('Timeline', {
            'fields': ('date_joined', 'last_login',)}
         ),

    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', ('country_code', 'phone'), 'password')}
         ),
        ('Autherization', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}
         ),
        ('Status', {
            'fields': ('is_email_varified', 'is_phone_varified',)}
         ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


models = apps.get_models()
#admin.site.unregister(Site)
for model in models:
    try:
        #print('count register :'+str(model))
        admin.site.register(model)
    except:
        #print('count non register : '+str(model))
        pass
        
