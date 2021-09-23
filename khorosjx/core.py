# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.core
:Synopsis:          Collection of core functions and tools to work with the Jive Core API v3
:Usage:             ``import khorosjx.core`` (Imported by default in primary package)
:Example:           ``user_info = khorosjx.core.get_data('people', 'john.doe@example.com', 'email')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Sep 2021
"""

import re
import json

import requests

from . import errors
from .utils.core_utils import eprint, convert_dict_to_json
from .utils.classes import Platform, Content

# Define global variables
base_url, api_credentials = '', None


def set_base_url(domain_url, version=3, protocol='https'):
    """This function gets the base URL for API calls when supplied with a domain URL. (e.g. ``community.example.com``)

    :param domain_url: The domain URL of the environment, with or without the http/https prefix
    :type domain_url: str
    :param version: The version of the REST API to utilize (Default: ``3``)
    :type version: int
    :param protocol: The protocol to leverage for the domain prefix if not already supplied (Default: ``https``)
    :type protocol: str
    :returns: The base URL for API calls in string format (e.g. ``https://community.example.com/api/core/v3``)
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`
    """
    # Define global variable and dictionaries
    global base_url
    versions = {
        2: '/api/core/v2',
        3: '/api/core/v3'
    }
    protocols = {
        80: 'http://',
        443: 'https://',
        'http': 'http://',
        'https': 'https://'
    }

    # Add the appropriate protocol prefix if not present
    if not domain_url.startswith('http'):
        domain_url = f"{protocols.get(protocol)}{domain_url}"

    # Append the appropriate API path to the URL and return the bse URL
    domain_url = re.sub('/$', '', domain_url)
    base_url = f"{domain_url}{versions.get(version)}"
    return base_url


def set_credentials(credentials):
    """This function defines the Core API credentials as global variables and validates them.

    .. versionchanged:: 3.1.0
       Parenthesis were added to the exception classes and utilized the :py:func:`isinstsance` builtin.

    :param credentials: The username and password for the account that will be utilizing the Core API
    :type credentials: tuple
    :returns: None
    :raises: :py:exc:`khorosjx.errors.exceptions.IncompleteCredentialsError`,
             :py:exc:`khorosjx.errors.exceptions.CredentialsUnpackingError`,
             :py:exc:`khorosjx.errors.exceptions.WrongCredentialTypeError`
    """
    # Initialize the global variable
    global api_credentials

    # Ensure the supplied data can be leveraged and then define the global variable
    if len(credentials) != 2:
        if len(credentials) == 1:
            raise errors.exceptions.IncompleteCredentialsError()
        else:
            raise errors.exceptions.CredentialsUnpackingError()
    elif not isinstance(credentials[0], str) or not isinstance(credentials[1], str):
        raise errors.exceptions.WrongCredentialTypeError()
    api_credentials = credentials
    return


def connect(base_api_url, credentials):
    """This function establishes the connection information for performing Core API queries.

    :param base_api_url: The base URL (e.g. https://community.example.com) for for environment
    :type base_api_url: str
    :param credentials: The username and password of the account to perform the API queries
    :type credentials: tuple
    :returns: None
    """
    set_base_url(base_api_url)
    set_credentials(credentials)
    return


def verify_connection():
    """This function verifies that the base URL and API credentials have been defined.

    .. versionchanged:: 3.1.0
       Refactored the function to be more pythonic and to avoid depending on a try/except block.

    :returns: None
    :raises: :py:exc:`khorosjx.errors.exceptions.KhorosJXError`,
             :py:exc:`khorosjx.errors.exceptions.NoCredentialsError`
    """
    if not base_url or not api_credentials:
        raise errors.exceptions.NoCredentialsError()
    return


def get_connection_info():
    """This function returns the connection information (Base URL and API credentials) to use in other modules.

    :returns: Base URL in string format and API credentials within a tuple
    """
    # Verify that the connection has been established and then return the information
    verify_connection()
    return base_url, api_credentials


def get_api_info(api_filter="none", verify_ssl=True):
    """This function obtains the API version information for a Jive environment.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param api_filter: A filter to return a subset of API data (e.g. ``v3``, ``platform``, ``sso``, etc.)
    :type api_filter: str
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: API information in JSON, string or list format depending on the filter
    """
    # Verify that the connection has been established
    verify_connection()

    # Get the query URL to use in the API call
    query_url = f"{base_url.split('/api')[0]}/api/version"

    # Perform GET request to obtain the version information
    response = requests.get(query_url, verify=verify_ssl)
    api_data = response.json()

    # Define the return filters
    filters = {
        'none': api_data,
        'platform': api_data['jiveVersion'],
        'v2': api_data['jiveCoreVersions'][0],
        'v3': api_data['jiveCoreVersions'][1],
        'sso': api_data['ssoEnabled'],
        'edition': api_data['jiveEdition'],
        'environment': api_data['jiveEdition']['product'],
        'tier': api_data['jiveEdition']['tier']
    }

    # Filter the data to return as necessary
    if api_filter.lower() in filters:
        try:
            api_data = filters.get(api_filter.lower())
        except KeyError:
            api_data = {}
    else:
        error_msg = f"The invalid filter '{api_filter}' was provided for the API " + \
                    f"information. Defaulting to returning all data."
        print(error_msg)
    return api_data


def get_api_version(api_name="v3", verify_ssl=True):
    """This function obtains, parses and returns the current version of one of the Jive Core APIs.

    .. versionchanged:: 3.1.0
       Refactored the function to be more efficient.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param api_name: The name of the API for which the version should be returned (Default: ``v3``)
    :type api_name: str
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API version in major.minor notation (e.g. 3.15) in string format
    """
    # Verify that the connection has been established
    verify_connection()

    # Ensure that a valid API name was supplied
    if api_name not in Platform.core_api_versions:
        error_msg = f"The invalid API name '{api_name}' was provided to obtain the API " + \
                    f"version. Defaulting to v3."
        print(error_msg)
        api_name = "v3"

    # Obtain the API information
    api_data = get_api_info(api_name, verify_ssl)

    # Parse and return the API version number
    api_version = f"{api_data.get('version')}.{api_data.get('revision')}"
    return api_version


def get_platform_version(verify_ssl=True):
    """This function obtains the current Khoros JX (or Jive) version for an environment.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The full platform version in string format (e.g. ``2018.22.0.0_jx``)
    """
    # Verify that the connection has been established
    verify_connection()

    # Obtain and return the platform version
    platform_version = get_api_info('platform', verify_ssl)
    return platform_version


def get_request_with_retries(query_url, return_json=False, verify_ssl=True):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 3.1.0
       Refactored the function to be more efficient.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param query_url: The URI to be queried
    :type query_url: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``False``)
    :type return_json: bool
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response from the GET request (optionally in JSON format)
    :raises: :py:exc:`ValueError`, :py:exc:`TypeError`, :py:exc:`khorosjx.errors.exceptions.APIConnectionError`
    """
    # Verify that the connection has been established
    verify_connection()

    # Perform the GET request
    retries, response = 0, None
    while retries <= 5:
        try:
            response = requests.get(query_url, auth=api_credentials, verify=verify_ssl)
            break
        except Exception as e:
            current_attempt = f"(Attempt {retries} of 5)"
            error_msg = f"The GET request failed with the exception below. {current_attempt}"
            print(f"{error_msg}\n{e}\n")
            retries += 1
    if retries == 6:
        failure_msg = "The API call was unable to complete successfully after five consecutive API timeouts " + \
                      "and/or failures. Please call the function again or contact Khoros Support."
        raise errors.exceptions.APIConnectionError(failure_msg)

    # Convert to JSON if specified
    response = response.json() if return_json else response
    return response


def get_base_url(api_base=True):
    """This function returns the base URL of the environment with or without the ``/api/core/v3/`` path appended.

    .. versionchanged:: 3.1.0
       Refactored the function to properly utilize the ``base_url`` global variable.

    :param api_base: Determines if the ``/api/core/v3/`` path should be appended (``True`` by default)
    :type api_base: bool
    :returns: The base URL for the Khoros JX or Jive-n environment
    """
    verify_connection()
    global base_url
    base_url = '' if not base_url else base_url
    if not api_base:
        base_url = base_url.split('/api')[0]
    return base_url


def get_query_url(pre_endpoint, asset_id="", post_endpoint=""):
    """This function constructs an API query URL excluding any query strings.

    .. versionchanged:: 3.1.0
       Refactored the function to be more efficient.

    :param pre_endpoint: The endpoint portion of the URL preceding any ID numbers (e.g. ``places``)
    :type pre_endpoint: str
    :param asset_id: The ID for an asset (e.g. User ID, Browse ID for a space/blog, etc.)
    :type asset_id: str, int
    :param post_endpoint: Any remaining endpoints following the ID number (e.g. ``contents``)
    :type post_endpoint: str
    :returns: The fully structured query URL
    """
    # Verify that the connection has been established
    verify_connection()

    # Construct and return the query URL
    if pre_endpoint[-1:] == '/':
        pre_endpoint = pre_endpoint[:-1]
    query_url = f"{base_url}/{pre_endpoint}"
    for section in (asset_id, post_endpoint):
        if not isinstance(section, str):
            section = str(section)
        if section:
            if section[-1:] == '/':
                section = section[:1]
            section = f"/{section}"
        query_url += section
    return query_url


def get_data(endpoint, lookup_value, identifier='id', return_json=False, ignore_exceptions=False, all_fields=False,
             verify_ssl=True):
    """This function returns data for a specific API endpoint.

    .. versionchanged:: 3.1.0
       Fixed how the ``query_url`` variable is defined to proactively avoid raising any :py:exc:`NameError` exceptions.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param endpoint: The API endpoint against which to request data (e.g. ``people``, ``contents``, etc.)
    :type endpoint: str
    :param lookup_value: The value to use to look up the endpoint data
    :type lookup_value: int, str
    :param identifier: The type of lookup value used to look up the endpoint data (Default: ``id``)
    :type identifier: str
    :param return_json: Determines if the data should be returned in default or JSON format (Default: ``False``)
    :type return_json: bool
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :param all_fields: Determines whether or not the ``fields=@all`` query should be included (Default: ``False``)
    :type all_fields: bool
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response either as a requests response or in JSON format depending on the ``return_json`` value
    :raises: :py:exc:`khorosjx.errors.exceptions.GETRequestError`
    """
    # Verify that the connection has been established
    verify_connection()

    # Define the endpoint if an appropriate one is supplied
    available_endpoints = ['abuseReports', 'acclaim', 'actions', 'activities', 'addOns', 'announcements', 'attachments',
                           'calendar', 'checkpoints', 'collaborations', 'comments', 'contents', 'deletedObjects', 'dms',
                           'events', 'eventTypes', 'executeBatch', 'extprops', 'extstreamDefs', 'extstreams',
                           'ideaVotes', 'images', 'inbox', 'invites', 'members', 'mentions', 'messages', 'moderation',
                           'oembed', 'outcomes', 'pages', 'people', 'places', 'placeTemplateCategories',
                           'placeTemplates', 'placeTopics', 'profileImages', 'publications', 'questions', 'rsvp',
                           'search', 'sections', 'securityGroups', 'shares', 'slides', 'stages', 'statics',
                           'streamEntries', 'streams', 'tags', 'tileDefs', 'tiles', 'urls', 'versions', 'videos',
                           'vitals', 'votes', 'webhooks'
                           ]
    query_url = f"{base_url}/{endpoint}" if endpoint in available_endpoints else None
    if not query_url:
        raise errors.exceptions.InvalidEndpointError()

    # Define the identifier type for the lookup value
    if identifier == "id":
        query_url += f"/{lookup_value}"
    elif identifier == "email" or identifier == "username":
        invalid_endpoint_msg = f"The identifier '{identifier}' is only accepted with the people endpoint."
        if endpoint != "people":
            raise errors.exceptions.InvalidLookupTypeError(invalid_endpoint_msg)
        else:
            if identifier == "email":
                query_url += f"/email/{lookup_value}"
            elif identifier == "username":
                query_url += f"/username/{lookup_value}"
    else:
        unrecognized_endpoint_msg = f"The identifier '{identifier}' is unrecognized."
        if not ignore_exceptions:
            raise errors.exceptions.InvalidLookupTypeError(unrecognized_endpoint_msg)
        unrecognized_endpoint_retry_msg = f"{unrecognized_endpoint_msg} " + \
                                          "The function will attempt to use the default 'id' identifier."
        eprint(unrecognized_endpoint_retry_msg)
        query_url += f"/{lookup_value}"

    # Append the fields=@all query if requested
    query_url += "?fields=@all" if all_fields else query_url

    # Perform the GET request with retries to account for any timeouts
    response = get_request_with_retries(query_url, verify_ssl=verify_ssl)

    # Error out if the response isn't successful
    if response.status_code != 200:
        error_msg = f"The query failed with a {response.status_code} status code and the following error: " + \
                    f"{response.text}"
        if ignore_exceptions:
            print(error_msg)
            if return_json:
                empty_json = {}
                response = convert_dict_to_json(empty_json)
        else:
            raise errors.exceptions.GETRequestError(error_msg)
    response = response.json() if return_json else response
    return response


def _api_request_with_payload(_url, _json_payload, _request_type, _verify_ssl=True):
    """This function performs an API request while supplying a JSON payload.

    .. versionchanged:: 3.1.0
       Included the name of the raised exception in the error message.

    .. versionchanged:: 2.6.0
       Added the ``_verify_ssl`` argument.

    :param _url: The query URL to be leveraged in the API call
    :type _url: str
    :param _json_payload: The payload for the API call in JSON format
    :type _json_payload: dict
    :param _request_type: Defines if the API call will be a ``put`` or ``post`` request
    :type _request_type: str
    :param _verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type _verify_ssl: bool
    :returns: The API response
    :raises: :py:exc:`khorosjx.errors.exceptions.InvalidRequestTypeError`,
             :py:exc:`khorosjx.errors.exceptions.APIConnectionError`
    """
    _retries, _response = 0, None
    while _retries <= 5:
        try:
            _headers = {"Content-Type": "application/json", "Accept": "application/json"}
            if _request_type.lower() == "put":
                _response = requests.put(_url, data=json.dumps(_json_payload, default=str), auth=api_credentials,
                                         headers=_headers, verify=_verify_ssl)
            elif _request_type.lower() == "post":
                _response = requests.post(_url, data=json.dumps(_json_payload, default=str), auth=api_credentials,
                                          headers=_headers, verify=_verify_ssl)
            else:
                raise errors.exceptions.InvalidRequestTypeError()
            break
        except Exception as _api_exception:
            _exc_type = type(_api_exception).__name__
            _current_attempt = f"(Attempt {_retries} of 5)"
            _error_msg = f"The {_request_type.upper()} request has failed with the following exception: " + \
                         f"{_exc_type} - {_api_exception} {_current_attempt}"
            print(_error_msg)
            _retries += 1
            pass
    if _retries == 6:
        _failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                       "Please run the script again or contact Khoros or Aurea Support for further assistance."
        raise errors.exceptions.APIConnectionError(_failure_msg)
    return _response


def post_request_with_retries(url, json_payload, verify_ssl=True):
    """This function performs a POST request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the POST request in JSON format
    :type json_payload: dict
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response from the POST request
    :raises: :py:exc:`ValueError`, :py:exc:`khorosjx.errors.exceptions.APIConnectionError`,
             :py:exc:`khorosjx.errors.exceptions.POSTRequestError`
    """
    response = _api_request_with_payload(url, json_payload, 'post', verify_ssl)
    return response


def put_request_with_retries(url, json_payload, verify_ssl=True):
    """This function performs a PUT request with a total of 5 retries in case of timeouts or connection issues.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param url: The URI to be queried
    :type url: str
    :param json_payload: The payload for the PUT request in JSON format
    :type json_payload: dict
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response from the PUT request
    :raises: :py:exc:`ValueError`, :py:exc:`khorosjx.errors.exceptions.APIConnectionError`,
             :py:exc:`khorosjx.errors.exceptions.PUTRequestError`
    """
    response = _api_request_with_payload(url, json_payload, 'put', verify_ssl)
    return response


def delete(uri, return_json=False, verify_ssl=True):
    """This function performs a DELETE request against the Core API.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param uri: The URI against which the DELETE request will be issued
    :type uri: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``False``)
    :type return_json: bool
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response from the DELETE request (optionally in JSON format)
    """
    response = requests.delete(uri, auth=api_credentials, verify=verify_ssl)
    if return_json:
        response = response.json()
    return response


def get_fields_from_api_response(json_data, dataset, return_fields=None, quiet=False):
    """This function parses and retrieves fields from an API response from a specific dataset.

    .. versionchanged:: 3.1.0
       Changed the default ``return_fields`` value to ``None`` and adjusted the function accordingly.

    .. versionchanged:: 2.6.0
       Added conditional to ensure ``quiet`` is ``False`` before calling the ``stderr`` print statement.

    .. versionchanged:: 2.5.3
       Fixed the ``email.value`` filter and added the optional ``quiet`` argument.

    :param json_data: The JSON data from an API response
    :type json_data: dict
    :param dataset: The nickname of a dataset from which fields should be retrieved (e.g. ``people``, ``group_admins``)
    :type dataset: str
    :param return_fields: The fields that should be returned from the API response (Default: all fields in dataset)
    :type return_fields: list, None
    :param quiet: Silences any errors about being unable to locate API fields (``False`` by default)
    :type quiet: bool
    :returns: A dictionary with the field names and corresponding values
    :raises: :py:exc:`khorosjx.errors.exceptions.InvalidDatasetError`
    """
    # Define the empty dictionary for data to return
    fields_data = {}

    # Define the fields that should be returned for the data
    fields_to_return = return_fields if return_fields else []
    if not fields_to_return:
        # Get the default return fields for the dataset
        if dataset not in Content.datasets:
            error_msg = f"The supplied value '{dataset}' is not a valid dataset."
            raise errors.exceptions.InvalidDatasetError(error_msg)
        fields_to_return = Content.datasets.get(dataset)

    # Get and return the fields and corresponding values
    for field in fields_to_return:
        field_not_found = False
        try:
            if field in json_data:
                fields_data[field] = json_data[field]
            elif field == "email.value":
                fields_data[field] = json_data['emails'][0]['value']
            elif field == "name.formatted":
                fields_data[field] = json_data['name']['formatted']
            elif field == "jive.lastAuthenticated":
                fields_data[field] = json_data['jive']['lastAuthenticated']
            elif field == "jive.externalIdentities.identityType":
                fields_data[field] = json_data['jive']['externalIdentities'][0]['identityType']
            elif field == "jive.externalIdentities.identity":
                fields_data[field] = json_data['jive']['externalIdentities'][0]['identity']
            elif field == "jive.username":
                fields_data[field] = json_data['jive']['username']
            elif field == "jive.status":
                fields_data[field] = json_data['jive']['status']
            elif field == "resources.html.ref":
                fields_data[field] = json_data['resources']['html']['ref']
            else:
                field_not_found = True
        except (IndexError, KeyError):
            field_not_found = True
        if field_not_found and not quiet:
            eprint(f"Unable to locate the '{field}' field in the API response data.")
    return fields_data


def _get_filter_syntax(_filter_info, _prefix=True):
    """This function retrieves the proper filter syntax for an API call."""
    if type(_filter_info) != tuple and type(_filter_info) != list:
        raise TypeError("Filter information must be provided as a tuple (element, criteria) or a list of tuples.")
    elif type(_filter_info) == tuple:
        _filter_info = [_filter_info]
    _syntax = ""
    if len(_filter_info[0]) > 0:
        _define_prefix = {True: '&', False: ''}
        _syntax_prefix = _define_prefix.get(_prefix)
        for _filter_tuple in _filter_info:
            _element, _criteria = _filter_tuple
            _syntax = f"{_syntax_prefix}filter={_element}({_criteria})&"
        _syntax = _syntax[:-1]
    return _syntax


def get_paginated_results(query, response_data_type, start_index=0, filter_info=(), query_all=True,
                          return_fields=None, ignore_exceptions=False, quiet=False, verify_ssl=True):
    """This function performs a GET request for a single paginated response up to 100 records.

    .. versionchanged:: 3.1.0
       Changed the default ``return_fields`` value to ``None`` and adjusted the function accordingly.

    .. versionchanged:: 2.6.0
       Added the ``verify_ssl`` argument.

    :param query: The API query without the query string
    :type query: str
    :param response_data_type: The dataset of fields that will be in the API response (e.g. ``group_members``)
    :type response_data_type: str
    :param start_index: The startIndex value in the API query string (``0`` by default)
    :type start_index: int, str
    :param filter_info: A tuple of list of tuples containing the filter element and criteria (Optional)
    :type filter_info: tuple, list
    :param query_all: Determines if ``fields=@all`` filter should be included in the query string (Default: ``True``)
    :type query_all: bool
    :param return_fields: The fields that should be returned from the API response (Default: all fields in dataset)
    :type return_fields: list, None
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :param quiet: Silences any errors about being unable to locate API fields (``False`` by default)
    :type quiet: bool
    :param verify_ssl: Determines if API calls should verify SSL certificates (``True`` by default)
    :type verify_ssl: bool
    :returns: The queried data as a list comprised of dictionaries
    :raises: :py:exc:`khorosjx.errors.exceptions.GETRequestError`
    """
    # Initialize the empty list for the aggregate data
    aggregate_data = []

    # Construct the full API query
    fields_filter = ""
    if query_all:
        fields_filter = "fields=@all&"
    if '?' in query:
        # Strip out the query string if present to prevent interference with the query string to be added
        query = query.split("?")[0]
    other_filters = _get_filter_syntax(filter_info, _prefix=True)
    full_query = f"{query}?{fields_filter}count=100&startIndex={start_index}{other_filters}"

    # Perform the API query to retrieve the information
    response = get_request_with_retries(full_query, verify_ssl=verify_ssl)

    # Verify that the query was successful
    successful_response = errors.handlers.check_api_response(response, ignore_exceptions=ignore_exceptions)
    if successful_response:
        # Get the response data in JSON format
        paginated_data = response.json()
        for data in paginated_data['list']:
            # Parse and append the data
            parsed_data = get_fields_from_api_response(data, response_data_type, return_fields, quiet)
            aggregate_data.append(parsed_data)
    return aggregate_data
