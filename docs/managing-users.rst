##############
Managing Users
##############

.. warning::

    This page is currently in development.

This page has instructions relating to managing users within a
KhorosJX (or Jive-n) community, including tasks such as obtaining
user information and statistics and other similar operations.

.. note::

    The tutorials within this page all assume that a connection has
    already been established using the information found in the
    :ref:`core-functionality:getting-started` section of the
    documentation.

***************************
Leveraging the Users Module
***************************
In order to leverage the Users Module (and any other module within the
khorosjx library) you must first perform the following steps:

1. Import the high-level **khorosjx** package.
2. Initialize the **users** module.
3. Establish the connection to the environment.


**************************
Obtaining User information
**************************
This section addresses how you can obtain information about a user to
use in other administrative functions and/or to obtain for statistical
purposes.

Obtain the User ID of a User
============================
The User ID value is a unique identifier within the KhorosJX / Jive environment
which identifies a user and allows the platform--as well as third-party
integrations via the API--to take actions against the user in various
capacities.

However, sometimes the User ID for a user is not readily available and you only
have their email address. In these situations, the ``get_user_id()`` function
can be used to retrieve the needed User ID, as shown in the example below.

..code-block:: python
    
    user_id = 
