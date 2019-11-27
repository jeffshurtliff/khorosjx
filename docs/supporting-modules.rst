==================
Supporting Modules
==================
This section provides details around the supporting modules used in the **khorosjx** package,
which are listed below.

* `Core Utilities Module (khorosjx.utils.core_utils)`_
* `Classes Module (khorosjx.utils.classes)`_
* `Exceptions Module (khorosjx.errors.exceptions)`_
* `Handlers Module (khorosjx.errors.handlers)`_
* `Tests Module (khorosjx.utils.tests)`_

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

Helper Module (khorosjx.utils.helper)
-------------------------------------
This module includes allows a "helper" configuration file to be imported and parsed to
facilitate the use of the library (e.g. defining the base URL and API credentials) and
defining additional settings.

.. automodule:: khorosjx.utils.helper
    :members:

Tests Module (khorosjx.utils.tests)
-----------------------------------
This module includes unit tests for the package that are performed using pytest.

**Test Module Import (khorosjx.utils.tests.test_init_module)**

.. automodule:: khorosjx.utils.tests.test_init_module
    :members:

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

|

Exceptions Module (khorosjx.errors.exceptions)
----------------------------------------------
This module contains all of the exception classes leveraged in functions throughout 
the library.

.. automodule:: khorosjx.errors.exceptions
    :members:

Handlers Module (khorosjx.errors.handlers)
------------------------------------------
This module contains various error handling functions that are leveraged throughout
the library.

.. automodule:: khorosjx.errors.handlers
    :members:
