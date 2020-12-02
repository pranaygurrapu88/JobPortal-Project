from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.


class AdminAccount(UserAdmin):
    model = Accounts
    list_display = ("email","first_name","last_name","is_employee","is_employer","is_staff")
    list_filter = ("email","first_name","last_name","is_employee","is_employer")
    search_fields = ("email","first_name","last_name")
    ordering = ("email","first_name")
    readonly_fields = ["date_joined"]

    add_fieldsets = (
        (None,{
            "classes":("wide",),
            "fields":("email","first_name","last_name","password1","password2","is_employee","is_employer","is_active"),
        }),
    )
    fieldsets = (
        (None,{"fields":("email","first_name","last_name","password")}),
        ("Permissions",{"fields":("is_staff","is_active","is_employee","is_employer")}),
    )
admin.site.register(Accounts,AdminAccount)
admin.site.register(Profile)
admin.site.register(Invite)


class BloggingAdmin(admin.ModelAdmin):
    list_display = ["title" , "date"]

admin.site.register(Blogging,BloggingAdmin)