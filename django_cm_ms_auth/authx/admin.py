from django.contrib import admin
from django.contrib.auth.models import Group, Site
from .models import CustomUser

admin.site.unregister(CustomUser)
admin.site.unregister(Group)
admin.site.unregister(Site)
