##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v2.3.0
******
**Release Date: 2020-02-11**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`khorosjx.news` module with the following functions:
    * :py:func:`khorosjx.news.verify_core_connection`
    * :py:func:`khorosjx.news.get_all_publications`
    * :py:func:`khorosjx.news.get_publication`
    * :py:func:`khorosjx.news.delete_publication`
    * :py:func:`khorosjx.news.get_subscription_data`
    * :py:func:`khorosjx.news.get_subscription_ids`
    * :py:func:`khorosjx.news.get_subscriber_groups`
    * :py:func:`khorosjx.news.get_subscribers`
    * :py:func:`khorosjx.news.rebuild_publication`
    * :py:func:`khorosjx.news.get_stream`
    * :py:func:`khorosjx.news.update_stream`
    * :py:func:`khorosjx.news.delete_stream`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the ``publication_fields``, ``subscription_fields`` and ``stream_fields`` lists to the
  :py:class:`khorosjx.utils.classes.FieldLists` class.
* Added the :py:exc:`khorosjx.errors.exceptions.SubscriptionNotFoundError` exception class.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`khorosjx.news` module to the ``__all__`` special variable in the primary :py:mod:`khorosjx` module.
* Updated the :py:func:`khorosjx.init_module` function to be compatible with the :py:mod:`khorosjx.news` module.
* Updated the :py:func:`khorosjx.core.get_data` function to include the ``all_fields`` argument. (``False`` by default)
* Referenced the :py:exc:`khorosjx.errors.exceptions.POSTRequestError` exception class in the docstring for the
  :py:func:`khorosjx.core.post_request_with_retries` function.
* Referenced the :py:exc:`khorosjx.errors.exceptions.PUTRequestError` exception class in the docstring for the
  :py:func:`khorosjx.core.put_request_with_retries` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added a ``DeprecationWarning`` to the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Changed the ``json_payload`` type to ``dict`` in the docstring for the
  :py:func:`khorosjx.core.put_request_with_retries` and :py:func:`khorosjx.core.post_request_with_retries` functions.

|

******
v2.2.0
******
**Release Date: 2020-01-22**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.core.get_base_url` function.
* Added the :py:func:`khorosjx.core.get_query_url` function.
* Added the :py:func:`khorosjx.core.__get_filter_syntax` function.
* Added the :py:func:`khorosjx.content.videos.get_video_id` function.
* Added the :py:func:`khorosjx.content.videos.get_native_videos_for_space` function.
* Added the :py:func:`khorosjx.content.videos.find_video_attachments` function.
* Added the :py:func:`khorosjx.content.videos.__construct_url_from_id` function.
* Added the :py:func:`khorosjx.content.videos.check_if_embedded` function.
* Added the :py:func:`khorosjx.content.videos.get_video_dimensions` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the ``video_fields`` list to the :py:class:`khorosjx.utils.classes.FieldLists` class.
* Added the ``video`` key value pair to the ``datasets`` dictionary within the
  :py:class:`khorosjx.utils.classes.Content` class.
* Added the :py:func:`khorosjx.errors.handlers.bad_lookup_type` function.
* Added the :py:exc:`khorosjx.errors.exceptions.ContentNotFoundError` exception.

Changed
=======

General
-------
* Updated `setup.py <https://github.com/jeffshurtliff/khorosjx/blob/master/setup.py>`_ to define ``version`` in the
  :py:func:`setuptools.setup` function using the ``__version__`` value from :py:func:`khorosjx.utils.version`.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khorosjx.core.get_paginated_results` function to allow additional filters to be supplied as
  a tuple containing the element and criteria (e.g. ``('type', 'video')`` or a list of tuples for multiple filters.
* Made minor adjustment to the :py:func:`khorosjx.groups.get_all_groups` function.
* Updated the :py:func:`khorosjx.content.videos.get_content_id` function to allow a URL or Video ID to be supplied.
* Updated the :py:func:`khorosjx.content.base.get_content_id` function to raise the
  :py:exc:`khorosjx.errors.exceptions.ContentNotFoundError` exception instead of a generic ``KeyError`` exception.

******
v2.1.0
******
**Release Date: 16 Jan 2020**

Added
=====

General
-------
* Added the ``__version__`` global variable in the :py:mod:`khorosjx` (``__init__.py``) module.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.core.delete` function.
* Added the :py:func:`khorosjx.content.docs.create_document` function.
* Added the :py:func:`khorosjx.content.docs.delete_document` function.
* Added the :py:func:`khorosjx.places.base.get_uri_for_id` function.
* Added the :py:func:`khorosjx.content.docs.get_url_for_id` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.utils.helper.__get_modules_to_import` function.
* Added the :py:exc:`khorosjx.errors.exceptions.DatasetNotFoundError` exception class.
* Added the ``uri_dataset_mapping`` and ``security_group_uri_map`` dictionaries to the
  :py:class:`khorosjx.utils.classes.Content` class.
* Added the :py:func:`khorosjx.utils.core_utils.identify_dataset` function with the accompanying internal functions:
    * :py:func:`khorosjx.utils.core_utils.__get_security_group_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_invite_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_metadata_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_moderation_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_search_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_support_center_dataset`
    * :py:func:`khorosjx.utils.core_utils.__get_tile_dataset`
* Added the :py:mod:`khorosjx.utils.version` module containing the source ``__version__`` and the following functions:
    * :py:func:`khorosjx.utils.version.get_full_version()`
    * :py:func:`khorosjx.utils.version.get_major_minor_version()`

Changed
=======

General
-------
* Updated `setup.py <https://github.com/jeffshurtliff/khorosjx/blob/master/setup.py>`_ to obtain the ``version``
  value from the :py:func:`khorosjx.utils.version` function.
* Updated `docs/conf.py <https://github.com/jeffshurtliff/khorosjx/blob/master/docs/conf.py>`_ to obtain
  the ``version`` value from the :py:func:`khorosjx.utils.version` function.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:mod:`khorosjx.places` module to proactively import the :py:mod:`khorosjx.places.base`,
  :py:mod:`khorosjx.places.blogs` and :py:mod:`khorosjx.places.spaces` modules.
* Updated the :py:func:`khorosjx.content.docs.get_content_id` function to accept both URLs and Document IDs.
* Updated the :py:func:`khorosjx.init_helper` function to handle the ``modules`` section of the YAML configuration file.
* Added error handling for invalid file types in the :py:func:`khorosjx.init_helper` function.
* Updated the :py:func:`khorosjx.init_module` function to properly handle the ``all`` string within an iterable.
* Updated the :py:func:`khorosjx.core.get_fields_from_api_response` to reference the ``datasets`` dictionary that was
  moved into the :py:class:`khorosjx.utils.classes.Content` class.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khorosjx.utils.helper.parse_helper_cfg` and
  :py:func:`khorosjx.utils.helper.retrieve_helper_settings` functions to leverage the
  :py:func:`khorosjx.utils.helper.__get_modules_to_import` function.
* Added the ``accepted_import_modules`` and ``all_modules`` lists to the
  :py:class:`khorosjx.utils.helper.HelperParsing` class.
* Moved the ``datasets`` dictionary from the :py:func:`khorosjx.core.get_fields_from_api_response` function into the
  :py:class:`khorosjx.utils.classes.Content` class.

Documentation
-------------
Changes to the documentation.

* Adjusted the docstring for the :py:exc:`khorosjx.errors.exceptions.InvalidDatasetError` exception class to
  differentiate it from the :py:exc:`khorosjx.errors.exceptions.DatasetNotFoundError` exception class.

Examples
--------
Changes to the example files found in the `examples <https://github.com/jeffshurtliff/khorosjx/tree/master/examples>`_
directory within the GitHub repository.

* Added the ``modules`` section to the
  `khorosjx_helper.yml <https://github.com/jeffshurtliff/khorosjx/blob/master/examples/khorosjx_helper.yml>`_ file.

|

******
v2.0.0
******
**Release Date: 8 Jan 2020**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Created the :py:mod:`khorosjx.places` module with the following sub-modules and functions:
    * :py:mod:`khorosjx.places.base`
        * :py:func:`khorosjx.places.base.verify_core_connection`
        * :py:func:`khorosjx.places.base.get_browse_id`
        * :py:func:`khorosjx.places.base.get_place_id`
        * :py:func:`khorosjx.places.base.get_place_info`
        * :py:func:`khorosjx.places.base.get_places_list_from_file`
    * :py:mod:`khorosjx.places.spaces`
        * :py:func:`khorosjx.places.spaces.verify_core_connection`
        * :py:func:`khorosjx.places.spaces.get_space_info`
        * :py:func:`khorosjx.places.spaces.get_permitted_content_types`
        * :py:func:`khorosjx.places.spaces.get_space_permissions`
    * :py:mod:`khorosjx.places.blogs`
        * :py:func:`khorosjx.places.blogs.verify_core_connection`
        * :py:func:`khorosjx.places.blogs.get_blog_info`
* Created the :py:mod:`khorosjx.content` module with the following sub-modules and functions:
    * :py:mod:`khorosjx.content.base`
        * :py:func:`khorosjx.content.base.verify_core_connection`
        * :py:func:`khorosjx.content.base.get_content_id`
        * :py:func:`khorosjx.content.base.__convert_lookup_value`
        * :py:func:`khorosjx.content.base.__trim_attachments_info`
    * :py:mod:`khorosjx.content.docs`
        * :py:func:`khorosjx.content.docs.verify_core_connection`
        * :py:func:`khorosjx.content.docs.get_content_id`
        * :py:func:`khorosjx.content.docs.overwrite_doc_body`
        * :py:func:`khorosjx.content.docs.get_document_info`
        * :py:func:`khorosjx.content.docs.get_document_attachments`
    * :py:mod:`khorosjx.content.events`
        * :py:func:`khorosjx.content.events.verify_core_connection`
        * :py:func:`khorosjx.content.events.get_content_id`
    * :py:mod:`khorosjx.content.ideas`
        * :py:func:`khorosjx.content.ideas.verify_core_connection`
        * :py:func:`khorosjx.content.ideas.get_content_id`
    * :py:mod:`khorosjx.content.threads`
        * :py:func:`khorosjx.content.threads.verify_core_connection`
        * :py:func:`khorosjx.content.threads.get_content_id`
    * :py:mod:`khorosjx.content.videos`
        * :py:func:`khorosjx.content.videos.verify_core_connection`
        * :py:func:`khorosjx.content.videos.get_content_id`
* Added the :py:func:`khorosjx.content.videos.download_video` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.utils.core_utils.print_if_verbose` function.
* Added the ``permitted_video_file_types`` list to the :py:class:`khorosjx.utils.classes.Content` class.

Documentation
-------------
Additions to the documentation.

* Added "Return to Top" hyperlinks on the :doc:`primary modules <primary-modules>`,
  :doc:`supporting modules <supporting-modules>` and :doc:`change log <changelog>` pages.
* Added the :py:mod:`khorosjx.utils.df_utils` and :py:mod:`khorosjx.errors` modules to the
  :doc:`supporting modules <supporting-modules>` page.

Changed
=======

General
-------
* Changed the ``Development Status`` PyPI classifier in the
  `setup.py <https://github.com/jeffshurtliff/khorosjx/blob/master/setup.py>`_ file to be ``5 - Production/Stable``.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Included the ``blog`` and ``place`` datasets in the dictionary within the
  :py:func:`khorosjx.core.get_fields_from_api_response` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added ``df_utils`` and ``helper`` to ``__all__`` in the :py:mod:`khorosjx.utils` module.

Documentation
-------------
Changes to the documentation.

* Updated the :doc:`Primary Modules <primary-modules>` page to show functions within the ``__init__.py`` files.
* Added ``deprecated`` directives to docstrings of deprecated functions.
* Adjusted the docstrings on the :py:func:`khorosjx.init_helper` function.
* Restructured the table of contents at the top of the :doc:`Supporting Modules <supporting-modules>` page.
* Updated the short-term and long-term items on the :doc:`Roadmap <roadmap>` page.

Fixed
=====

Primary Modules
---------------
Fixes applied in the :doc:`primary modules <primary-modules>`.

* Fixed the try/except in the :py:func:`khorosjx.content.docs.get_document_attachments` function to account for both
  ``KeyError`` and ``IndexError`` exceptions instead of just the latter.

Supporting Modules
------------------
Fixes applied in the :doc:`supporting modules <supporting-modules>`.

* Fixed the :py:func:`khorosjx.errors.handlers.check_api_response` function so that a 502 response code displays a
  simple ``Site Temporarily Unavailable`` error rather than displaying the entire raw HTML response from the API.

Documentation
-------------
Fixes applied to the documentation.

* Fixed an issue with the header block docstring for the :py:mod:`khorosjx.utils.classes` module.

Deprecated
==========

Primary Modules
---------------
Deprecations in the :doc:`primary modules <primary-modules>`.

* Deprecated and moved the functions below to the
  `khorosjx/content/__init__.py <https://github.com/jeffshurtliff/khorosjx/blob/master/khorosjx/content.py>`_ file
  from the removed `khorosjx/content.py <https://github.com/jeffshurtliff/khorosjx/commits/master/khorosjx/content.py>`_
  file. (The deprecated functions will be removed in v3.0.0.)

    * :py:func:`khorosjx.content.get_content_id`
    * :py:func:`khorosjx.content.overwrite_doc_body`
    * :py:func:`khorosjx.content.__convert_lookup_value`
    * :py:func:`khorosjx.content.get_document_info`
    * :py:func:`khorosjx.content.__trim_attachments_info`
    * :py:func:`khorosjx.content.get_document_attachments`

* Deprecated the :py:func:`khorosjx.spaces.get_space_info` function.
* Deprecated the :py:func:`khorosjx.spaces.get_place_id` function.
* Deprecated the :py:func:`khorosjx.spaces.get_browse_id` function.
* Deprecated the :py:func:`khorosjx.spaces.__verify_browse_id` function.
* Deprecated the :py:func:`khorosjx.spaces.get_spaces_list_from_file` function.
* Deprecated the :py:func:`khorosjx.spaces.get_permitted_content_types` function.
* Deprecated the :py:func:`khorosjx.spaces.get_space_permissions` function.
* Deprecated the :py:func:`khorosjx.spaces.__get_unique_permission_fields` function.
* Deprecated the :py:func:`khorosjx.spaces.__generate_permissions_dataframe` function.

Removed
=======

Primary Modules
---------------
Removals in the :doc:`primary modules <primary-modules>`.

* The :py:mod:`khorosjx.content` module has been removed. (See the previous sections for additional context.)

:doc:`Return to Top <changelog>`

|

******
v1.7.0
******
**Release Date: 2019-12-21**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.spaces.get_spaces_list_from_file` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the new :py:mod:`khorosjx.utils.df_utils` module to house all pandas-related functions and utilities.
* Added the :py:func:`khorosjx.utils.df_utils.convert_dict_list_to_dataframe` function. (Moved from the
  :py:mod:`khorosjx.utils.core_utils` module.)
* Added the :py:func:`khorosjx.utils.df_utils.import_csv` function.
* Added the :py:func:`khorosjx.utils.df_utils.import_excel` function.
* Added the :py:exc:`khorosjx.errors.exceptions.InvalidFileTypeError` exception class.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khorosjx.core.get_fields_from_api_response` function to handle the ``resources.html.ref`` field.

-----

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function to leverage the
  :py:func:`khorosjx.utils.df_utils.convert_dict_list_to_dataframe` function in the new module.
* Updated the ``place_fields`` list in the :py:class:`khorosjx.utils.classes.FieldLists` class to include the
  ``resources.html.ref`` field.

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Fixed a logic error in the :py:func:`khorosjx.core.get_fields_from_api_response` function which was preventing
  custom-curated fields for nested values from returning properly.


Deprecated
==========

Supporting Modules
------------------
Deprecations in the :doc:`supporting modules <supporting-modules>`.

* Deprecated the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function as it now resides in the
  :py:func:`khorosjx.utils.df_utils.convert_dict_list_to_dataframe` function within the new module.

:doc:`Return to Top <changelog>`

|

******
v1.6.0
******
**Release Date: 2019-12-17**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khorosjx.spaces.get_permitted_content_types` function.
* Added the internal :py:func:`khorosjx.spaces._verify_browse_id` function.
* Added the :py:func:`khorosjx.spaces.get_space_permissions` function.
* Added the internal :py:func:`khorosjx.spaces.__get_unique_permission_fields` function.
* Added the internal :py:func:`khorosjx.spaces.__generate_permissions_dataframe` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khorosjx.errors.handlers.check_json_for_error` function.
* Added the :py:class:`khorosjx.errors.exceptions.NotFoundResponseError` exception class.
* Added the :py:class:`khorosjx.errors.exceptions.SpaceNotFoundError` exception class.

-----

Documentation
-------------
Addition to the documentation in this release.

* Added a :doc:`Roadmap <roadmap>` page to list upcoming enhancements and changes.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khorosjx.init_module` function to allow the ``all`` string to be passed which
  imports all modules.

-----

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added the optional ``column_names`` keyword argument in the
  :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function.

-----

Documentation
-------------
Changes to the documentation in this release.

* Changed the project name from ``KhorosJX`` to ``Khoros JX Python Library`` in the
  `conf.py <https://github.com/jeffshurtliff/khorosjx/blob/master/docs/conf.py>`_ script.
* Made adjustments to the ``toctree`` directives on the :doc:`index <index>` page.
* Changed the **Latest Release** badge in the
  `README.md <https://github.com/jeffshurtliff/khorosjx/blob/master/README.md>`_ file to be labeled
  **Latest Stable Release** instead.


Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Removed ``helper`` from ``__all__`` in the :ref:`primary-modules:Init Module (khorosjx)`.
* Fixed how to query URL was generated in the :py:func:`khorosjx.core.get_api_info` function.
* Fixed a docstring error in the :py:func:`khorosjx.core.put_request_with_retries` function.
* Fixed a minor docstring error in :py:func:`khorosjx.groups.add_user_to_group` function.
* Fixed a docstring error in the :py:func:`khorosjx.users.get_people_followed` function.
* Added the missing ``verify_core_connection()`` function call in :py:func:`khorosjx.users.get_recent_logins`
  function. (See `Issue #1 <https://github.com/jeffshurtliff/khorosjx/issues/1>`_)

-----

Supporting Modules
------------------
Fixes to the :doc:`supporting modules <supporting-modules>`.

* Removed the ``**kwargs`` argument in the ``super()`` call within all custom exceptions.

-----

Documentation
-------------
Fixes in the documentation in this release.

* Fixed minor typos in the `README.md <https://github.com/jeffshurtliff/khorosjx/blob/master/README.md>`_ file.
* Fixed a minor typo in the :py:func:`khorosjx.utils.core_utils.convert_dict_list_to_dataframe` function docstring.

:doc:`Return to Top <changelog>`

|

******
v1.5.0
******
**Release Date: 2019-12-05**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added to the ``datasets`` dictionary and a "field not found" error message in the
  :py:func:`khorosjx.core.get_fields_from_api_response` function.
* Added the :py:func:`khorosjx.content.get_document_info` function.
* Added the :py:func:`khorosjx.content.get_document_attachments` function.
* Added the internal :py:func:`khorosjx.content.__convert_lookup_value` function.
* Added the internal :py:func:`khorosjx.content.__trim_attachments_info` function.
* Added the :py:func:`khorosjx.spaces.get_space_info` function.
* Added the :py:func:`khorosjx.spaces.get_place_id` and :py:func:`khorosjx.spaces.get_browse_id` functions.
* Added the internal :py:func:`khorosjx.users.__validate_lookup_type` function.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the ``place_fields`` and ``document_fields`` lists to the :py:class:`khorosjx.utils.classes.FieldLists` class.
* Added the :py:exc:`khorosjx.errors.exceptions.LookupMismatchError` exception class.
* Added the :py:exc:`khorosjx.errors.exceptions.CurrentlyUnsupportedError` exception class.

-----

Documentation
-------------
* Added the section on how to :ref:`managing-users:obtain the primary email address` within the
  :doc:`Managing Users <managing-users>` page now that the function is available.

Changed
=======
* Updated the :py:func:`khorosjx.users.get_user_id` and :py:func:`khorosjx.users.get_username` functions to leverage
  the internal :py:func:`khorosjx.users.__validate_lookup_type` function.
* Updated the :py:func:`khorosjx.users.get_user_id` function to confirm that an email address was provided if the
  'email' lookup type is supplied.
* Updated the header block docstring at the top of the :py:func:`khorosjx.spaces` module.
* Updated the header block docstring at the top of the :py:func:`khorosjx.errors.exceptions` module.

Fixed
=====
* Fixed a variable name error in the :py:func:`khorosjx.users.get_username` function.

:doc:`Return to Top <changelog>`

|

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

* Removed the nested ``add_to_master_list()`` function from within the
  :py:func:`khorosjx.groups.get_all_groups` function.

:doc:`Return to Top <changelog>`

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

* Added the ``init_helper()`` function to the :ref:`primary-modules:Init Module (khorosjx)`
  to initialize a helper configuration file.

-----

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the new :ref:`supporting-modules:Helper Module (khorosjx.utils.helper)` which allows a "helper"
  configuration file to be imported and parsed to facilitate the use of the library (e.g. defining the base URL and
  API credentials) and defining additional settings.
* Added the :py:exc:`khorosjx.errors.exceptions.InvalidHelperArgumentsError` exception class.
* Added the :py:exc:`khorosjx.errors.exceptions.HelperFunctionNotFoundError` exception class.

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

:doc:`Return to Top <changelog>`

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

* Added the :py:func:`khorosjx.core.__api_request_with_payload` function to leverage for both POST and PUT requests.
* Added the :py:func:`khorosjx.core.post_request_with_retries` function for POST requests, which leverages the
  private function above.
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
* Refactored the :py:func:`khorosjx.core.put_request_with_retries` function to leverage
  the :py:func:`khorosjx.core.__api_request_with_payload` function.
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

:doc:`Return to Top <changelog>`

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
* The :py:func:`khorosjx.errors.raise_exceptions` function is no longer necessary as the exception classes now have
  default messages and it has been removed from the :py:mod:`khorosjx.errors` module
  (`__init__.py <https://github.com/jeffshurtliff/khorosjx/blob/master/khorosjx/errors/__init__.py>`_) and the
  :ref:`supporting-modules:Handlers Module (khorosjx.errors.handlers)`.
* Removed the :py:class:`khorosjx.errors.exceptions.ExceptionMapping` and
  :py:class:`khorosjx.errors.exceptions.ExceptionGrouping` classes as they are no longer used.

:doc:`Return to Top <changelog>`

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
* Added a ``PendingDeprecationWarning`` warning on the :py:func:`khorosjx.errors.handlers.raise_exception` function as
  it will be deprecated in a future release.  (See `v1.1.1`_)

Fixed
=====
* Added the :py:func:`khorosjx.core.verify_connection` function call to the :py:func:`khorosjx.core.get_data` function.

:doc:`Return to Top <changelog>`

|

************
v1.0.1.post1
************
**Release Date: 2019-11-19**

Changed
=======
* Created a new :doc:`Introduction <introduction>` page with the existing home page content and added
  a :doc:`Navigation <index>` (i.e. Table of Contents) to the home page.
* Changed all :doc:`auxilliary modules <supporting-modules>` references to be
  :doc:`supporting modules <supporting-modules>` instead.
* Added a :ref:`introduction:Reporting Issues` section to the :doc:`Introduction <introduction>` page and to the
  `README <https://github.com/jeffshurtliff/khorosjx/blob/master/README.md>`_ file.

:doc:`Return to Top <changelog>`

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
* Added missing ``from . import core`` in the :py:mod:`khorosjx.admin`, :py:mod:`khorosjx.groups`
  and :py:mod:`khorosjx.spaces` modules.

:doc:`Return to Top <changelog>`
