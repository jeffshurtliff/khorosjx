==========
Change Log
==========

v1.1.0.dev2
===========
**Release Date: 2019-11-22*

Enhancements
~~~~~~~~~~~~
* Added the ``BadCredentialsError`` class to the :ref:`Classes Module (khorosjx.utils.classes)`.
* Updated the ``check_api_response()`` function in the :ref:`Handlers Module (khorosjx.errors.handlers)` to
  leverage the ``BadCredentialsError`` exception class.
* Added the ``convert_dict_list_to_dataframe()`` function to the
  :ref:`Core Utilities Module (khorosjx.utils.core_utils)`.

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~
* Updated the *Supporting Modules* page to reference the new :ref:`Handlers Module (khorosjx.errors.handlers)`.


v1.1.0.dev1
===========
**Release Date: 2019-11-22**

Enhancements
~~~~~~~~~~~~
* Added the ``get_fields_from_api_response()`` function to the :ref:`primary-modules:Core Module (khorosjx.core)`.
* Updated the ``groups.get_group_info()`` function to leverage the ``core.get_fields_from_api_response()`` function.
* Added the ``get_all_groups()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.

v1.1.0.dev0
===========
**Release Date: 2019-11-20**

Enhancements
~~~~~~~~~~~~
* Added the ``put_request_with_retries()`` function to the :ref:`primary-modules:Core Module (khorosjx.core)`.
* Added the ``ignore_exceptions`` parameter in the ``get_data()`` function and replaced the built-in ``ValueError``
  exception with the custom ``GETRequestError`` exception in the :ref:`primary-modules:Core Module (khorosjx.core)`.
* Added the ``get_recent_logins()`` function to the :ref:`primary-modules:Users Module (khorosjx.users)`.
* Added the ``overwrite_doc_body()`` function to the :ref:`primary-modules:Content Module (khorosjx.content)`.
* Added the ``get_user_memberships()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.
* Added the ``get_group_info()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.
* Added the ``ContentPublishError``, ``GETRequestError`` and ``PUTRequestError`` exception classes to the
  :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`.
* Added the new `supporting-modules:Handlers Module (khorosjx.errors.handlers)` which includes a new
  ``check_api_response()`` function.

Fixed Bugs
~~~~~~~~~~
* Added the ``verify_connection()`` function call to the ``get_data()`` function in the
  :ref:`primary-modules:Core Module (khorosjx.core)`.

Deprecated
~~~~~~~~~~
* The ``raise_exception()`` function in the ``khorosjx.errors`` module now displays a DeprecationWarning as it has
  been moved into the new `supporting-modules:Handlers Module (khorosjx.errors.handlers)`.


v1.0.1.post1
============
**Release Date: 2019-11-19**

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~
* Created a new :doc:`introduction <introduction>` page with the existing home page content and added
  a :ref:`index:Navigation` to the home page.
* Changed all :doc:`auxilliary modules <supporting-modules>` references to be
  :doc:`supporting modules <supporting-modules>` instead.
* Added a :ref:`introduction:Reporting Issues` section to the :doc:`introduction <introduction>` page and to the
  `README <https://github.com/jeffshurtliff/khorosjx/blob/master/README.md>`_ file.



v1.0.1
======
**Release Date: 2019-11-19**

Developer Changes
~~~~~~~~~~~~~~~~~
* Removed the version from the individual module header blocks as all will adhere to the primary versioning.


Fixed Bugs
~~~~~~~~~~
* Added missing ``from . import core`` in the ``admin``, ``groups`` and ``spaces`` modules.

