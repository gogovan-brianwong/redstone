from django.contrib import admin

from dao import models as m

admin.site.register(m.UserGroups)
admin.site.register(m.UserDetails)
admin.site.register(m.AppName)
admin.site.register(m.AppImage)
admin.site.register(m.AppType)
admin.site.register(m.AppRepository)
admin.site.register(m.AppVersion)
admin.site.register(m.AppDeployOption)


