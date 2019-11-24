##############
Managing Users
##############
.. warning::

    This page is currently in development.

This page has instructions relating to managing users within a
KhorosJX (or Jive-n) community, including tasks such as obtaining
user information and statistics and other similar operations.

* `Leveraging the Users Module`_
* `Obtaining User Information`_
    * `Obtain the User ID of a user`_

***************************
Leveraging the Users Module
***************************
In order to leverage the Users Module (and any other module within the
khorosjx library) you must first perform the following steps:

1. Import the high-level **khorosjx** package.
2. Initialize the **users** module.
3. Establish the connection to the environment.

This is demonstrated in the example below.

.. code-block:: python

    # Import the package
    import khorosjx

    # Initialize the users module
    khorosjx.init_module('users')

    # Establish a connection to the environment
    environment_url = 'https://community.example.com'
    api_username = 'adminuser'
    api_password = 'password123$'
    khorosjx.core.connect(environment_url, (api_username, api_password))

    # Global variables established from the connection above
    base_url            # Global variable (str) derived from the environment_url above
    api_credentials     # Global variable (tuple) derived from api_username and api_password above

.. warning::

    The API credentials were defined in the example above for the purpose of demonstrating the process.
    However, it is strongly recommended that you **never** include API credentials in plaintext within
    scripts or other locations that can potentially be accessed by unauthorized parties.

**************************
Obtaining User Information
**************************
This section addresses how you can obtain information about a user to
use in other administrative functions and/or to obtain for statistical
purposes.

Obtain the User ID of a user
============================
The User ID value is a unique identifier within the KhorosJX / Jive environment
which identifies a user and allows the platform--as well as third-party
integrations via the API--to take actions against the user in various
capacities.

However, sometimes the User ID for a user is not readily available and you only
have their email address or username. In these situations, the ``get_user_id()``
function can be used to retrieve the needed User ID, as shown in the examples below.

.. code-block:: python
    
    user_id_from_email = khorosjx.users.get_user_id('john.doe@example.com')
    user_id_from_username = khorosjx.users.get_user_id('john_doe', 'username')

.. note::

    You will notice that, because ``email`` is the default identifier, you must
    supply ``username`` as a second argument if you are providing a username.

.. todo::

    The remainder of this document is still in progress. Please check back later
    for updates.