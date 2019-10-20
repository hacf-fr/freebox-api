import base64


class Vm:
    """
    Vm
    """

    def __init__(self, access):
        self._access = access

    oses = ["fedora", "debian", "ubuntu", "freebsd"]

    disk_info_schema = {"disk_path": ""}

    resize_schema = {"disk_path": "", "size": 45097156608, "shrink_allow": False}

    vm_init_schema = {
        "name": "",
        "disk_path": "",
        "disk_type": "qcow2",
        "cd_path": "",
        "memory": 957,
        "vcpus": 2,
        "status": "",
        "enable_screen": False,
        "bind_usb_ports": [],
        "enable_cloudinit": True,
        "cloudinit_hostname": "freebox-vm",
        "cloudinit_userdata": "#cloud-config\nsystem_info:\n  default_user:\n    name: freebox\npassword: ubuntoutou\nchpasswd: { expire: False }\nssh_pwauth: True\n",
        "mac": "",
        "os": "ubuntu",
    }

    async def create_vm(self, vm_init_data):
        """
        Create a vm

        vm_init_data : `vm_init_schema`
        """
        return await self._access.post("vm/", vm_init_data)

    async def delete_vm(self, vm_id):
        """
        Delete a vm

        vm_id : `int`
        """
        await self._access.delete(f"vm/{vm_id}")

    async def edit_vm(self, vm_id, vm_config_data):
        """
        Edit vm configuration

        vm_id : `int`
        vm_config_data : `dict`
        """
        return await self._access.put(f"vm/{vm_id}", vm_config_data)

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
        return await self._access.get("vm/distros/")

    async def get_disk_info(self, disk_path):
        """
        Get disk info

        disk_path : `str`
        """
        disk_info = self.disk_info_schema
        disk_info["disk_path"] = base64.b64encode(disk_path.encode("utf-8")).decode(
            "utf-8"
        )
        return await self._access.post("vm/disk/info", disk_info)

    async def get_vms(self):
        """
        Get the list of vms
        """
        return await self._access.get("vm/")

    async def resize_vm(self, disk_path, new_size, shrink_allow=False):
        """
        Resize a vm

        disk_path : `str`
        new_size : `int`
        shrink_allow : True | False
            , Default to False
        """
        resize = self.resize_schema
        resize["disk_path"] = base64.b64encode(disk_path.encode("utf-8")).decode(
            "utf-8"
        )
        resize["size"] = new_size
        resize["shrink_allow"] = shrink_allow
        return await self._access.post("vm/disk/resize", resize)

    async def restart_vm(self, vm_id):
        """
        Restart a vm

        vm_id : `int`
        """
        return await self._access.post(f"vm/{vm_id}/restart/")

    async def start_vm(self, vm_id):
        """
        Start a vm

        vm_id : `int`
        """
        return await self._access.post(f"vm/{vm_id}/start/")

    async def shutdown_vm(self, vm_id):
        """
        Shutdown a vm

        vm_id : `int`
        """
        return await self._access.post(f"vm/{vm_id}/powerbutton/")

    async def stop_vm(self, vm_id):
        """
        Stop a vm

        vm_id : `int`
        """
        return await self._access.post(f"vm/{vm_id}/stop/")
