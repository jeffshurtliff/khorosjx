# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.spaces
:Synopsis:       Collection of functions relating to spaces/places
:Usage:          ``import khorosjx.spaces``
:Example:        ``space_info = khorosjx.spaces.get_space_info(1234)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 Dec 2019
"""

from . import core, errors
from .utils import core_utils


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    def get_info():
        """This function initializes and defines the global variables for the connection information.

        :returns: None
        :raises: NameError, KhorosJXError, NoCredentialsError
        """
        # Initialize global variables
        global base_url
        global api_credentials

        # Define the global variables at this module level
        base_url, api_credentials = core.get_connection_info()
        return

    try:
        base_url
        api_credentials
    except NameError:
        get_info()
    return


# Define function to get basic group information for a particular Group ID
def get_space_info(place_id, return_fields=[], ignore_exceptions=False):
    """This function obtains the space information for a given Space ID.

    :param place_id: The Place ID (aka Browse ID) of the space whose information will be requested
    :type place_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the space information
    :raises: GETRequestError, InvalidDatasetError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty dictionary for the space information
    space_info = {}

    # Perform the API query to retrieve the space information
    query_uri = f"{base_url}/places/{place_id}?fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful
    successful_response = errors.handlers.check_api_response(response, ignore_exceptions=ignore_exceptions)

    # Parse the data if the response was successful
    if successful_response:
        # Determine which fields to return
        space_json = response.json()
        space_info = core.get_fields_from_api_response(space_json, 'space', return_fields)
    return space_info


# Define function to get the Place ID for a space
def get_place_id(space_id, return_type='str'):
    """This function retrieves the Place ID (aka Browse ID) for a space given its ID.

    :param space_id: The Space ID for the space to query
    :type space_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Place ID (aka Browse ID) for the space
    :raises: GETRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the API query to retrieve the information
    query_uri = f"{base_url}/places?filter=entityDescriptor(14,{space_id})&fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful and raise an exception if not
    successful_response = errors.handlers.check_api_response(response)

    # Get the placeID value from the JSON response
    if successful_response:
        space_json = response.json()
        space_dict = core.get_fields_from_api_response(space_json['list'][0], 'space', ['placeID'])
        place_id = space_dict.get('placeID')
    if return_type == 'int':
        place_id = int(place_id)
    return place_id


# Define function to get the Browse ID for a space
def get_browse_id(space_id, return_type='str'):
    """This function retrieves the Browse ID (aka Place ID) for a space given its ID.

    :param space_id: The Space ID for the space to query
    :type space_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Browse ID (aka Place ID) for the space
    :raises: GETRequestError
    """
    browse_id = get_place_id(space_id, return_type)
    return browse_id


def __verify_browse_id(_id_value, _id_type):
    """This function checks for a Browse ID and converts another value to get it if necessary."""
    _accepted_id_types = ['browse_id', 'place_id', 'space_id']
    if _id_type in _accepted_id_types:
        if _id_type != "browse_id" and _id_type != "place_id":
            _id_value = get_browse_id(_id_value)
    else:
        _exception_msg = "The supplied lookup type for the API query is not recognized. (Examples of valid " + \
                         "lookup types include 'browse_id' and 'space_id')"
        raise errors.exceptions.InvalidLookupTypeError(_exception_msg)
    return _id_value


# Define function to get the permitted content types for a space
def get_permitted_content_types(id_value, id_type='browse_id', return_type='list'):
    """This function returns the permitted content types for a given space.

    :param id_value: The space identifier as a Browse ID (default), Place ID or Space ID
    :type id_value: int, str
    :param id_type: Determines if the ``id_value`` is a ``browse_id`` (Default), ``place_id`` or ``space_id``
    :type id_type: str
    :param return_type: Determines if the result should be returned in ``list`` (Default), ``tuple`` or ``str`` format
    :type return_type: str
    :returns: The permitted content types in list, tuple or string format
    :raises: SpaceNotFountError, GETRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the appropriate ID for the space to check
    id_value = __verify_browse_id(id_value, id_type)

    # Get the permitted content types
    query_url = f"{base_url}/places/{id_value}/permissions"
    space_permissions = core.get_request_with_retries(query_url, return_json=True)

    # Check for an error in the response
    errors.handlers.check_json_for_error(space_permissions)

    # Get and return the permitted content types as a list or string
    content_types = space_permissions['contentTypes']
    if return_type == 'tuple':
        content_types = tuple(content_types)
    elif return_type == 'str':
        content_types = ', '.join(content_types)
    return content_types


# Define function to get space permissions for a space
def get_space_permissions(id_value, id_type, return_type='list'):
    def __get_paginated_permissions(_browse_id, _start_index):
        _query_uri = f"{base_url}/places/{_browse_id}/appliedEntitlements?fields=@all&count=100&" + \
                     f"startIndex={_start_index}"
        _permissions_json = core.get_request_with_retries(_query_uri, return_json=True)
        errors.handlers.check_json_for_error(_permissions_json)
        _permissions_list = _permissions_json['list']
        return _permissions_list

    # Verify that the core connection has been established
    verify_core_connection()

    # Get the appropriate ID for the space to check
    id_value = __verify_browse_id(id_value, id_type)

    # Initialize the empty list for the permissions information
    all_permissions = []

    # Perform the first query to get up to the first 100 groups
    start_index = 0
    permissions = __get_paginated_permissions(id_value, start_index)
    all_permissions = core_utils.add_to_master_list(permissions, all_permissions)

    # Continue querying for groups until none are returned
    while len(permissions) > 0:
        start_index += 100
        permissions = __get_paginated_permissions(id_value, start_index)
        all_permissions = core_utils.add_to_master_list(permissions, all_permissions)

    # Return the data as a master list of group dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_permissions = core_utils.convert_dict_list_to_dataframe(all_permissions)
    return all_permissions
