# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.places.spaces
:Synopsis:          Collection of core places functions that are specific to spaces
:Usage:             ``import khorosjx.places.spaces``
:Example:           ``space_info = khorosjx.places.spaces.get_space_info(browse_id)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     04 Jan 2020
"""

from .. import core, errors
from . import base as places_core
from ..utils import core_utils, df_utils


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    def __get_info():
        """This function initializes and defines the global variables for the connection information."""
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
        __get_info()
    return


# Define function to get space info
def get_space_info(place_id, return_fields=[], ignore_exceptions=False):
    """This function obtains the space information for a given Place ID. (aka Browse ID)

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

    # Leverage the core module to retrieve the data
    space_info = places_core.get_place_info(place_id, return_fields, ignore_exceptions)
    return space_info


# Define function to get the permitted content types for a space
def get_permitted_content_types(id_value, id_type='browse_id', return_type='list'):
    """This function returns the permitted content types for a given space.

    :param id_value: The space identifier as a Browse ID (default), Place ID or Container ID
    :type id_value: int, str
    :param id_type: Determines if the ``id_value`` is a ``browse_id`` (Default), ``place_id`` or ``container_id``
    :type id_type: str
    :param return_type: Determines if the result should be returned in ``list`` (Default), ``tuple`` or ``str`` format
    :type return_type: str
    :returns: The permitted content types in list, tuple or string format
    :raises: SpaceNotFountError, GETRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the appropriate ID for the space to check
    id_value = places_core.__verify_browse_id(id_value, id_type)

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
def get_space_permissions(id_value, id_type='browse_id', return_type='list'):
    """This function returns all of the defined permissions (aka ``appliedEntitlements``) for a specific space.

    :param id_value: The space identifier as a Browse ID (default), Place ID or Space ID
    :type id_value: int, str
    :param id_type: Determines if the ``id_value`` is a ``browse_id`` (Default), ``place_id`` or ``space_id``
    :type id_type: str
    :param return_type: Determines if the result should be returned as a ``list`` (Default) or pandas ``dataframe``
    :type return_type: str
    :returns: The list or dataframe with the space permissions
    :raises: SpaceNotFoundError, GETRequestError
    """
    def __get_paginated_permissions(_browse_id, _start_index):
        _query_uri = f"{base_url}/places/{_browse_id}/appliedEntitlements?fields=@all&count=100&" + \
                     f"startIndex={_start_index}"
        _permissions_json = core.get_request_with_retries(_query_uri, return_json=True)
        errors.handlers.check_json_for_error(_permissions_json, 'space')
        _permissions_list = _permissions_json['list']
        return _permissions_list

    # Verify that the core connection has been established
    verify_core_connection()

    # Get the appropriate ID for the space to check
    id_value = places_core.__verify_browse_id(id_value, id_type)

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
        all_permissions = __generate_permissions_dataframe(all_permissions)
    return all_permissions


# Define function to get the unique fields for the permissions data
def __get_unique_permission_fields(_permissions_dict_list):
    """This function gets the unique fields from a space permissions list from the ``get_space_permissions`` function.

    :param _permissions_dict_list: A list of dictionaries containing space permissions
    :type _permissions_dict_list: list
    :returns: List of unique field names
    """
    _unique_fields = []
    for _permissions_dict in _permissions_dict_list:
        for _permission_field in _permissions_dict.keys():
            if _permission_field not in _unique_fields:
                _unique_fields.append(_permission_field)
    return _unique_fields


# Define function to generate a dataframe with the space permissions
def __generate_permissions_dataframe(_permissions_dict_list):
    """This function converts a list of dictionaries containing space permissions into a pandas dataframe.

    :param _permissions_dict_list: A list of dictionaries containing space permissions
    :type _permissions_dict_list: list
    :returns: A pandas dataframe with the permissions data
    """
    # Get the unique field names to act as the dataframe columns
    _unique_permission_fields = __get_unique_permission_fields(_permissions_dict_list)

    # Loop through the dictionaries in the original list
    for _permissions_dict in _permissions_dict_list:
        # Loop through the unique permission fields to see if they are all present
        for _unique_field in _unique_permission_fields:
            if _unique_field not in _permissions_dict.keys():
                # Add the field if it does not exist
                _permissions_dict[_unique_field] = ''

    # Convert the dictionary list to a pandas dataframe
    _permissions_data = df_utils.convert_dict_list_to_dataframe(_permissions_dict_list, _unique_permission_fields)
    return _permissions_data
