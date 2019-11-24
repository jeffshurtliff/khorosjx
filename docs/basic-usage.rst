Importing the package
=====================
The package can be imported into a Python script using the syntax below.

.. code-block:: python

    import khorosjx

|

Initializing the modules
========================
While it is certainly possible to import modules directly (e.g. ``from khorosjx import users``), it is
recommended that you instead leverage the ``init_module()`` function as shown below.

.. code-block:: python

    khorosjx.init_module('content', 'users')

In the example above, both the ``khorosjx.content`` and the ``khoros.users`` modules have been initiated.

.. note:: It is not necessary to import the ``khorosjx.core`` module as it is imported by default.

|

Establishing the API connection
===============================
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