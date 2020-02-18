from django.contrib import admin

from businesses import models

admin.site.register(models.Business)
admin.site.register(models.UserProfile)
