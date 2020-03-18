==================
Supporting Modules
==================
This section provides details around the supporting modules used in the **khorosjx** package,
which are listed below.

* `Tools and Utilities`_
    * `Core Utilities Module (khorosjx.utils.core_utils)`_
    * `Dataframe Utilities Module (khorosjx.utils.df_utils)`_
    * `Helper Module (khorosjx.utils.helper)`_
    * `Tests Module (khorosjx.utils.tests)`_
    * `Version Module (khorosjx.utils.version)`_
* `Classes and Exceptions`_
    * `Classes Module (khorosjx.utils.classes)`_
    * `Errors Module (khorosjx.errors)`_
        * `Exceptions Module (khorosjx.errors.exceptions)`_
        * `Handlers Module (khorosjx.errors.handlers)`_

|

Tools and Utilities
===================
This section includes modules that contain tools and utilities leveraged by other scripts.

|

Core Utilities Module (khorosjx.utils.core_utils)
-------------------------------------------------
This module includes various utilities to assist in converting dictionaries to JSON, 
formatting timestamps, etc.

.. automodule:: khorosjx.utils.core_utils
   :members:

:doc:`Return to Top <supporting-modules>`

|

Dataframe Utilities Module (khorosjx.utils.df_utils)
----------------------------------------------------
This module includes various utilities to assist in creating, importing, exporting and manipulating
pandas dataframes.

.. automodule:: khorosjx.utils.df_utils
   :members:

:doc:`Return to Top <supporting-modules>`

|

Helper Module (khorosjx.utils.helper)
-------------------------------------
This module includes allows a "helper" configuration file to be imported and parsed to
facilitate the use of the library (e.g. defining the base URL and API credentials) and
defining additional settings.

.. automodule:: khorosjx.utils.helper
   :members:

:doc:`Return to Top <supporting-modules>`

|

Tests Module (khorosjx.utils.tests)
-----------------------------------
This module includes unit tests for the package that are performed using pytest.

**Test Module Import (khorosjx.utils.tests.test_init_module)**

.. automodule:: khorosjx.utils.tests.test_init_module
   :members:

:doc:`Return to Top <supporting-modules>`

|

Version Module (khorosjx.utils.version)
---------------------------------------
This module is the primary source of the current version of the khorosjx package, and includes two simple
functions to return either the full version or the major.minor (i.e. X.Y) version.

.. automodule:: khorosjx.utils.version
   :members:

:doc:`Return to Top <supporting-modules>`

|

Classes and Exceptions
======================
This section includes modules that contain the classes and exceptions used in the package.

|

Classes Module (khorosjx.utils.classes)
---------------------------------------
This module contains nearly all classes utilized by other modules within the library.

.. automodule:: khorosjx.utils.classes
   :members:

:doc:`Return to Top <supporting-modules>`

|

Errors Module (khorosjx.errors)
-------------------------------
This module contains all of the exception classes and error handling functions leveraged throughout the library.

.. automodule:: khorosjx.errors
   :members:

|

Exceptions Module (khorosjx.errors.exceptions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This sub-module contains all of the exception classes leveraged in functions throughout
the library.

.. automodule:: khorosjx.errors.exceptions
   :members:

:doc:`Return to Top <supporting-modules>`

|

Handlers Module (khorosjx.errors.handlers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This sub-module contains various error handling functions that are leveraged throughout
the library.

.. automodule:: khorosjx.errors.handlers
   :members:

:doc:`Return to Top <supporting-modules>`
