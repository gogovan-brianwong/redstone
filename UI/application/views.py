from Infrastructure.public import *
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from Infrastructure.public import *
from django.utils.decorators import method_decorator
from application.Config import accessMode, ingressAnnotations, wordpress_default_info
from application.views import AppOptionsHandler, AppDetailsHandler, AppIndexHandler


class AppIndexPorter(View):

    # Login required decorator
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(AppIndexPorter, self).dispatch(request, *args, **kwargs)

    # Get All apps availabled in repository
    def get(self, request, *args, **kwargs):
    #
    #     # instantiate AppIndexHandler
        instance = AppIndexHandler()
    #     # If no url parameter attached with URL, all apps availabled app in repo will be shown.
    #         # Call instanced class to fetch all apps
        result = instance.fetch_all_apps()
    #
        return render(request, 'app_index.html', result )

    # If it's POST method to request, call instanced class AppIndexHandler's fetch_specific method.
    def post(self, request, *args, **kwargs):
        mimetype = 'application/json'
        select_apptype = request.POST.get('data')
        instance = AppIndexHandler()
        result = instance.fetch_specific_apptype(select_apptype=select_apptype)
        return HttpResponse(json.dumps(result), mimetype)


class AppDetailsPorter(View):

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(AppDetailsPorter, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        mimetype = 'application/json'
        select_app_id = args[0]
        instance = AppDetailsHandler()
        ret = instance.fetch_app_by_one(appid=select_app_id)
        return HttpResponse(json.dumps(ret), mimetype)

    # Deploy app's request
    def post(self, request, *args, **kwargs):
        body_deploy_options = {}
        body_ingress_annote = {}
        select_app_id = args[0]
        body_basic = json.loads(request.POST.get('basic_frm'))
        body_account = json.loads(request.POST.get('account_frm'))
        body_app_storage = json.loads(request.POST.get('app_storage_frm'))
        body_db_storage = json.loads(request.POST.get('db_storage_frm'))
        body_resource = json.loads(request.POST.get('resource_frm'))
        body_ingress = json.loads(request.POST.get('ingress_frm'))
        body_custom = json.loads(request.POST.get('custom_frm'))
        body_custom['select_app'] = request.POST.get('select_appname')

        if request.POST.get('ingress_annote') == 'None':
            body_ingress_annote['ingress_annotations'] = ingressAnnotations
        else:
            body_ingress_annote['ingress_annotations'] = json.loads(request.POST.get('ingress_annote'))
        deploy_list = [ body_basic, body_account, body_app_storage, body_db_storage, body_resource, body_ingress,
                       wordpress_default_info, body_ingress_annote, body_custom ]
        instance = AppDetailsHandler()
        ret = instance.deploy_app(app_id=select_app_id,deploy_list=deploy_list)
        return HttpResponse(json.dumps(ret))



@check_login
def fetchSpecificApp(request, *args, **kwargs):
    appUID = args[0]
    instance = AppDetailsHandler()
    response = {'status': True, 'message': '', 'data': ''}
    try:

        ret = instance.fetch_specific_app(identifier=appUID)
        response['status'] = True
        response['data'] = ret
        return HttpResponse(json.dumps(response))

    except Exception as e:
        response['status'] = False
        response['message'] = e
        return HttpResponse(json.dumps(response))


@check_login
def deleteApp(request):

    req = request.POST.get('select_app', None)
    app_name = req.split('-')[0]
    instance = AppDetailsHandler()
    ret = instance.delete_app(app_name=app_name)
    return HttpResponse(json.dumps(ret))

@check_login
def searchApp(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'app_index.html')

    elif request.method == 'POST':
        mimetype = 'application/json'
        input_string = request.POST.get('data') # key-value {'data': 'input_data'}
        instance = AppIndexHandler()
        result = instance.search_app(input_string=input_string)
        return HttpResponse(json.dumps(result), mimetype)



@check_login
def listNamespacedSecret(request):

    select_namespace = request.POST.get('data')
    response = {'status': False, 'data': '', 'message': ''}

    try:
        api_instance = AppOptionsHandler()
        result = api_instance.list_namespaced_secret(namespace=select_namespace)
        response['data'] = result
        response['status'] = True
    except ApiException as e:
        response['status'] = False
        response['message'] = e

    return HttpResponse(json.dumps(response))

@check_login
def fetchApptype(request):
    instance = AppDetailsHandler()
    ret = instance.fetch_apptype()

    return HttpResponse(json.dumps(ret))

@check_login
def listSCResources(request):
    ret_sc = AppOptionsHandler()
    data = ret_sc.list_storage_class
    return HttpResponse(json.dumps({ 'resource_sc': data, 'access_mode': [ { 'mode': x } for x in accessMode ]}))


@check_login
def allDeployedApp(request):

    mimetype = 'application/json'
    if request.method == 'GET':

        try:
            ret = AppOptionsHandler()
            data = ret.list_deployment_for_all_namespaces # Call instanced AppOptionsHandler class's list_deployment_for_all_namespaces method.
            return HttpResponse(json.dumps(data, cls=JsonCustomSerializer), mimetype)

        except ApiException as e:

            return HttpResponse(json.dumps({'data': '', 'message': e }))


