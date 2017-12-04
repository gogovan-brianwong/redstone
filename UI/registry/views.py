# Create your views here.
import os

from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from harborclient import harborclient

from Infrastructure.public import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class RegistryLogin(View):

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistryLogin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, 'registry_login.html')

    def post(self, request, *args, **kwargs):
        host = 'registry.allbright.local'
        username = request.POST.get('reg_username')
        password = request.POST.get('reg_password')
        h1 = harborclient.HarborClient(host=host, user=username, password=password)
        if h1.login():
            request.session['user'] = h1.user
            request.session['password'] = h1.password
            request.session['session_id'] = h1.session_id

            resp = redirect('/registry/index/')

            return resp
        else:
            error_msg = "Wrong login"
            return render(request, 'registry_login.html', {'error_msg': error_msg })





class RegistryInfo(View):

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistryInfo, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        ack = RegistryHandler(user=request.session['user'], passwd=request.session['password'])
        all_project = ack.fetch_all()


        return render(request, 'registry_index.html', {'data': all_project } )

    def post(self, request, *args, **kwargs):

        return render(request, 'registry_index.html')




class RegistryHandler:

    host='registry.allbright.local'

    def __init__(self, user, passwd):
        self.host = RegistryHandler.host
        self.user = user
        self.passwd = passwd
        self.auth = harborclient.HarborClient(self.host, self.user, self.passwd)


    def fetch_all(self):
        auth = self.auth
        print(auth.get_projects())
        proj_list = []
        for row in  auth.get_projects():
            proj_dict = {}
            proj_dict['project_id'] = row['project_id']
            proj_dict['project_name'] = row['name']
            proj_dict['repo_count'] = row['repo_count']
            proj_dict['creation_time'] = row['creation_time']
            proj_dict['is_public'] = row['public']
            proj_list.append(proj_dict)
        return proj_list

    def delete_one(self):
        pass


    def add_one(self):
        pass


    def fetch_one(self):

        pass









