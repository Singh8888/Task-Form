from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'first_name','last_name', 'is_admin')
    list_filter = ('email',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name','last_name','email')
        }),
        ('Advanced options', {
            'fields': ('is_active',),
        }),
        ('Sensitive Information', {
            'fields': ('password',),
        }),
    )
    
admin.site.register(User,UserAdmin)
