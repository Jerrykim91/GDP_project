from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import LIST

# Register your models here.

admin.site.register(LIST, UserAdmin)