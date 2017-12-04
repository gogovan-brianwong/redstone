from __future__ import print_function
import kubernetes
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from pprint import pprint
import os, time, datetime, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.load_kube_config(os.path.join(BASE_DIR, '../assets/certs', 'kubeconfig-dev.yaml'))

kind = 'deployment'

def showAllHPA():
    # Configure API key authorization: BearerToken
    # kubernetes.client.configuration.api_key['authorization'] = 'YOUR_API_KEY'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = kubernetes.client.AutoscalingV1Api()
    field_selector = 'field_selector_example'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)
    resp_list = []
    try:
        api_response = api_instance.list_horizontal_pod_autoscaler_for_all_namespaces(pretty=pretty,
                                                                                      timeout_seconds=timeout_seconds)

        for row in api_response.items:
            resp_dict = {}
            resp_dict['apiVersion'] = api_response.api_version
            resp_dict['kind'] = api_response.kind
            # resp_dict['annotations'] = row.metadata.annotations.keys
            resp_dict['created_at'] = str(row.metadata.creation_timestamp)
            resp_dict['name'] = row.metadata.name
            resp_dict['namespace'] = row.metadata.namespace
            resp_dict['uid'] = row.metadata.uid
            resp_dict['max_replicas'] = row.spec.max_replicas
            resp_dict['min_replicas'] = row.spec.min_replicas
            resp_dict['target_ref'] = row.spec.scale_target_ref.name
            resp_dict['CPU_Util_percent'] = row.spec.target_cpu_utilization_percentage
            resp_dict['current_CPU_util_percent'] = row.status.current_cpu_utilization_percentage
            resp_dict['current_replicas'] = row.status.current_replicas
            resp_dict['desired_replicas'] = row.status.desired_replicas
            resp_dict['action'] = None

            resp_list.append(resp_dict)
        return resp_list

    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->list_horizontal_pod_autoscaler_for_all_namespaces: %s\n" % e)


def showNamespacedHPA(*args, **kwargs):
    api_instance = kubernetes.client.AutoscalingV1Api()
    namespace = args[0]  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    field_selector = 'field_selector_example'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_namespaced_horizontal_pod_autoscaler(namespace, pretty=pretty,
                                                                              include_uninitialized=include_uninitialized,
                                                                              timeout_seconds=timeout_seconds,
                                                                              watch=watch)
        resp_list = []

        for row in api_response.items:
            resp_dict = {}
            resp_dict['name'] = row.metadata.name
            resp_dict['uid'] = row.metadata.uid
            resp_list.append(resp_dict)
        return resp_list


    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->list_namespaced_horizontal_pod_autoscaler: %s\n" % e)


def addHPA(rev_data):

    optDict = {}
    for i in rev_data.split('&'):
        temp = i.split('=')
        opt = {temp[0]: temp[1].strip()}
        optDict.update(opt)
    # print(optDict)
    api_instance = client.AutoscalingV1Api()
    hpa_target_ref = client.V1CrossVersionObjectReference(name=optDict['current_hpa_deployment'], kind=kind)
    hpa_spec = client.V1HorizontalPodAutoscalerSpec(max_replicas=optDict['hpa_max_qant'],
                                                    scale_target_ref=hpa_target_ref,
                                                    min_replicas=optDict['hpa_min_qant'],
                                                    target_cpu_utilization_percentage=optDict['cpu_threshold'])
    hpa_metadata = client.V1ObjectMeta(name=optDict['current_hpa_deployment'], namespace=optDict['current_ns'])
    hpa_status = client.V1HorizontalPodAutoscalerStatus()
    # hpa_metadata = client.V1ObjectMeta(name=optDict['current_hpa_deployment'], namespace=optDict['current_ns'])
    body = client.V1HorizontalPodAutoscaler(metadata=hpa_metadata, spec=hpa_spec)

    namespace = optDict['current_ns']  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    api_status = {}
    try:
        api_response = api_instance.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=body,
                                                                                pretty=pretty)
        pprint(api_response)

        api_status['current_replicas'] = hpa_status.current_replicas
        api_status['cpu_util'] = hpa_status.current_cpu_utilization_percentage
        api_status['last_scale_time'] = hpa_status.last_scale_time
        api_status['status_code'] = 200

        return api_status
    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->create_namespaced_horizontal_pod_autoscaler: %s\n" % e)


def removeHPA(*args, **kwargs):
    api_instance = kubernetes.client.AutoscalingV1Api()
    name = args[0]  # str | name of the HorizontalPodAutoscaler
    namespace = args[1]  # str | object name and auth scope, such as for teams and projects
    body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions |
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    grace_period_seconds = 56  # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period for the specified type will be used. Defaults to a per object value if not specified. zero means delete immediately. (optional)
    propagation_policy = 'propagation_policy_example'  # str | Whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both. The default policy is decided by the existing finalizer set in the metadata.finalizers and the resource-specific default policy. (optional)

    try:
        api_response = api_instance.delete_namespaced_horizontal_pod_autoscaler(name, namespace, body, pretty=pretty,
                                                                                grace_period_seconds=grace_period_seconds)

        pprint(api_response)
        status_code = 200
        return status_code

    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->delete_namespaced_horizontal_pod_autoscaler: %s\n" % e)


def selectNS(*args, **kwargs):
    # kubernetes.client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = kubernetes.client.AppsV1beta1Api()
    namespace = args[0]  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    field_selector = 'field_selector_example'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_namespaced_deployment(namespace, pretty=pretty,
                                                               include_uninitialized=include_uninitialized,
                                                               timeout_seconds=timeout_seconds, watch=watch)
        select_ns_deploy = []
        for row in api_response.items:
            deploy = {}
            deploy['deployment_name'] = row.metadata.name
            select_ns_deploy.append(deploy)
        return select_ns_deploy
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->list_namespaced_deployment: %s\n" % e)


def getSpecifiedSvc(*args, **kwargs):
    api_instance = kubernetes.client.CoreV1Api()
    namespace = args[1]  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    field_selector = 'metadata.name=' + args[
        0]  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_namespaced_service(namespace, pretty=pretty, field_selector=field_selector,
                                                            include_uninitialized=include_uninitialized,
                                                            timeout_seconds=timeout_seconds, watch=watch)
        selector_dict = {}
        for row in api_response.items:
            selector_dict['namespace'] = args[1]
            selector_dict['svc_name'] = row.metadata.name
            selector_dict['selector'] = row.spec.selector
            selector_dict['selector'].update(selector_dict['selector'])

        selector_dict['pod_list'] = getSpecifiedPod(**selector_dict)
        return selector_dict
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)


def getSpecifiedPod(*args, **kwargs):
    # print(kwargs)

    api_instance = kubernetes.client.CoreV1Api()
    namespace = kwargs['namespace']  # str | object name and auth scope, such as for teams and projects
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
    field_selector = 'field_selector_example'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = convertLabel(**kwargs[
        'selector'])  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_namespaced_pod(namespace, pretty=pretty,
                                                        include_uninitialized=include_uninitialized,
                                                        label_selector=label_selector,
                                                        timeout_seconds=timeout_seconds, watch=watch)
        label_list = []
        for row in api_response.items:
            label_list.append(row.metadata.name)
        return label_list
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)


def convertLabel(*args, **kwargs):
    match_list = re.findall(r"'(.*?)'", str(kwargs))
    label = match_list[0] + '=' + match_list[1]
    return label


def updateTableField(*args, **kwargs):

    '''
    :param kwargs:
    {'target_ref': 'grafana-grafana', 'created_at': '2017-09-06 01:47:07+00:00', 'namespace': 'kube-system',
    'min_replicas': '1', 'name': 'grafana-grafana', 'max_replicas': 10, 'apiVersion': 'autoscaling/v1',
    'uid': '4a50612d-92a5-11e7-b532-000c296cc8d9', 'current_replicas': 1, 'CPU_Util_percent': 55,
    'kind': 'HorizontalPodAutoscalerList', 'desired_replicas': 1}

    :param args:

    :return:
    '''

    api_instance = kubernetes.client.AutoscalingV1Api()
    hpa_target_ref = client.V1CrossVersionObjectReference(name=kwargs['target_ref'], kind=kind)
    hpa_spec = client.V1HorizontalPodAutoscalerSpec(max_replicas=kwargs['max_replicas'],scale_target_ref = hpa_target_ref,min_replicas = kwargs['min_replicas'],
                                                    target_cpu_utilization_percentage=kwargs['CPU_Util_percent'])
    hpa_metadata = client.V1ObjectMeta(name=kwargs['name'], namespace=kwargs['namespace'])
    hpa_status = client.V1HorizontalPodAutoscalerStatus()
    name = kwargs['name']  # str | name of the HorizontalPodAutoscaler
    namespace = kwargs['namespace']  # str | object name and auth scope, such as for teams and projects
    body = kubernetes.client.V1HorizontalPodAutoscaler(metadata=hpa_metadata, spec=hpa_spec, status=hpa_status)  # V1HorizontalPodAutoscaler |
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)

    try:
        api_response = api_instance.replace_namespaced_horizontal_pod_autoscaler(name, namespace, body, pretty=pretty)
        pprint(api_response)
        status = 201
        return status

    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->replace_namespaced_horizontal_pod_autoscaler: %s\n" % e)
