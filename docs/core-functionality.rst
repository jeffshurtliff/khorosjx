##################
Core Functionality
##################
.. warning::

    This page is currently in development.

This page provides instructions and examples around the core functionality of the library.  This includes a review
of the :ref:`introduction:Basic Usage` as well as base functionality such as performing generic API requests.

* `Getting Started`_
    * `Importing the package`_
    * `Initializing the modules`_
    * `Establishing the API connection`_
* `Performing GET Requests`_
    * `Using the get_data() function`_
        * `Optional arguments in the get_data() function`_
            * `Ignoring exceptions in the get_data() function`_
            * `Returning the get_data() response in JSON format`_
    * `Using the get_request_with_retries() function`_
        * `Returning the get_request_with_retries() response in JSON format`_
* `Performing POST Requests`_
* `Performing PUT Requests`_

***************
Getting Started
***************
The topics in this section are necessary to leverage the khorosjx library.

|

.. include:: basic-usage.rst

|

***********************
Performing GET Requests
***********************
There are two primary ways to perform GET requests against the Core API.  The first is to use the ``get_data()``
function, which avoids the necessity to construct a `query URI <https://en.wikipedia.org/wiki/Query_string>`_ but is
somewhat restrictive in what can be returned. The second is more flexible but does require the construction of
API query URIs.

Both of these methods are addressed in the sections below.

|

Using the get_data() function
=============================
The ``get_data()`` function performs GET requests by requiring only two arguments: the API **endpoint** and a
**lookup value**.

The API **endpoints**, also known as the API *services* in the
`Jive REST API documentation <https://developers.jivesoftware.com/api/v3/cloud/rest/index.html#overview>`_, are the
different avenues within the API through which data can be retrieved and, in some cases, created and/or modified. The
endpoints supported within the khorosjx library are listed below.

+----------------+---------------+----------------+-------------------------+----------------+---------------+
| abuseReports   | acclaim       | actions        | activities              | addOns         | announcements |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| attachments    | calendar      | checkpoints    | collaborations          | comments       | contents      |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| deletedObjects | dms           | events         | eventTypes              | executeBatch   | extprops      |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| extstreamDefs  | extstreams    | ideaVotes      | images                  | inbox          | invites       |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| members        | mentions      | messages       | moderation              | oembed         | outcomes      |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| pages          | people        | places         | placeTemplateCategories | placeTemplates | placeTopics   |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| profileImages  | publications  | questions      | rsvp                    |search          | sections      |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| securityGroups | shares        | slides         | stages                  | statics        | streamEntries |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| streams        | tags          | tileDefs       | tiles                   | urls           | versions      |
+----------------+---------------+----------------+-------------------------+----------------+---------------+
| videos         | vitals        | votes          | webhooks                |                |               |
+----------------+---------------+----------------+-------------------------+----------------+---------------+

By default, the respective ID is used as the lookup value for each endpoint. For example, when querying the
*people* endpoint the default lookup value is the **User ID**, whereas when querying the *contents* endpoint
the default lookup value is the **Content ID**.

The example below shows how you would use the function to retrieve data for content with ``12345`` as its
*Content ID*.

.. code-block:: python

    api_response = khorosjx.core.get_data('contents', 12345)

.. note::

    Because `f-strings <https://www.python.org/dev/peps/pep-0498/>`_ are leveraged to construct the query URIs in
    the function, the lookup value can be supplied as an *integer* or a *string*.

When querying against specific endpoints, other identifiers may be permitted as well. For example, if querying for
user data via the ``people`` endpoint it is possible to supply a ``User ID``, ``username`` or ``email address`` as
demonstrated in the examples below.

.. code-block:: python

    response_from_id = khorosjx.core.get_data('people', 1234)
    response_from_email = khorosjx.core.get_data('people', 'john.doe@example.com', 'email')
    response_from_username = khorosjx.core.get_data('people', 'john_doe', 'username')

Optional arguments in the get_data() function
---------------------------------------------
There are two optional arguments that may be supplied within the ``get_data()`` function which can be useful
in certain circumstances. Both are addressed below.

Ignoring exceptions in the get_data() function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When utilizing the ``get_data()`` function multiple times, such as when looping through a list of users, it may
be useful to ignore exceptions so that the entire script doesn't fail if data for a single user cannot be returned
successfully.  This can be done by setting the ``ignore_exceptions`` argument to ``True`` in the function arguments,
as demonstrated below.

.. code-block:: python

    api_response = khorosjx.core.get_data('people', 1234, ignore_exceptions=True)

Leveraging this option will result in failed responses printing an error message and then either returning the API
response (which will include a status code other than ``200``) or an empty JSON string.  (See the next section)

Returning the get_data() response in JSON format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Rather than having to convert the API response to JSON in your script, you can do so within the ``get_data()`` function
by setting the ``return_json`` argument to ``True`` as shown in the example below.

.. code-block:: python

    user_json = khorosjx.core.get_data('people', 1234, return_json=True)

.. note::

    As stated in the previous section, if the ``ignore_exceptions`` argument is also set to true then JSON data will
    still be returned but will simply be empty.

|

Using the get_request_with_retries() function
=============================================
If you have a need to perform a less generic GET request then it will likely be better to leverage the
``get_request_with_retries()`` function instead of ``get_data()`` so that the specific query URI can be supplied.

The ``get_request_with_retries()`` function performs the GET query and will retry the operation up to five times to
account for any unexpected connection aborts or timeouts, which is known to happen on occasion with the Jive APIs.

This function is demonstrated in the example below.

.. code-block:: python

    query_uri = f"{base_url}/people/1234/contents?count=100&startIndex=200&fields=@all"
    api_response = khorosjx.core.get_request_with_retries(query_uri)

.. note::

    Notice that the ``base_url`` global variable is being utilized above, which was defined when
    `establishing the API connection`_ when `getting started`_ above.

Returning the get_request_with_retries() response in JSON format
----------------------------------------------------------------
Similar to the ``get_data()`` function, you have the option of returning the response in JSON format by setting the
``return_json`` argument to ``True`` as shown in the example below.

.. code-block:: python

    get_request_json = khorosjx.core.get_request_with_retries(query_uri, return_json=True)

|

************************
Performing POST Requests
************************
.. todo::

    This section is not yet written but will be at a future date.

|

***********************
Performing PUT Requests
***********************
.. todo::

    This section is not yet written but will be at a future date.