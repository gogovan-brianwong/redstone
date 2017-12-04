from django.shortcuts import render

# Create your views here.
from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_FILE = 'myapp.crt'
KEY_FILE = 'myapp.key'


def create_self_signed_cert(cert_dir):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "Minnesota"
        cert.get_subject().L = "Minnetonka"
        cert.get_subject().O = "my company"
        cert.get_subject().OU = "my organization"
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        open(join(cert_dir, CERT_FILE), "w").write(str(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert)))
        open(join(cert_dir, KEY_FILE), "w").write(str(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k)))


############ 2 ##########

from OpenSSL import crypto

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA


def createKeyPair(type, bits):
    """
    Create a public/private key pair.
    Arguments: type - Key type, must be one of TYPE_RSA and TYPE_DSA
               bits - Number of bits to use in the key
    Returns:   The public/private key pair in a PKey object
    """
    pkey = crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey


def createCertRequest(pkey, digest="sha256", **name):
    """
    Create a certificate request.
    Arguments: pkey   - The key to associate with the request
               digest - Digestion method to use for signing, default is sha256
               **name - The name of the subject of the request, possible
                        arguments are:
                          C     - Country name
                          ST    - State or province name
                          L     - Locality name
                          O     - Organization name
                          OU    - Organizational unit name
                          CN    - Common name
                          emailAddress - E-mail address
    Returns:   The certificate request in an X509Req object
    """
    req = crypto.X509Req()
    subj = req.get_subject()

    for key, value in name.items():
        setattr(subj, key, value)

    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req


def createCertificate(req, issuerCertKey, serial, validityPeriod,
                      digest="sha256"):
    """
    Generate a certificate given a certificate request.
    Arguments: req        - Certificate request to use
               issuerCert - The certificate of the issuer
               issuerKey  - The private key of the issuer
               serial     - Serial number for the certificate
               notBefore  - Timestamp (relative to now) when the certificate
                            starts being valid
               notAfter   - Timestamp (relative to now) when the certificate
                            stops being valid
               digest     - Digest method to use for signing, default is sha256
    Returns:   The signed certificate in an X509 object
    """
    issuerCert, issuerKey = issuerCertKey
    notBefore, notAfter = validityPeriod
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(issuerCert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(issuerKey, digest)
    return cert


def dump_to_file(material, destpath, mode=755, format=crypto.FILETYPE_PEM):
    """
    Writes the passed-in key/req/cert to file.

    :param material: A :class:`OpenSSL.crypto.X509`, :class:`OpenSSL.crypto.PKey` or :class:`OpenSSL.crypto.X509Req` object.
    :param destpath: The path to the file that should be created.
    :param mode: The mode with which to create the file.
    :param format: The format for the file (PEM or DER).
    """
    dump_func = None
    if isinstance(material, crypto.X509):
        dump_func = crypto.dump_certificate
    elif isinstance(material, crypto.PKey):
        dump_func = crypto.dump_privatekey
    elif isinstance(material, crypto.X509Req):
        dump_func = crypto.dump_certificate_request
    else:
        # FIXME: Exception type
        raise Exception("Don't know how to dump content type to file: %s (%r)" % (type(material), material))

    content = dump_func(format, material)

    destfd = os.open(destpath, os.O_RDWR | os.O_CREAT, mode)
    try:
        os.write(destfd, content)
    finally:
        os.close(destfd)


if __name__ == '__main__':
    # create_self_signed_cert('c:\k8s')
    dump_to_file(createKeyPair(TYPE_RSA, 2048),destpath='cert_files/' + 'keypair.pem', format=crypto.FILETYPE_PEM)
