from utils.esxi_connexion import get_connexion
import os
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect
import atexit

load_dotenv()

host = os.getenv('HOST')
user = os.getenv('USER_')
password = os.getenv('PASSWORD')


c = get_connexion(host=host, user=user, pwd=password)
print(c.CurrentTime())



