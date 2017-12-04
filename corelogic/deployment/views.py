from __future__ import print_function
import kubernetes
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from pprint import pprint
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def all_deploy_info(*args, **kwargs):
    kubernetes.client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = kubernetes.client.ExtensionsV1beta1Api()
    field_selector = 'field_selector_example'  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    include_uninitialized = 'true'  # bool | If true, partially initialized resources are included in the response. (optional)
    label_selector = 'label_selector_example'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
    resource_version = 'resource_version_example'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        # api_response = api_instance.list_deployment_for_all_namespaces(field_selector=field_selector,
        #                                                                include_uninitialized=include_uninitialized,
        #                                                                label_selector=label_selector, pretty=pretty,
        #                                                                resource_version=resource_version,
        #                                                                timeout_seconds=timeout_seconds, watch=watch)
        api_response = api_instance.list_deployment_for_all_namespaces(watch=watch)
        return api_response.items

    except ApiException as e:
        print("Exception when calling ExtensionsV1beta1Api->list_deployment_for_all_namespaces: %s\n" % e)


def findOne(*args, **kwargs):
    # kubernetes.client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = kubernetes.client.ExtensionsV1beta1Api()
    name = args[0]  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    namespace = 'kube-system'  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
    exact = 'true'  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    export = 'true'
    watch = 'false'  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.read_namespaced_deployment(name, namespace, pretty=pretty, exact=exact, export=export)
        # api_response = api_instance.list_deployment_for_all_namespaces(watch=watch)
        return api_response.to_dict()

    except ApiException as e:
        print("Exception when calling ExtensionsV1beta1Api->list_deployment_for_all_namespaces: %s\n" % e)


