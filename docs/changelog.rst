##########
Change Log
##########

******
v1.4.0
******
**Release Date: 2019-11-30**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.core.get_paginated_results` function.
* Added docstrings to the :py:func:`khorosjx.core.get_fields_from_api_response` function.
* Added the :py:func:`khorosjx.groups.get_group_memberships` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.utils.core_utils.add_to_master_list` function.
* Added the :py:func:`khorosjx.utils.core_utils.convert_single_pair_dict_list` function.
* Added docstrings to the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function.
* Added the new :py:class:`khorosjx.utils.classes.Groups` class which contains the ``membership_types``
  and ``user_type_mapping`` dictionaries.
* Added the ``people_fields`` list to the :py:class:`khorosjx.utils.classes.FieldLists` class.

Changed
=======

Supporting Modules
------------------
Changes in the :doc:`supporting modules <supporting-modules>`.

* Added a ``TODO`` note to move the :py:func:`khorosjx.utils.core_utils.eprint` function to
  the :py:mod:`khorosjx.errors.handlers` module.

Documentation
-------------
* Changed the structure of the changelog to be more concise. (i.e. less sub-sections)

Developer Changes
-----------------
* Changed the **Development Status** `classifier <https://pypi.org/classifiers>`_ from ``Alpha`` to ``Beta`` in the
  `setup.py <https://github.com/jeffshurtliff/khorosjx/blob/master/setup.py>`_ file.

Removed
=======

Primary Modules
---------------
Removals in the :doc:`primary modules <primary-modules>`.

* Removed the internal function ``add_to_master_list()`` from within the
  :py:func:`khorosjx.groups.get_all_groups` function.

|

******
v1.3.0
******
**Release Date: 2019-11-27**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the ``init_helper()`` function to the
  `khorosjx/__init__.py <https://github.com/jeffshurtliff/khorosjx/blob/master/khorosjx/__init__.py>`_ file to
  initialize a helper configuration file.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the new :ref:`supporting-modules:Helper Module (khorosjx.utils.helper)` which allows a "helper"
  configuration file to be imported and parsed to facilitate the use of the library (e.g. defining the base URL and
  API credentials) and defining additional settings.
* Added the new :py:exc:`khorosjx.errors.exceptions.InvalidHelperArgumentsError` and
  :py:exc:`khorosjx.errors.exceptions.HelperFunctionNotFoundError` exception classes.

-----

Examples
--------
* Added a new `examples <https://github.com/jeffshurtliff/khorosjx/tree/master/examples>`_ directory containing the
  `khorosjx_helper.yml <https://github.com/jeffshurtliff/khorosjx/blob/master/examples/khorosjx_helper.yml>`_ file
  which demonstrates how the helper configuration file should be formatted.

-----

Documentation
-------------
* Added the :ref:`using-helper:Using the Helper Utility` page to address the new Helper Utility that was introduced.
* Added the :ref:`supporting-modules:Helper Module (khorosjx.utils.helper)` to the
  :doc:`Supporting Modules<supporting-modules>` page.
* Added a "See Also" section mentioning the Helper Utility on the :doc:`Core Functionality <core-functionality>` page.

|

******
v1.2.0
******
**Release Date: 2019-11-24**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the internal ``__api_request_with_payload()`` function in the :py:mod:`khorosjx.core` module to leverage
  for both POST and PUT requests.
* Added the :py:func:`khorosjx.core.post_request_with_retries` function for POST requests, which leverages the
  internal function above.
* Added the :py:func:`khorosjx.groups.add_user_to_group` function.
* Added the :py:func:`khorosjx.groups.check_user_membership` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.utils.core_utils.eprint` function to print error messages to stderr and onscreen.
* Added the :py:exc:`khorosjx.errors.exceptions.POSTRequestError`,
  :py:exc:`khorosjx.errors.exceptions.InvalidScopeError`, :py:exc:`khorosjx.errors.exceptions.InvalidLookupTypeError`,
  :py:exc:`khorosjx.errors.exceptions.InvalidEndpointError`,
  :py:exc:`khorosjx.errors.exceptions.InvalidRequestTypeError` and
  :py:exc:`khorosjx.errors.exceptions.APIConnectionError` exception classes.

-----

Documentation
-------------
* Added the :doc:`Core Functionality <core-functionality>` page with instructions on leveraging the core
  functionality of the library. (Page is still a work in progress)
* Added the :doc:`Managing Users <managing-users>` page with instructions on managing users by leveraging
  the library. (Page is still a work in progress)
* Added the :doc:`Basic Usage <basic-usage>` page with the intent of inserting it into more than one page.

Changed
=======

General
-------
* Updated the classifiers in `setup.py <https://github.com/jeffshurtliff/khorosjx/blob/master/setup.py>`_
  to specifically reference Python 3.6, 3.7 and 3.8.

-----

Primary Modules
---------------
Changes to existing functions in the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khorosjx.core.get_data` function to accept ``username`` as an identifier for the
  ``people`` endpoint.
* Updated the :py:func:`khorosjx.core.get_request_with_retries` function to include the ``return_json`` optional
  argument. (Disabled by default)
* Refactored the :py:func:`khorosjx.core.put_request_with_retries` function to leverage the internal
  ``__api_request_with_payload()`` function.
* Updated the :py:func:`khorosjx.users.get_user_id` function to accept a username as well as an email address.

-----

Supporting Modules
------------------
Changes to existing functions in the :doc:`supporting modules <supporting-modules>`.

* Expanded the functionality of the :py:func:`khorosjx.errors.handlers.check_api_response` function.

-----

Documentation
-------------
* Updated the :doc:`Introduction <introduction>` page to insert the :ref:`introduction:Basic Usage` content.
* Added the :doc:`Basic Usage <basic-usage>` page with the intent of inserting it into more than one page.

|

******
v1.1.1
******
**Release Date: 2019-11-23**

Added
=====
* Added default messages to all of the exception classes
  in the :ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`.
* Added docstrings to the :py:func:`khorosjx.content.overwrite_doc_body` function.

Changed
=======
* Updated the build workflow
  (`pythonpackage.yml <https://github.com/jeffshurtliff/khorosjx/blob/master/.github/workflows/pythonpackage.yml>`_)
  to also test Python 3.8 for compatibility.
* Changed the structure of the change log to match the best practices from
  `keepachangelog.com <https://keepachangelog.com>`_.
* Made minor `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ compliance edits to
  the :ref:`supporting-modules:Classes Module (khorosjx.utils.classes)`.

Removed
=======
* The ``raise_exceptions()`` function is no longer necessary as the exception classes now have
  default messages and has been removed from the :py:mod:`khorosjx.errors` module
  (`__init__.py <https://github.com/jeffshurtliff/khorosjx/blob/master/khorosjx/errors/__init__.py>`_) and the
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

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.core.put_request_with_retries` function.
* Added the ``ignore_exceptions`` parameter in the :py:func:`khorosjx.core.get_data` function and replaced the
  built-in `ValueError <https://docs.python.org/3/library/exceptions.html#ValueError>`_ exception with the
  custom :py:exc:`khorosjx.errors.exceptions.GETRequestError` exception class.
* Added the :py:func:`khorosjx.core.get_fields_from_api_response` function.
* Added the :py:func:`khorosjx.content.overwrite_doc_body` function.
* Added the :py:func:`khorosjx.groups.get_user_memberships` function.
* Added the :py:func:`khorosjx.groups.get_group_info` function.
* Added the :py:func:`khorosjx.groups.get_all_groups` function.
* Added the :py:func:`khorosjx.users.get_recent_logins` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function.
* Added the :py:exc:`khorosjx.errors.exceptions.ContentPublishError`,
  :py:exc:`khorosjx.errors.exceptions.BadCredentialsError`, :py:exc:`khorosjx.errors.exceptions.GETRequestError`
  and :py:exc:`khorosjx.errors.exceptions.PUTRequestError` exception classes.
* Added the new :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)` which includes a new
  :py:func:`khorosjx.errors.handlers.check_api_response` function.
* Created the new :ref:`supporting-modules:Tests Module (khorosjx.utils.tests)` for unit tests to leverage
  with `pytest <https://docs.pytest.org/en/latest/>`_.

Changed
=======
* Updated the :doc:`Supporting Modules <supporting-modules>` documentation page to reference the new modules.
* Reformatted the :doc:`Change Log <changelog>` documentation page to follow the
  `Sphinx Style Guide <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html>`_.

Deprecated
==========
* The ``raise_exception()`` function in the ``khorosjx.errors`` module now displays a ``DeprecationWarning`` as it has
  been moved into the new :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)`.
* Added a ``PendingDeprecationWarning`` warning on the ``khorosjx.errors.handlers.raise_exception()`` function as it
  will be deprecated in a future release.  (See `v1.1.1`_)

Fixed
=====
* Added the :py:func:`khorosjx.core.verify_connection` function call to the :py:func:`khorosjx.core.get_data` function.

|

************
v1.0.1.post1
************
**Release Date: 2019-11-19**

Changed
=======
* Created a new :doc:`Introduction <introduction>` page with the existing home page content and added
  a :ref:`index:Navigation` (i.e. Table of Contents) to the home page.
* Changed all :doc:`auxilliary modules <supporting-modules>` references to be
  :doc:`supporting modules <supporting-modules>` instead.
* Added a :ref:`introduction:Reporting Issues` section to the :doc:`Introduction <introduction>` page and to the
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