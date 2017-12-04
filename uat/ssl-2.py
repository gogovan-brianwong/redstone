from OpenSSL import crypto, SSL
import os

def generateCertificateObjects(organization, organizationalUnit):
    """
    Create a certificate for given C{organization} and C{organizationalUnit}.

    @return: a tuple of (key, request, certificate) objects.
    """
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 512)
    req = crypto.X509Req()
    subject = req.get_subject()
    subject.O = organization
    subject.OU = organizationalUnit
    req.set_pubkey(pkey)
    req.sign(pkey, "sha1")

    # Here comes the actual certificate
    cert = crypto.X509()
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60)  # Testing certificates need not be long lived
    cert.set_issuer(req.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(pkey, "sha1")

    return pkey, req, cert


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




    dump_to_file(generateCertificateObjects('abnet','k8s')[2], destpath='cert_files/'+'cert', format=crypto.FILETYPE_PEM)