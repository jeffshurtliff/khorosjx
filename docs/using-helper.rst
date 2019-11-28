########################
Using the Helper Utility
########################
This page provides instructions and examples around leveraging the
:ref:`supporting-modules:Helper Module (khorosjx.utils.helper)` which allows a "helper" configuration file
to be imported and parsed to facilitate the use of the library (e.g. defining the base URL and API credentials)
and defining additional settings.

* `What is a helper?`_
* `The configuration file`_
    * `API Connection`_
        * `Supplying credentials in the config file`_
        * `Retrieving credentials using a script function`_
    * `Script Styling`_
* `Initializing the Helper`_
    * `Global Variables`_

*****************
What is a helper?
*****************
When talking about the KhorosJX Python Library, a **helper** is a configuration file which defines various
settings that can be leveraged by the library to simplify the :ref:`core-functionality:Getting Started` process.
It also allows additional features to be enabled in certain circumstances that may be deemed helpful.

|

**********************
The configuration file
**********************
The Helper configuration file is a `YAML <https://en.wikipedia.org/wiki/YAML>`_ file that follows the formatting
shown below.

.. code-block:: yaml

    # Helper configuration file for the khorosjx package

    # Define how to obtain the connection information
    connection:
        base_url: https://community.example.com
        credentials:
            # Uncomment the lines below to provide plaintext credentials
            #
            use_script: no
            username: exampleuser
            password: examplePWD123!

            # Uncomment the lines below to provide the credentials via module
            # for a module and function
            #
            # use_script: yes
            # module_name: jxhelper
            # function_name: get_credentials
            # function_kwargs: username='adminuser'

    # Define whether or not to color-code the function output
    styling:
        use_console_colors: no

.. note::

    In a future release, you will have the ability to utilize a JSON file rather than YAML if preferred.

|

API Connection
==============

The primary functionality of the Helper configuration file is to allow you to define the **Base URL** and the
**API credentials** which are both necessary to leverage the library.  (See :ref:`introduction:Basic Usage`)

This can be done in two different ways:

* Supplying the credentials within the configuration file
* Leveraging another Python module and function to retrieve the credentials.

|

Supplying credentials in the config file
----------------------------------------
If your configuration will be stored in a secure location then you have the option of storing the credentials
directly within the configuration file, as demonstrated in the example above. This method requires the fields
listed below to be defined, which all reside within the **credentials** subsection under the **connection**
section.

**use_script**
    This field specifies whether or not a script (i.e. module/function) will be used to retrieve the credentials
    and should be set to ``no`` in this situation.

**username**
    This field is where you will store the username for the account you will utilize with the Core API.

**password**
    This field is where you will store the corresponding password for the username above.

|

Retrieving credentials using a script function
----------------------------------------------
An an alternative to providing credentials directly within the configuration file, you have the option to
create a module and function (or leverage an existing module and function) to return the credentials needed
for the *khorosjx* library.

This can be done by commenting out (or removing) the section mentioned above in the configuration file for
storing credentials within the file itself and instead uncomment the other section which includes these fields:

**use_script**
    This field specifies whether or not a script (i.e. module/function) will be used to retrieve the credentials
    and should be set to ``yes`` in this situation.

**module_name**
    This field defines the name of the module that must be imported.

**function_name**
    This field defines the name of the function within the module above that will provide the credentials.

**function_kwargs**
    This is an optional field where you can define any keyword arguments that must be defined in order to return
    the appropriate data for the **khorosjx** library.

.. note::

    The configuration file only supports basic keyword arguments (e.g. `username="apiuser"`) with integer, string
    or Boolean values. Non-keyword arguments and values that are lists, tuples, dictionaries or other data types
    are not permitted at this time.

For example, let's assume that you have a package entitled `myutils` with an underlying module entitled `jxhelper`
which lets you return credentials for a specified user.

.. code-block:: python

    # Define function to return credentials for a specific user
    get_credentials(username):
        # Retrieve the credentials from our SQL server database
        un, pw = get_credentials_from_sql(username)
        return un, pw

In this example, if you wanted this function to return credentials for a user with the usrename `adminuser`, then
you would define the values below in the configuration file.

* **use_script:** no
* **module_name:** myutils.jxhelper
* **function_name:** get_credentials
* **function_kwargs:** username='adminuser`

|

Script Styling
==============
A secondary section in the configuration file address **script styling**, with a single option to enable
`console colors <https://www.oreilly.com/library/view/linux-shell-scripting/9781785881985/b0ddd805-aa79-441d-b5a7-3
80c66c7712d.xhtml>`_, which is not currently an enabled feature and will be available in a future release. As such,
the setting in the configuration file is present for future preparation purposes and current has no effect.

|

***********************
Initializing the Helper
***********************
Once the configuration file is created, you can initialize it from the primary module with the syntax below.

.. code-block:: python

    khorosjx.init_helper('/path/to/khorosjx_helper.yml')

This function call will not only initialize the Helper settings as global variables to use throughout the library,
but will also perform the API connection process as well so this will not need to be performed in a separate
function call.

|

Global Variables
================
Once the Helper utility has been initialized, the following global variables become accessible:

**helper_settings**
    A dictionary that includes all settings defined by the utility

**use_console_colors**
    A Boolean value that defines whether console colors should be utilized throughout the library.
    *(Currently has no effect)*