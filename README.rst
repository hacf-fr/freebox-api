freebox-api
===========

|PyPI| |GitHub Release| |Python Version| |License|

|Read the Docs| |Tests| |Codecov| |GitHub Activity|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/freebox-api.svg
   :target: https://pypi.org/project/freebox-api/
   :alt: PyPI
.. |GitHub Release| image:: https://img.shields.io/github/release/hacf-fr/freebox-api.svg
   :target: https://github.com/hacf-fr/freebox-api/releases
   :alt: GitHub Release
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/freebox-api
   :target: https://pypi.org/project/freebox-api
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/freebox-api
   :target: https://opensource.org/licenses/GPL-3.0
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/freebox-api/latest.svg?label=Read%20the%20Docs
   :target: https://freebox-api.readthedocs.io/
   :alt: Read the documentation at https://freebox-api.readthedocs.io/
.. |Tests| image:: https://github.com/hacf-fr/freebox-api/workflows/Tests/badge.svg
   :target: https://github.com/hacf-fr/freebox-api/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/hacf-fr/freebox-api/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hacf-fr/freebox-api
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |GitHub Activity| image:: https://img.shields.io/github/commit-activity/y/hacf-fr/freebox-api.svg
   :target: https://github.com/hacf-fr/freebox-api/commits/master
   :alt: GitHub Activity


Features
--------

Easily manage your freebox in Python using the Freebox OS API.
Check your calls, manage your contacts, configure your dhcp, disable your wifi, monitor your LAN activity and many others, on LAN or remotely.

freebox-api is a python library implementing the freebox OS API. It handles the authentication process and provides a raw access to the freebox API in an asynchronous manner.

This project is based on fstercq/freepybox, which provides the same features as freebox-api in a synchronous manner.


Requirements
------------

* TODO


Installation
------------

You can install *freebox-api* via pip_ from PyPI_:

.. code:: console

   $ pip install freebox-api

Or manually download the last version from github and install it with Poetry_

.. code:: console

   $ git clone https://github.com/hacf-fr/freebox-api.git
   $ python poetry install

.. _Poetry: https://python-poetry.org/



Usage
-----

.. code:: python

   # Import the freebox-api package.
   from freebox_api import Freepybox

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

Have a look at the example.py_ for a more complete overview.

.. _example.py: tests/example.py

Notes on HTTPS
--------------

When you access a Freebox with its default-assigned domain (ending in ``fbxos.fr``), the library verifies its
certificate by automatically trusting the Freebox certificate authority. If you want to avoid this, you can
`setup a custom domain name`_ which will be associated with a Let's Encrypt certificate.

.. _setup a custom domain name: https://www.freenews.fr/freenews-edition-nationale-299/freebox-9/lacces-distant-a-freebox-os-sameliore-https


Resources
---------

Freebox OS API documentation : http://dev.freebox.fr/sdk/os/


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `GNU GPL v3`_ license,
*freebox-api* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.


.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _GNU GPL v3: https://opensource.org/licenses/GPL-3.0
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/hacf-fr/freebox-api/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
