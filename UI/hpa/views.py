import json

from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, HttpResponse

from Infrastructure.public import check_login
from Infrastructure.public import getAllNamespaces
from corelogic.hpa.alertbox import *
from corelogic.hpa.views import *


@check_login
def index(request):
    return render(request, 'hpa_index.html', {'all_namespaces': getAllNamespaces() })


@check_login
def add_hpa(request):
    if request.method == 'POST':
        inputData = request.POST.get('input_data')
        return HttpResponse(json.dumps({'data': addHPA(inputData)}))

@check_login
def select_ns(request):
    if request.method == 'POST':
        selectData = request.POST.get('namespace')
        return HttpResponse(json.dumps({'data': selectNS(selectData) }))

@check_login
def show_all(request):
    if request.method == 'GET':

        return HttpResponse(json.dumps({'data': showAllHPA() }))
    if request.method == 'POST':
        select = request.POST.get('namespace')
        return HttpResponse(json.dumps({'data': showNamespacedHPA(select)}))

@check_login
def remove_hpa(request):
    if request.method == 'GET':
        redirect('/hpa/index/')
    if request.method == 'POST':
        selected_hpa = request.POST.get('hpa')
        selected_ns = request.POST.get('ns')
        return HttpResponse(json.dumps({'data': removeHPA(selected_hpa, selected_ns) }))

@check_login
def getresources(request):
    if request.method == 'POST':
        select_hpa = request.POST.get('hpa')
        select_ns = request.POST.get('ns')
        return HttpResponse(json.dumps({'data': getSpecifiedSvc(select_hpa, select_ns)}))



@check_login
def alertbox(request):

    resp = StreamingHttpResponse(streaming_content=(stream_generator()),content_type="text/event-stream")
    resp['Cache-Control'] = 'no-cache'
    return resp

@check_login
def tableupdate(request):

    if request.method == 'POST':
        select_row = json.loads(request.POST.get('content'))
        return HttpResponse(json.dumps({'data': updateTableField(**select_row)}))
