# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.groups
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import groups``
:Example:        Coming Soon
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  20 Nov 2019
"""

import re

from . import core, users, errors


# Define function to verify the connection in the core module
def verify_core_connection():
    """This function verifies that the core connection information (Base URL and API credentials) has been defined.

    :returns: None
    :raises: NameError, KhorosJXError, NoCredentialsError
    """
    def __get_info():
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
        __get_info()
    return


# Define function to get basic group information for a particular Group ID
def get_group_info(group_id, return_fields=[], ignore_exceptions=False):
    """This function obtains the group information for a given Group ID.

    :param group_id: The Group ID of the group whose information will be requested
    :type group_id: int,str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the group information
    :raises: GETRequestError, InvalidDatasetError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty dictionary for the group information
    group_info = {}

    # Perform the API query to retrieve the group information
    query_uri = f"{base_url}/securityGroups/{group_id}?fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful
    successful_response = errors.handlers.check_api_response(response, ignore_exceptions=ignore_exceptions)

    # Parse the data if the response was successful
    if successful_response:
        # Determine which fields to return
        group_json = response.json()
        group_info = core.get_fields_from_api_response(group_json, 'security_group', return_fields)
    return group_info


# Define function to get information on all security groups
def get_all_groups(return_fields=[], ignore_exceptions=False):
    """This function returns information on all security groups found within the environment.

    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of dictionaries containing information for each group
    :raises: InvalidDatasetError
    """
    def __get_paginated_groups(_return_fields, _ignore_exceptions, _start_index):
        """This function returns paginated group information. (Up to 100 records at a time)

        :param _return_fields: Specific fields to return if not all of the default fields are needed (Optional)
        :type _return_fields: list
        :param _ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
        :type _ignore_exceptions: bool
        :param _start_index: The startIndex API value
        :type _start_index: int, str
        :returns: A list of dictionaries containing information for each group in the paginated query
        """
        # Initialize the empty list for the group information
        _groups = []

        # Perform the API query to retrieve the group information
        _query_uri = f"{base_url}/securityGroups?fields=@all&count=100&startIndex={_start_index}"
        _response = core.get_request_with_retries(_query_uri)

        # Verify that the query was successful
        successful_response = errors.handlers.check_api_response(_response, ignore_exceptions=_ignore_exceptions)

        if successful_response:
            # Get the response data in JSON format
            _paginated_group_data = _response.json()
            for _group_data in _paginated_group_data['list']:
                _parsed_data = core.get_fields_from_api_response(_group_data, 'security_group', _return_fields)
                _groups.append(_parsed_data)
        return _groups

    def add_to_master_list(_groups, _all_groups):
        """This function appends all group dictionaries from the paginated query to the master list.

        :param _groups: List of dictionaries from the paginated query
        :type _groups: list
        :param _all_groups: Master list of dictionaries containing group information
        :type _all_groups: list
        :returns: The master list with the appended data
        """
        for _group in _groups:
            _all_groups.append(_group)
        return _all_groups

    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty list for the group information
    all_groups = []

    # Perform the first query to get up to the first 100 groups
    start_index = 0
    groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
    all_groups = add_to_master_list(groups, all_groups)

    # Continue querying for groups until none are returned
    while len(groups) > 0:
        start_index += 100
        groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
        all_groups = add_to_master_list(groups, all_groups)

    # Return the master list of group dictionaries
    return all_groups


# Define function to obtain and return a list of the security group memberships for a user
def get_user_memberships(user_lookup, return_values='name', ignore_exceptions=False):
    """This function returns the security group memberships for a given user.

    :param user_lookup: A User ID or email address that can be used to identify the user
    :type user_lookup: int,str
    :param return_values: The type of values that should be returned in the membership list (Default: ``name``)
    :type return_values: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of group memberships for the user
    :raises: UserQueryError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize an empty list for group memberships
    memberships = []

    # Get the User ID if the user lookup value is an email address
    if (type(user_lookup) != int) and (user_lookup.isdigit() is False):
        if '@' in user_lookup:
            user_lookup = users.get_user_id(user_lookup)
        else:
            # TODO: Allow a username to be supplied and utilized as a lookup value
            error_msg = f"{user_lookup} is not a valid lookup value to obtain user memberships."
            if ignore_exceptions:
                print(error_msg)
                return memberships
            else:
                raise errors.exceptions.UserQueryError(error_msg)

    # Perform the API query and convert the response to JSON if possible
    query = f"{base_url}/people/{user_lookup}/securityGroups"
    response = core.get_request_with_retries(query)
    if response.status_code != 200:
        error_msg = f"The attempt to get group membership for the user {user_lookup} " + \
                    f"failed with a {response.status_code} status code."
        if ignore_exceptions:
            print(error_msg)
        else:
            raise errors.exceptions.UserQueryError(error_msg)
        
    else:
        groups = (response.json())['list']

        # Report a warning if 100+ groups are found since function doesn't currently look through multiple API responses
        if len(groups) >= 100:
            warn_msg = f"User ID {user_lookup} belongs to 100 or more and some may not have been captured."
            print(warn_msg)
        # TODO: Allow the paginate through the groups of >100 exist for a user

        # Add the group names to the memberships list
        for group in groups:
            if return_values == "name":
                memberships.append(group['name'])
            # TODO: Allow the Group ID to be specified as the return_values option and returned

    # Return the memberships list whether populated or empty
    return memberships
