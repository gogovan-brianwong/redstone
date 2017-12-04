import os

import requests

from dao import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def login_auth(req):
    filled_username = req.POST.get('reg_username')
    filled_password = req.POST.get('reg_password')
    obj_list = models.UserDetails.objects.all()
    for item in obj_list:
        if item.username == filled_username and item.password == filled_password:

            status_code = 200
            return status_code
        else:
            status_code = 404
            return status_code

# @app.task(bind=True)
def showall():

    from Infrastructure.RegistryAPI import Registry

    reg_api_server = 'https://registry.allbright.local:5000'
    reg_api_endpoint = '/v2/_catalog'
    auth_user = 'admin'
    auth_passwd = 'allbright'

    rep_repositories = Registry(url=reg_api_server + reg_api_endpoint, auth=(auth_user,auth_passwd))

    content = rep_repositories.connect.json() # content => Json object

    image_alltags_list = []
    for eachimage in content['repositories']:

        for tag in fetch_imageTags(eachimage):

            image_tag_dict = {}

            image_tag_dict['name'] = eachimage
            image_tag_dict['tag'] = tag
            image_tag_dict['SHA'] = fetch_shaValue(eachimage,tag)
            # image_tag_dict['uid'] = base64.b64encode(bytes(image_tag_dict['SHA'], 'utf-8'))
            image_tag_dict['reg_api_server'] = reg_api_server[8:]

            image_alltags_list.append(image_tag_dict)
    return image_alltags_list


def fetch_imageTags(image):

    from Infrastructure.RegistryAPI import Registry

    auth_user = 'admin'
    auth_passwd = 'allbright'

    reg_api_server = 'https://registry.allbright.local:5000'
    reg_api_ep = '/v2/' + image + '/tags/list'

    rep_imageTags = Registry(url=reg_api_server +reg_api_ep, auth=(auth_user,auth_passwd))
    content = rep_imageTags.connect.json()

    print (content)
    return content['tags']



def fetch_shaValue(image,tag):
    # from pkg.RegistryAPI import Registry
    auth_user = 'admin'
    auth_passwd = 'allbright'

    reg_api_server = 'https://registry.allbright.local:5000'
    reg_api_ep = '/v2/' + image + '/manifests/' + tag
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
    rep = requests.get(reg_api_server + reg_api_ep, headers=headers,
                       verify=os.path.join(BASE_DIR, '../assets/certs/ca.crt'), auth=(auth_user, auth_passwd))
    header_key = 'Docker-Content-Digest'
    # rep = Registry(url=reg_api_server + reg_api_ep, headers=headers, auth=(auth_user, auth_passwd))
    if header_key in rep.headers.keys():
        content = rep.headers['Docker-Content-Digest']
    else:
        content = "NULL"
    return content

def image_info(request,uid):
    pass


def remove_image(request,nid):
    if request.method == 'POST':
        uid = request.POST.get('nid')
        imgName = request.POST.get('imgName')
        imgTag = request.POST.get('imgTag')
        imgSha = request.POST.get('imgSha')

        print ('%s - %s - %s -%s' % (uid, imgName, imgTag, imgSha))