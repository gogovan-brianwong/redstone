import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APIAuthInfo = {

    'APIHost_URL': 'https://47.52.242.147:8443',
    'CA': os.path.join(BASE_DIR, 'assets/certs/ca.crt'),
    'Client_Cert': os.path.join(BASE_DIR, 'assets/certs/client.crt'),
    'Client_Key': os.path.join(BASE_DIR, 'assets/certs/client.key'),

}