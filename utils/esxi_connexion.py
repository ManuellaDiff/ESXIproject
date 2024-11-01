import ssl
from pyVim.connect import SmartConnect, Disconnect
import atexit

'''
 etablissons une connection  sécurisée à l'ESXi en désactivant la vérification SSL.

'''
def get_connexion(host, user, pwd):
    context = ssl._create_unverified_context()
    c = SmartConnect(host=host, user=user, pwd=pwd, sslContext=context, disableSslCertValidation=True)
    atexit.register(Disconnect, c)
    
    return c



