import json
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
from dotenv import load_dotenv
import os
from utils.esxi_connexion import get_connexion


load_dotenv()


host = os.getenv('HOST')
user = os.getenv('USER_')
password = os.getenv('PASSWORD')

# Chargeons la configuration depuis le fichier JSON
with open('data/config2.json', 'r') as config_file:
    config = json.load(config_file)


c = get_connexion(host=host, user=user, pwd=password)
content = c.RetrieveContent()

def create_dummy_vm(vm_name, si, vm_folder, resource_pool, datastore):

    ''' Création d'une VM "vide" avec les spécifications de base '''
    config_spec = vim.vm.ConfigSpec(
        name=vm_name,
        memoryMB=config['memory'],
        numCPUs=config['cpu'],
        guestId="otherGuest",
        version="vmx-13"
    )

    
    disk_spec = vim.vm.device.VirtualDeviceSpec(
        operation=vim.vm.device.VirtualDeviceSpec.Operation.add,
        device=vim.vm.device.VirtualDisk(
            backing=vim.vm.device.VirtualDisk.FlatVer2BackingInfo(
                datastore=datastore,
                diskMode="persistent"
            ),
            capacityInKB=config['disk_size'] * 1024 * 1024
        )
    )
    config_spec.deviceChange.append(disk_spec)

    # Ajouter CD-ROM
    cdrom_spec = vim.vm.device.VirtualDeviceSpec(
        operation=vim.vm.device.VirtualDeviceSpec.Operation.add,
        device=vim.vm.device.VirtualCdrom(
            backing=vim.vm.device.VirtualCdrom.IsoBackingInfo(
                fileName=config['cdrom_iso_path'],
                datastore=datastore
            )
        )
    )
    config_spec.deviceChange.append(cdrom_spec)

    task = vm_folder.CreateVM_Task(config=config_spec, pool=resource_pool)
    return task

# Variables nécessaires
datacenter = content.rootFolder.childEntity[0]
vm_folder = datacenter.vmFolder
resource_pool = datacenter.hostFolder.childEntity[0].resourcePool
datastore = datacenter.datastore[0]  # Utiliser le premier datastore

# Création d'une instance de VM
for i in range(config['num_instances']):
    vm_name = f"{config['vm_name']}_{i+1}"
    task = create_dummy_vm(vm_name, c, vm_folder, resource_pool, datastore)
    while task.info.state == vim.TaskInfo.State.running:
        continue
    if task.info.state == vim.TaskInfo.State.success:
        print(f"VM {vm_name} créée avec succès.")
    else:
        print(f"Erreur lors de la création de la VM {vm_name}: {task.info.error}")

print("la machines virtuelles a été crééeavec succè.")
