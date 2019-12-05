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
    * `Obtain the username, email address and profile URL of a user`_
        * `Obtain the username`_
        * `Obtain the primary email address`_
        * `Obtain the user profile URL`_

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

.. seealso::

    To simplify the initialization process, you should consider leveraging the 
    :ref:`supporting-modules:Helper Module (khorosjx.utils.helper)`.

|

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

Obtain the username, email address and profile URL of a user
============================================================
Similar to how you obtain the User ID of a user, you can also retrieve a user's
username, email address and profile URL using simple functions within the
:ref:`primary-modules:Users Module (khorosjx.users)`.  These operations are
explained in the following subsections.

Obtain the username
-------------------
Assuming you have the User ID or email address for a user, you can quickly obtain
their username via the :py:func:`khorosjx.users.get_username` function, as
demonstrated in the examples below.

.. code-block:: python

    username_from_id = khorosjx.users.get_username(1234)
    username_from_email = khorosjx.users.get_username('john.doe@example.com', 'email')

.. note::

    Similar to the :py:func:`khorosjx.users.get_user_id` function, you must provide the
    *lookup type* (e.g. ``email``) as a second argument if not querying with the User ID.

    You may also notice that when leveraging the User ID, you can provide it as either an
    integer or a string value and both will be acceptable.

Obtain the primary email address
--------------------------------
You can quickly retrieve the primary email address for a user by leveraging the
:py:func:`khorosjx.users.get_primary_email` function and supplying the User ID or username
of the user.  This is demonstrated below.

.. code-block:: python

    email_address_from_id = khorosjx.users.get_primary_email(1234)
    email_address_from_username = khorosjx.users.get_primary_email('john_doe', 'username')

.. note::

    As with the other functions above, you must provide the *lookup type* (e.g. ``username``)
    as a second argument if not querying with the User ID. Also in similar fashion, the User ID
    can be provided as either an integer or a string value and both will be acceptable.

Obtain the user profile URL
---------------------------
When you have the username for a user, it is easy to determine the URL of their respective
profile as the URL structure is simply your base URL, the ``people`` endpoint and then the
username.  (e.g. ``https://community.example.com/people/john_doe``)

However, the :py:func:`khorosjx.users.get_profile_url` function makes the process even
easier by constructing the URL for you, and can even do so when supplied a User ID or
email address rather than a username.

All three methods are demonstrated below.

.. code-block:: python

    profile_url_from_id = khorosjx.users.get_profile_url(1234)
    profile_url_from_email = khorosjx.users.get_profile_url('john.doe@example.com', 'email')
    profile_url_from_username = khorosjxusers.get_profile_url('john_doe', 'username')

.. note::

    Despite the profile URL being constructed using the username, functions within this
    module will generally utilize the **User ID** as the primary lookup type as it is the
    main unique identifier leveraged within the Khoros JX / Jive platform.

-----

.. todo::

    The remainder of this document is still in progress. Please check back later
    for updates.