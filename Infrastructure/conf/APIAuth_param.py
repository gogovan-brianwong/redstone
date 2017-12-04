import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APIAuthInfo = {

    'APIHost_URL': 'https://192.168.151.40:443',
    'CA': os.path.join(BASE_DIR, 'assets/certs/ca.pem'),
    'Client_Cert': os.path.join(BASE_DIR, 'assets/certs/apiserver.pem'),
    'Client_Key': os.path.join(BASE_DIR, 'assets/certs/apiserver-key.pem'),

}