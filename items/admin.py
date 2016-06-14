from django.contrib import admin

from items import models

admin.site.register(models.Item)
admin.site.register(models.Category)