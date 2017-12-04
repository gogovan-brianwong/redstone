from OpenSSL import crypto, SSL
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st_cert = open(os.path.join(BASE_DIR, 'assets/certs/ca.pem'), 'rt').read()

c = crypto
cert = c.load_certificate(c.FILETYPE_PEM, st_cert)

print (cert)