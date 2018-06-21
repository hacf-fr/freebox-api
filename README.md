aiofreepybox
==========

Easily manage your freebox in Python using the Freebox OS API.
Check your calls, manage your contacts, configure your dhcp, disable your wifi, monitor your LAN activity and many others, on LAN or remotely.

aiofreepybox is a python library implementing the freebox OS API. It handles the authentication process and provides a raw access to the freebox API in an asynchronous manner.

This project is based on fstercq/freepybox, which provides the same features as aiofreepybox in a synchronous manner.

Install
-------
Use the PIP package manager
```bash
$ pip install aiofreepybox
```

Or manually download and install the last version from github
```bash
$ git clone https://github.com/stilllman/aiofreepybox.git
$ python setup.py install
```

Get started
-----------
```python
# Import the aiofreepybox package.
from aiofreepybox import Freepybox

async def reboot()
    # Instantiate the Freepybox class using default options.
    fbx = Freepybox()

    # Connect to the freebox with default options. 
    # Be ready to authorize the application on the Freebox.
    await fbx.open('192.168.0.254')

    # Do something useful, rebooting your freebox for example.
    await fbx.system.reboot()

    # Properly close the session.
	await fbx.close()
```
Have a look at the [example.py](https://github.com/stilllman/freepybox/blob/aiofreepybox/example.py) for a more complete overview.

Notes on HTTPS
--------------
When you access a Freebox with its default-assigned domain (ending in `fbxos.fr`), the library verifies its certificate by automatically trusting the Freebox certificate authority. If you want to avoid this, you can [setup a custom domain name](https://www.freenews.fr/freenews-edition-nationale-299/freebox-9/lacces-distant-a-freebox-os-sameliore-https) which will be associated with a Let's Encrypt certificate.

Resources
---------
Freebox OS API documentation : http://dev.freebox.fr/sdk/os/

