# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.core
:Synopsis:       Collection of core functions and tools to work with the Jive Core API v3
:Usage:          ``import khorosjx.core`` (Imported by default in primary package)
:Example:        ``user_info = khorosjx.core.get_data('people', 'john.doe@example.com', 'email')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  24 Nov 2019
"""

import re
import json
import warnings

import requests

from . import errors
from .utils.core_utils import eprint, convert_dict_to_json
from .utils.classes import FieldLists, Platform


# Define function to get the base API URL
def set_base_url(domain_url, version=3, protocol='https'):
    """This function gets the base URL for API calls when supplied with a domain URL. (e.g. ``community.example.com``)

    :param domain_url: The domain URL of the environment, with or without the http/https prefix
    :type domain_url: str
    :param version: The version of the REST API to utilize (Default: ``3``)
    :type version: int
    :param protocol: The protocol to leverage for the domain prefix if not already supplied (Default: ``https``)
    :type protocol: str
    :returns: The base URL for API calls in string format (e.g. ``https://community.example.com/api/core/v3``)
    :raises: TypeError, ValueError
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


# Define function to define the Core API credentials as global variables
def set_credentials(credentials):
    """This function defines the Core API credentials as global variables and validates them.

    :param credentials: The username and password for the account that will be utilizing the Core API
    :type credentials: tuple
    :returns: None
    """
    # Initialize the global variable
    global api_credentials

    # Ensure the supplied data can be leveraged and then define the global variable
    if len(credentials) != 2:
        if len(credentials) == 1:
            raise errors.exceptions.IncompleteCredentialsError
        else:
            raise errors.exceptions.CredentialsUnpackingError
    elif (type(credentials[0]) != str) or (type(credentials[1]) != str):
        raise errors.exceptions.WrongCredentialTypeError
    api_credentials = credentials
    return


# Define function to set up connection to the Core API
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


# Define function to check if the API credentials have been defined and raise an exception if not
def verify_connection():
    """This function verifies that the base URL and API credentials have been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    try:
        base_url
        api_credentials
    except NameError:
        raise errors.exceptions.NoCredentialsError
    return


# Define function to get the connection information
def get_connection_info():
    """This function returns the connection information (Base URL and API credentials) to use in other modules.

    :returns: Base URL in string format and API credentials within a tuple
    """
    # Verify that the connection has been established and then return the information
    verify_connection()
    return base_url, api_credentials


# Define function to get the current API version information
def get_api_info(api_filter="none"):
    """This function obtains the API version information for a Jive environment.

    :param api_filter: A filter to return a subset of API data (e.g. ``v3``, ``platform``, ``sso``, etc.)
    :type api_filter: str
    :returns: API information in JSON, string or list format depending on the filter
    """
    # Verify that the connection has been established
    verify_connection()

    # Get the query URL to use in the API call
    query_url = f"{base_url}/api/version"

    # Perform GET request to obtain the version information
    response = requests.get(query_url)
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


# Define function to get the current Core API version
def get_api_version(api_name="v3"):
    """This function obtains, parses and returns the current version of one of the Jive Core APIs.

    :param api_name: The name of the API for which the version should be returned (Default: ``v3``)
    :type api_name: str
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
    api_data = get_api_info(api_name)

    # Parse and return the API version number
    api_version = f"{api_data['version']}.{api_data['revision']}"
    return api_version


# Define function to get the current Core API version
def get_platform_version():
    """This function obtains the current Khoros JX (or Jive) version for an environment.

    :returns: The full platform version in string format (e.g. ``2018.22.0.0_jx``)
    """
    # Verify that the connection has been established
    verify_connection()

    # Obtain and return the platform version
    platform_version = get_api_info('platform')
    return platform_version


# Define function to perform a GET request with retries
def get_request_with_retries(query_url, return_json=False):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

    :param query_url: The URI to be queried
    :type query_url: str
    :param return_json: Determines whether or not the response should be returned in JSON format (Default: ``False``)
    :type return_json: bool
    :returns: The API response from the GET request (optionally in JSON format)
    :raises: ValueError, TypeError, ConnectionError
    """
    # Verify that the connection has been established
    verify_connection()

    # Perform the GET request
    retries = 0
    while retries <= 5:
        try:
            response = requests.get(query_url, auth=api_credentials)
            break
        except Exception as e:
            current_attempt = f"(Attempt {retries} of 5)"
            error_msg = f"The GET request failed with the exception below. {current_attempt}"
            print(f"{error_msg}\n{e}\n")
            retries += 1
            pass
    if retries == 6:
        failure_msg = "The API call was unable to complete successfully after five consecutive API timeouts " + \
                      "and/or failures. Please call the function again or contact Khoros Support."
        raise ConnectionError(failure_msg)

    # Convert to JSON if specified
    if return_json:
        response = response.json()
    return response


# Define function to perform a general GET request
def get_data(endpoint, lookup_value, identifier='id', return_json=False, ignore_exceptions=False):
    """This function returns data for a specific API endpoint.

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
    :returns: The API response either as a requests response or in JSON format depending on the ``return_json`` value
    :raises: GETRequestError
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
    if endpoint in available_endpoints:
        endpoint_url = f"{base_url}/{endpoint}"
    else:
        raise errors.exceptions.InvalidEndpointError

    # Define the identifier type for the lookup value
    if identifier == "id":
        query_url = f"{endpoint_url}/{lookup_value}"
    elif identifier == "email" or identifier == "username":
        invalid_endpoint_msg = f"The identifier '{identifier}' is only accepted with the people endpoint."
        if endpoint != "people":
            raise errors.exceptions.InvalidLookupTypeError(invalid_endpoint_msg)
        else:
            if identifier == "email":
                query_url = f"{endpoint_url}/email/{lookup_value}"
            elif identifier == "username":
                query_url = f"{endpoint_url}/username/{lookup_value}"
    else:
        unrecognized_endpoint_msg = f"The identifier '{identifier}' is unrecognized."
        if not ignore_exceptions:
            raise errors.exceptions.InvalidLookupTypeError(unrecognized_endpoint_msg)
        unrecognized_endpoint_retry_msg = f"{unrecognized_endpoint_msg} " + \
                                          "The function will attempt to use the default 'id' identifier."
        eprint(unrecognized_endpoint_retry_msg)
        query_url = f"{endpoint_url}/{lookup_value}"

    # Perform the GET request with retries to account for any timeouts
    response = get_request_with_retries(query_url)

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
    if return_json:
        response = response.json()
    return response


# Define function to perform a PUT request with supplied JSON data
def put_request_with_retries(url, json_payload):
    """This function performs a GET request with a total of 5 retries in case of timeouts or connection issues.

        :param url: The URI to be queried
        :type url: str
        :param json_payload: The payload for the PUT request in JSON format
        :type json_payload: json
        :returns: The API response from the GET request
        :raises: ValueError, ConnectionError
        """
    retries = 0
    while retries <= 5:
        try:
            response = requests.put(url, data=json.dumps(json_payload, default=str), auth=api_credentials,
                                    headers={"Content-Type": "application/json", "Accept": "application/json"})
            break
        except Exception as put_exception:
            current_attempt = f"(Attempt {retries} of 5)"
            error_msg = f"The PUT request has failed with the following exception: {put_exception} {current_attempt}"
            print(error_msg)
            retries += 1
            pass
    if retries == 6:
        failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                      "Please run the script again or contact Khoros or Aurea Support for further assistance."
        print(failure_msg)
        
        raise ConnectionError(f"{failure_msg}")
    return response


# Define function to get fields from API responses
def get_fields_from_api_response(json_data, dataset, return_fields=[]):
    # Define the empty dictionary for data to return
    fields_data = {}

    # Map the datasets to their respective field lists
    datasets = {
        'security_group': FieldLists.security_group_fields
    }

    # Define the fields that should be returned for the data
    if len(return_fields) > 0:
        fields_to_return = return_fields
    else:
        # Get the default return fields for the dataset
        if dataset not in datasets:
            error_msg = f"The supplied value '{dataset}' is not a valid dataset."
            raise errors.exceptions.InvalidDatasetError(error_msg)
        fields_to_return = datasets.get(dataset)

    # Get and return the fields and corresponding values
    for field in fields_to_return:
        if field in json_data:
            fields_data[field] = json_data[field]
    return fields_data
