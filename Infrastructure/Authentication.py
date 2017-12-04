import os

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class APIAuth():

    from Infrastructure.conf.APIAuth_param import APIAuthInfo

    # Class construct ini function with default CA cert
    def __init__(self, url=APIAuthInfo['APIHost_URL'], data=(None), headers=(None),cacert=APIAuthInfo['CA'],
                                                                              cert=( APIAuthInfo['Client_Cert'],
                                                                                     APIAuthInfo['Client_Key'])):
        self.url = url
        self.cacert = cacert
        self.cert = cert
        self.headers = headers
        self.data = data

    def connect_get(self, resourceEndpoint):
        with requests.Session() as s:
            content = s.get(self.url + resourceEndpoint, headers=self.headers, verify=self.cacert, cert=self.cert)

        return  content

    def connect_post(self, resourceEndpoint):
        with requests.Session() as s:
            content = s.post(self.url + resourceEndpoint, headers=self.headers, verify=self.cacert, cert=self.cert)

        return  content

    def connect_del(self, resourceEndpoint):
        with requests.Session() as s:
            content = s.delete(self.url + resourceEndpoint, headers=self.headers, verify=self.cacert, cert=self.cert)

        return  content

    def connect_put(self, resourceEndpoint, payload, headers):
        with requests.Session() as s:
            content = s.put(self.url + resourceEndpoint, data=payload, headers=headers, verify=self.cacert, cert=self.cert)

        return  content

    def connect_patch(self, resourceEndpoint,payload):
        with requests.Session() as s:
            content = s.patch(self.url + resourceEndpoint, data=payload, headers=self.headers, verify=self.cacert, cert=self.cert)

        return  content

