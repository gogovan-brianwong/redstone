import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

imagePullPolicy = (

    "IfNotPresent",
    "Never",
    "Always",

)
# Guest registry : registry.allbright.local/guestrepo/{ IMAGE }:{ VER }
# eg. docker pull registry.allbright.local/guestrepo/mongodb:3.4
imagePullSecrets = (

    'harbor-secret-guest',

)

serviceType = (
    "ClusterIP",
    "NodePort",
    "LoadBalancer",

)

accessMode = (

    "ReadWriteOnce",
    "ReadOnlyMany",
    "ReadWriteMany",
)

volumePhase = (

    "Available",
    "Bound",
    "Released",
    "Failed",
)

ingressAnnotations = [

    "kubernetes.io/ingress.class: nginx",
    'ingress.kubernetes.io/ssl-redirect: "false"',
    "ingress.kubernetes.io/proxy-body-size: 500m",

]

wordpress_default_info = {

    'app_firstname': 'wordpress',
    'app_lastname': 'wordpress',
    'app_blog_name': 'WPBlog',
    'app_email': 'wordpress@example.com',
    'app_detail_healthcheck': 'False'

}



