class Vm:

    def __init__(self, access):
        self._access = access

    disk_info_schema = {
        'disk_path': ''
    }

    resize_schema = {
        'disk_path': '',
        'size': 45097156608,
        'shrink_allow': False
    }

    vm_init_schema = {
        'name': '',
        'disk_path': '',
        'disk_type': 'qcow2',
        'cd_path': '',
        'memory': 957,
        'vcpus': 2,
        'status': '',
        'enable_screen': False,
        'bind_usb_ports': [],
        'enable_cloudinit': True,
        'cloudinit_hostname': 'freebox-vm',
        'cloudinit_userdata': '#cloud-config\nsystem_info:\n  default_user:\n    name: freebox\npassword: ubuntoutou\nchpasswd: { expire: False }\nssh_pwauth: True\n',
        'mac': '',
        'os': 'ubuntu'
    }

    async def create_vm(self, vm_init_data):
        """
        Create a vm
        """
        return await self._access.post('vm/', vm_init_data)

    async def delete_vm(self, vm_id):
        """
        Delete a vm
        """
        await self._access.delete(f'vm/{vm_id}')

    async def edit_vm(self, vm_id, vm_config_data):
        """
        Edit vm configuration
        """
        return await self._access.put(f'vm/{vm_id}', vm_config_data)

    ''' Disabled : requires websocket
    async def get_console(self, vm_id):
        """
        Get console
        """
        return await self._access.wsget(f'vm/{vm_id}/console')
    '''

    async def get_distros(self):
        """
        Get distros
        """
        return await self._access.get('vm/distros/')

    async def get_disk_info(self):
        """
        Get disk info
        """
        return await self._access.post('vm/disk/info')

    async def get_vms(self):
        """
        Get the list of vms
        """
        return await self._access.get('vm/')

    async def resize_vm(self, resize_data):
        """
        Resize a vm
        """
        return await self._access.post('vm/disk/resize', resize_data)

    async def restart_vm(self, vm_id):
        """
        Restart a vm
        """
        return await self._access.post(f'vm/{vm_id}/restart/')

    async def start_vm(self, vm_id):
        """
        Start a vm
        """
        return await self._access.post(f'vm/{vm_id}/start/')

    async def shutdown_vm(self, vm_id):
        """
        Shutdown a vm
        """
        return await self._access.post(f'vm/{vm_id}/powerbutton/')

    async def stop_vm(self, vm_id):
        """
        Stop a vm
        """
        return await self._access.post(f'vm/{vm_id}/stop/')
