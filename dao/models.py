from django.db import models

class UserGroups(models.Model):
    grouptype = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.grouptype)


class UserDetails(models.Model):  # Mysql DB connection
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10, default=None)
    age = models.IntegerField(default=None)
    position = models.CharField(max_length=20, null=True)
    group_type = models.ForeignKey(UserGroups)


    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.username, self.password, self.email, self.gender, self.age,
                                          self.position)


# Create your models here.




class AppType(models.Model):
    typename = models.CharField(max_length=30, default=None)



    def fetch_all(self):
        obj = self.__class__.objects.all()
        return obj

    def __str__(self):
        return '{}'.format(self.typename)


class AppVersion(models.Model):
    appversion = models.CharField(max_length=20)



    def __str__(self):
        return '{}'.format(self.appversion)


class AppImage(models.Model):
    imagename = models.CharField(max_length=20)
    # app_version = models.ForeignKey(AppVersion)
    all_appversions = models.ManyToManyField(AppVersion, blank=True)

    def __str__(self):
        return '{}'.format(self.imagename)



class AppRepository(models.Model):
    name = models.CharField(max_length=60)
    apprepository = models.CharField(max_length=100)
    app_image = models.ForeignKey(AppImage)

    def __str__(self):
        return '{}'.format(self.apprepository)


class AppDeployOption(models.Model):
    name = models.CharField(max_length=32, default=None)
    basic_tab = models.BooleanField(default=True)
    account_tab = models.BooleanField(default=True)
    policy_tab = models.BooleanField(default=True)
    app_persist_tab = models.BooleanField(default=True)
    db_persist_tab = models.BooleanField(default=True)
    resources_tab = models.BooleanField(default=True)
    ingress_tab = models.BooleanField(default=True)
    custom_tab = models.BooleanField(default=True)


    def __str__(self):
        return '{} {} {} {} {} {} {} {}'.format(self.basic_tab, self.account_tab, self.policy_tab, self.app_persist_tab,
                                             self.db_persist_tab, self.resources_tab, self.ingress_tab, self.custom_tab)

class AppName(models.Model):
    appname = models.CharField(max_length=32)
    appdetails = models.CharField(max_length=1000)
    thumbnail_path = models.CharField(max_length=60, default=None)
    template_path = models.CharField(max_length=50, default=None)
    rendered_path = models.CharField(max_length=50, default=None)
    custom_tab_html = models.CharField(max_length=60, default='/templates/application/custom_tab')
    helm_repo = models.CharField(max_length=32, default=None)
    all_apptypes = models.ManyToManyField(AppType, blank=True)
    app_repository = models.ForeignKey(AppRepository, default=1)
    app_deployoption = models.ForeignKey(AppDeployOption, default=1)

    def fetch_all(self):
        obj = self.__class__.objects.all()
        return obj

    def fetch_by_id(self,app_id):
        obj = self.__class__.objects.filter(id=app_id).distinct()
        return obj

    def fetch_value_by_id(self, app_id, values):

        obj = self.__class__.objects.filter(id=app_id).all().values(values)
        return obj

    def fetch_apptype(self, select_apptype):
        obj =  self.__class__.objects.filter(all_apptypes=select_apptype)
        return obj

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.appname, self.appdetails, self.thumbnail_path, self.template_path, self.rendered_path, self.custom_tab_html, self.helm_repo)








