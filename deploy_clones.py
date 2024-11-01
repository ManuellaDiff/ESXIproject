import json
import os
import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from dotenv import load_dotenv
from utils.esxi_connexion import get_connexion

# Chargement des configurations depuis le fichier config.json et 
# de meme on charge les variables d'environement depuis le fichier .env
load_dotenv()
host = os.getenv('HOST') 
user = os.getenv('USER_') 
password = os.getenv('PASSWORD')

with open('data/config.json', 'r') as config_file:
    config = json.load(config_file)

c = get_connexion(host=host, user=user, pwd=password)

content = c.RetrieveContent()

# la fonction clone_vm permet de clonner la vm existante.

def clone_vm(template_vm, vm_name):
    datacenter = content.rootFolder.childEntity[0]
    destfolder = datacenter.vmFolder
    resource_pool = datacenter.hostFolder.childEntity[0].resourcePool


    relospec = vim.vm.RelocateSpec()
    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = True
    clonespec.template = False
 

    task = template_vm.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    while task.info.state == vim.TaskInfo.State.running:
        continue
    if task.info.state == vim.TaskInfo.State.success:
        print(f"VM {vm_name} clonée avec succès.")
    else:
        print(f"Erreur lors du clonage de la VM {vm_name}: {task.info.error}")


template_vm = None
for datacenter in content.rootFolder.childEntity:
    for vm in datacenter.vmFolder.childEntity:
        print(f"Checking VM: {vm.name}")
        if vm.name == config['template_vm']:
            template_vm = vm
            break

if not template_vm:
    print("Template VM non trouvée.")
else:
    
    for i in range(config['num_instances']):
        vm_name = f"{config['vm_name']}_{i+1}"
        clone_vm(template_vm, vm_name)

print("Toutes les machines virtuelles ont été clonées avec succès.")
