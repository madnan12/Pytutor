from django.contrib import admin
from .models import CustomUser

# Actions for CustomUser Model admin panel
@admin.action(description='Deactive selected user accounts')
def deactivate_account(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = False
        user.save()
        
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'user_type', 'last_login', 'is_active')
	list_filter = ('user_type', 'is_active')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	actions = [deactivate_account]

admin.site.register(CustomUser, CustomUserAdmin)
