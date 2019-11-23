##########
Change Log
##########

***********
v1.2.0.dev0
***********
**Release Date: TBD**

Added
=====

Primary Modules
---------------
Additions to the `primary modules <primary-modules>`_.

Groups Module
^^^^^^^^^^^^^
* Added the ``add_user_to_group()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.
* Added the ``check_user_membership()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.

-----

Supporting Modules
------------------
Additions to the `supporting modules <supporting-modules>`_.

Core Utilities Module
^^^^^^^^^^^^^^^^^^^^^
* Added the ``eprint()`` function to the :ref:`primary-modules:Core Module (khorosjx.core)` to print error messages.

Exceptions Module
^^^^^^^^^^^^^^^^^
* Added the ``POSTRequestError``, ``InvalidScopeError`` and ``InvalidLookupTypeError`` exception classes to the
  :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`.

Changed
=======
* Updated the classifiers in ``setup.py`` to specifically reference Python 3.6, 3.7 and 3.8.
* Expanded the functionality of the ``check_api_response()`` function in the
  :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)`.

|

******
v1.1.1
******
**Release Date: 2019-11-23**

Added
=====
* Added default messages to all of the exception classes
  in the :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`.
* Added docstrings to the ``overwrite_doc_body()`` function
  in the :ref:`primary-modules:Content Module (khorosjx.content)`.

Changed
=======
* Updated the build workflow (``pythonpackage.yml``) to also test Python 3.8 for compatibility.
* Changed the structure of the change log to match the best practices from
  `keepachangelog.com <https://keepachangelog.com>`_.
* Made minor `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ compliance edits to
  the :ref:`supporting-modules:Classes Module (khorosjx.utils.classes)`.

Removed
=======
* The ``raise_exceptions()`` function is no longer necessary as the exception classes now have
  default messages and has been removed from the ``khorosjx.errors.__init__`` module and the
  :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)`.
* Removed the ``ExceptionMapping`` and ``ExceptionGrouping`` classes from the
  :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)` as they are no longer used.

|

******
v1.1.0
******
**Release Date: 2019-11-22**

Added
=====
Additions that are available in this release.

Primary Modules
---------------
Additions to the `primary modules <primary-modules>`_.

Core Module
^^^^^^^^^^^
* Added the ``put_request_with_retries()`` function to the :ref:`primary-modules:Core Module (khorosjx.core)`.
* Added the ``ignore_exceptions`` parameter in the ``get_data()`` function and replaced the built-in ``ValueError``
  exception with the custom ``GETRequestError`` exception in the :ref:`primary-modules:Core Module (khorosjx.core)`.
* Added the ``get_fields_from_api_response()`` function to the :ref:`primary-modules:Core Module (khorosjx.core)`.

Content Module
^^^^^^^^^^^^^^
* Added the ``overwrite_doc_body()`` function to the :ref:`primary-modules:Content Module (khorosjx.content)`.

Groups Module
^^^^^^^^^^^^^
* Added the ``get_user_memberships()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.
* Added the ``get_group_info()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.
* Added the ``get_all_groups()`` function to the :ref:`primary-modules:Groups Module (khorosjx.groups)`.

Users Module
^^^^^^^^^^^^
* Added the ``get_recent_logins()`` function to the :ref:`primary-modules:Users Module (khorosjx.users)`.

-----

Supporting Modules
------------------
Additions to the `supporting modules <supporting-modules>`_.

Core Utilities Module
^^^^^^^^^^^^^^^^^^^^^
* Added the ``convert_dict_list_to_dataframe()`` function to the
  :ref:`supporting-modules:Core Utilities Module (khorosjx.utils.core_utils)`.

Exceptions Module
^^^^^^^^^^^^^^^^^
* Added the ``ContentPublishError``, ``BadCredentialsError``, ``GETRequestError`` and ``PUTRequestError`` exception
  classes to the :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`.

Handlers Module
^^^^^^^^^^^^^^^
* Added the new :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)` which includes a new
  ``check_api_response()`` function.

Tests Module
^^^^^^^^^^^^
* Created the new :ref:`supporting-modules:Tests Module (khorosjx.utils.tests)` for unit tests to leverage
  with *pytest*.

Changed
=======
* Updated the *Supporting Modules* documentation page to reference the new modules.
* Reformatted the *Change Log* documentation page to follow the
  `Sphinx Style Guide <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html>`_.

Deprecated
==========
* The ``raise_exception()`` function in the ``khorosjx.errors`` module now displays a DeprecationWarning as it has
  been moved into the new `supporting-modules:Handlers Module (khorosjx.errors.handlers)`.
* Added a ``PendingDeprecationWarning`` warning on the ``khorosjx.errors.handlers.raise_exception()`` function as it
  will be deprecated in a future release.  (See `v1.1.1`_)

Fixed
=====
* Added the ``verify_connection()`` function call to the ``get_data()`` function in the
  :ref:`primary-modules:Core Module (khorosjx.core)`.

|

************
v1.0.1.post1
************
**Release Date: 2019-11-19**

Changed
=======
* Created a new :doc:`introduction <introduction>` page with the existing home page content and added
  a :ref:`index:Navigation` to the home page.
* Changed all :doc:`auxilliary modules <supporting-modules>` references to be
  :doc:`supporting modules <supporting-modules>` instead.
* Added a :ref:`introduction:Reporting Issues` section to the :doc:`introduction <introduction>` page and to the
  `README <https://github.com/jeffshurtliff/khorosjx/blob/master/README.md>`_ file.

|

******
v1.0.1
******
**Release Date: 2019-11-19**

Changed
=======
* Removed the version from the individual module header blocks as all will adhere to the primary versioning.


Fixed
=====
* Added missing ``from . import core`` in the ``admin``, ``groups`` and ``spaces`` modules.
