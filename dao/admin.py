from django.contrib import admin
from . import models
from dao.models import AppName, AppDeployOption, AppType, AppImage, UserGroups, UserDetails, AppRepository, AppVersion
# Register your models here.

admin.site.register(models.AppName)
admin.site.register(models.AppDeployOption)
admin.site.register(models.AppType)
admin.site.register(models.AppImage)
admin.site.register(models.AppRepository)
admin.site.register(models.AppVersion)
admin.site.register(models.UserDetails)
admin.site.register(models.UserGroups)
