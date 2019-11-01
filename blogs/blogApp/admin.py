from django.contrib import admin
from blogApp.models import userModel,journalModel
# Register your models here.

admin.site.register(userModel)
admin.site.register(journalModel)