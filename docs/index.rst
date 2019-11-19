############
Introduction
############

The **khorosjx** library acts as a Python software development kit (SDK)
to administer and manage `Khoros JX <https://community.khoros.com/t5/Atlas-Insights-Blog/Lithium-and-Jive-x-
It-s-Official/ba-p/325465>`_ (formerly `Jive-x <https://www.prnewswire.com/news-releases/lithium-technologies-
completes-acquisition-of-external-online-community-business-from-jive-300531058.html>`_) and 
`Jive-n <https://www.jivesoftware.com/>`_ online community platforms.

|

Installation
============
The package can be installed via pip using the syntax below.

.. code-block:: default

    # pip install khorosjx

You may also clone the repository and install from source using the syntax below.

.. code-block:: default

    # git clone git://github.com/jeffshurtliff/khorosjx.git
    # cd khorosjx/
    # python3 setup.py install

|

Usage
=====
This section provides basic usage instructions for the package.

Importing the package
---------------------
.. code-block:: python

    import khorosjx

|

Initializing the modules
------------------------
While it is certainly possible to import modules directly (e.g. ``from khorosjx import users``), it is
recommended that you instead leverage the ``init_module()`` function as shown below.

.. code-block:: python

    khorosjx.init_module('content', 'users')

In the example above, both the ``khorosjx.content`` and the ``khoros.users`` modules have been initiated.

.. note:: It is not necessary to import the ``khorosjx.core`` module as it is imported by default.

|

Establishing the API connection
-------------------------------
Before leveraging the API in function calls, you must first establish your connection by providing the
base URL for the environment (e.g. ``https://community.example.com``) and the username and password for
the unfederated service account through which the API calls will be made.  This is demonstrated below.

.. code-block:: python

    base_url = 'https://community.example.com'
    credentials = ('adminuser', 'password123!')
    khorosjx.core.connect(base_url, credentials)

|

.. note:: 

    At this time the library only allow connections using 
    `basic authentication <https://developers.jivesoftware.com/api/v3/cloud/rest/index.html#authentication>`_, 
    but there are plans to include the ability to leverage 
    `OAuth 2.0 <https://developers.jivesoftware.com/api/v3/cloud/rest/AuthorizationEntity.html>`_ in a 
    future release.

Once the connection has been established, you can proceed to leverage the library of functions in the
various modules as needed.

|

Requirements
============
The following packages are leveraged within the khorosjx package:

* numpy 1.17.4
* pandas-0.25.3
* python-dateutil 2.8.1
* pytz 2019.3
* requests 2.22.0
* urllib3 1.25.7

The full requirements list can be foune in the :file:`requirements.txt` file.

|

Modules
=======
The KhorosJX Python Library consists of the following :doc:`primary modules <primary-modules>`:

:ref:`primary-modules:Core Module (khorosjx.core)`
    This module contains core functions such as initializing the connection to the API, getting API version
    information, performing GET and PUT requests, etc.

:ref:`primary-modules:Admin Module (khorosjx.admin)`
    This module contains administrative functions that would only be performed by a platform administrator
    or a community manager.

:ref:`primary-modules:Content Module (khorosjx.content)`
    This module contains functions relating to content within the platform which allows for creating, editing
    and managing content such as documents, ideas, videos, etc.

:ref:`primary-modules:Groups Module (khorosjx.groups)`
    This module contains functions for working with security groups (and eventually social groups) such as
    obtaining and managing group membership.

:ref:`primary-modules:Spaces Module (khorosjx.spaces)`
    This module contains functions for working with spaces, such as identifying content within spaces, etc.

:ref:`primary-modules:Users Module (khorosjx.users)`
    This module contains functions for working with users, such as obtaining their account/profile information, 
    getting a count of their created content, etc.

|

The library also includes some :doc:`auxilliary modules <auxilliary-modules>` to support the overall functionality of 
the :doc:`primary modules <primary-modules>`, as well as modules containing global :ref:`auxilliary-modules:classes 
and exceptions` for the library, which are listed below.

:ref:`auxilliary-modules:Core Utilities Module (khorosjx.utils.core_utils)`
    This module includes various utilities to assist in converting dictionaries to JSON, formatting timestamps, etc.

:ref:`auxilliary-modules:Classes Module (khorosjx.utils.classes)`
    This module contains nearly all classes utilized by other modules within the library.

:ref:`auxilliary-modules:Exceptions Module (khorosjx.errors.exceptions)`
    This module contains all of the exception classes leveraged in functions throughout the library.

|

Disclaimer
==========

This package is in no way endorsed or supported by the `Khoros <https://www.builtinaustin.com/company/khoros>`_ 
or `Aurea Software, Inc. <https://www.jivesoftware.com/>`_ companies.

|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

|

.. toctree::
   :hidden:

   primary-modules
   auxilliary-modules