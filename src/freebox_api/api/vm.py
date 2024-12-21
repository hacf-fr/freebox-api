import base64

class Vm:
    """
    API to manage VMs
    """

    def __init__(self, access):
        self._access = access
    
    usb_ports = [ 'usb-external-type-c', 'usb-external-type-a' ]
    disk_type = [ 'qcow2', 'raw' ]
    vm_os = [ 'debian', 'ubuntu', 'fedora', 'other1', 'other2', 'other3' ]
    init_data_schema = { 'user': 'freebox', 'pwd': 'this_is_not_g00d',
        'sshkey': '', 'seefbx': True }
    vm_write_parms = { 'bind_usb_ports': 'list', 'cd_path': 'text',
        'cloudinit_hostname': 'text', 'cloudinit_userdata': 'sublist',
        'disk_type': 'text', 'enable_cloudinit': 'bool', 'disk_path': 'text',
        'enable_screen': 'bool', 'memory': 'int', 'name': 'text',
        'os': 'text', 'vcpus': 'int' }
    vm_data_schema = { 'bind_usb_ports': [], 'cd_path': '',
        'cloudinit_hostname': 'fbxvm', 'cloudinit_userdata': init_data_schema,
        'disk_path': '', 'disk_type': disk_type[0], 'enable_cloudinit': True,
        'enable_screen': False, 'memory': 512, 'name': 'fbxvm',
        'os': vm_os[3], 'vcpus': 1 }
    vm_raw_schema = { 'bind_usb_ports': [], 'cd_path': '',
        'cloudinit_hostname': 'fbxvm', 'cloudinit_userdata': '',
        'disk_path': '', 'disk_type': disk_type[0], 'enable_cloudinit': True,
        'enable_screen': False, 'memory': 512, 'name': 'fbxvm',
        'os': vm_os[3], 'vcpus': 1 }

    async def get_config_all(self):
        """
        Gets all VM configuration
        """
        return await self._access.get('vm/')

    async def get_system_info(self):
        """
        Gets system informations
        """
        return await self._access.get('vm/info')

    async def get_config_vm(self, id):
        """
        Gets VM #id configuration
        """
        return await self._access.get('vm/{0}/'.format(id))
    
    async def start(self, id):
        """
        Starts specified VM
        """
        return await self._access.post('vm/{0}/start'.format(id), payload=None)
    
    async def restart(self, id):
        """
        Restarts specified VM
        """
        return await self._access.post('vm/{0}/restart/'.format(id), payload=None)
    
    async def stop(self, id):
        """
        Stops specified VM
        """
        return await self._access.post('vm/{0}/powerbutton'.format(id), payload=None)

    async def halt(self, id):
        """
        Halt/force stop specified VM
        """
        return await self._access.post('vm/{0}/stop'.format(id), payload=None)

    async def get_distrib(self):
        """
        Gets all free distributions
        """
        return await self._access.get('vm/distros')
    
    async def resize(self, vfile, size, shrink=False):
        """
        Resize VM virtual file
        """
        json = { 'disk_path': base64.b64encode(vfile.encode('utf-8')).decode('utf-8'), 'shrink_allow': shrink, 'size': size }
        return await self._access.post('vm/disk/resize', payload=json)
    
    async def get_task(self, id):
        """
        Gets resize or create task status
        """
        return await self._access.get('vm/disk/task/{0}'.format(id))
    
    async def del_task(self, id):
        """
        Removes resize or create task
        """
        return await self._access.delete('vm/disk/task/{0}'.format(id))
        
    def format_cloudinit_data(self, user, pwd='', sshkey='', seefbx=False):
        """
        Formats a correct string for cloudinit_userdata
        """
        if pwd == '' and sshkey == '': return ''
        cid = '#cloud-config'
        if sshkey != '': cid = cid + '\nssh_authorized_keys:\n  - ' + sshkey
        cid = cid + '\nsystem_info:\n default_user:\n  name: ' + user
        if pwd != '': cid = cid + '\npassword: ' + pwd + '\nchpasswd: { expire: False }\nssh_pwauth: True'
        if seefbx: cid = cid + '\npackages_update: true\npackages:\n  - cifs-utils\nmounts:\n  - [ \'//mafreebox.freebox.fr/Freebox\', \'/mnt/Freebox\', cifs, \'vers=1.0,guest,uid=1000,gid=1000\', \'0\', \'0\' ]\nruncmd:\n  - mount -a'
        cid = cid + '\n'
        return cid

    def decode_cloudinit_data(self, conf={}):
        """
        Decodes a JSON representing the cloudinit_userdata
        """
        if conf == {}: return ''
        if 'user' not in conf: return ''
        else: usr = conf['user']
        if 'pwd' in conf: pwd = conf['pwd']
        else: pwd = ''
        if 'sshkey' in conf: sshkey = conf['sshkey']
        else: sshkey = ''
        if 'seefbx' in conf: seefbx = (conf['seefbx'] == 'True')
        else: seefbx = False
        return self.format_cloudinit_data(usr, pwd, sshkey, seefbx)

    def encode_dirs(self, data):
        for d in ['disk_path', 'cd_path']:
            if d in data:
                data[d] = base64.b64encode(data[d].encode('utf-8')).decode('utf-8')

    async def create(self, data, decodedir=True):
        """
        Creates a new VM
        """
        if decodedir:
            self.encode_dirs(data)
        print(data)
        return await self._access.post('vm/', payload=data)

    async def set_config(self, id, data, decodedir=True):
        """
        Sets VM #id configuration
        """
        if decodedir:
            self.encode_dirs(data)
        return await self._access.put('vm/{0}'.format(id), payload=data)
    
    async def delete(self, id):
        """
        Removes a VM
        """
        return await self._access.delete('vm/{0}'.format(id))

    async def disk_info(self, vfile):
        """
        Get VM disk info
        """
        json = { 'disk_path': base64.b64encode(vfile.encode('utf-8')).decode('utf-8') }
        return await self._access.post('vm/disk/info', payload=json)

    async def disk_create(self, vfile, size, disk_type):
        """
        Create VM disk task
        """
        json = { 'disk_path': base64.b64encode(vfile.encode('utf-8')).decode('utf-8'), 'disk_type': disk_type, 'size': size }
        return await self._access.post('vm/disk/create', payload=json)

    async def disk_list(self):
        """
        Get VM disk list
        """
        return await self._access.get('vm/disk')
