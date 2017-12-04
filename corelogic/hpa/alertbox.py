from __future__ import print_function
import os
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from django.http import StreamingHttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kubernetes.config.load_kube_config(os.path.join(BASE_DIR, '../assets/certs', 'kubeconfig-dev.yaml'))



def scan_all_hpa():
    # Configure API key authorization: BearerToken
    # kubernetes.client.configuration.api_key['authorization'] = 'YOUR_API_KEY'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = kubernetes.client.AutoscalingV1Api()
    field_selector = 'currentCPUUtilizationPercentage'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_horizontal_pod_autoscaler_for_all_namespaces(
            include_uninitialized=include_uninitialized,
            pretty=pretty,
            timeout_seconds=timeout_seconds,
            watch=watch)
        current_replicas_list = []

        for row in api_response.items:

            current_replicas_dict = {}
            if row.status.current_replicas != 1:
                current_replicas_dict['name'] = row.metadata.name
                current_replicas_dict['code'] = 999
                current_replicas_list.append(current_replicas_dict)

        return current_replicas_list

    except ApiException as e:
        print("Exception when calling AutoscalingV1Api->list_horizontal_pod_autoscaler_for_all_namespaces: %s\n" % e)


def stream_generator():

    for i in scan_all_hpa():
        if i == 'None' or i['code'] != 999:
                continue
        else:
            yield u'data: %s&%s\n\n' % ( i['name'], i['code'])
            time.sleep(5)


