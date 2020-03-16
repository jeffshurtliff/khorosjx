# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.groups
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import groups``
:Example:        ``group_info = groups.get_group_info(1051)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  22 Jan 2020
"""

import requests

from . import core, users, errors
from .utils.classes import Groups
from .utils.core_utils import eprint
from .utils import core_utils, df_utils


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
def get_all_groups(return_fields=[], return_type='list', ignore_exceptions=False):
    """This function returns information on all security groups found within the environment.

    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param return_type: Determines if the data should be returned in a list or a pandas dataframe (Default: ``list``)
    :type return_type: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of dictionaries or a dataframe containing information for each group
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

    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty list for the group information
    all_groups = []

    # Perform the first query to get up to the first 100 groups
    start_index = 0
    groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
    all_groups = core_utils.add_to_master_list(groups, all_groups)

    # Continue querying for groups until none are returned
    while len(groups) > 0:
        start_index += 100
        groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
        all_groups = core_utils.add_to_master_list(groups, all_groups)

    # Return the data as a master list of group dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_groups = df_utils.convert_dict_list_to_dataframe(all_groups)
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


def check_user_membership(user_memberships, groups_to_check, scope='any', ignore_exceptions=False):
    """This function checks if a user belongs to one or more security groups.

    :param user_memberships: A list of security groups to which the user belongs
    :type user_memberships: list, tuple
    :param groups_to_check: One or more groups (name or ID) against which to compare the user's memberships
    :type groups_to_check: list, tuple, str
    :param scope: Determines the result returned for the comparison (Options: ``any``, ``all`` or ``each``)
    :type scope: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: Returns a Boolean value for ``any`` and ``all`` scopes, or a list of Boolean values for ``each``
    :raises: InvalidScopeError
    """
    # Convert the groups_to_check argument to a tuple if a string was provided
    if type(groups_to_check) == str:
        # Check for a comma-separated string
        if ',' in groups_to_check:
            if ', ' in groups_to_check:
                groups_to_check = ', '.join(groups_to_check)
            else:
                groups_to_check = ','.join(groups_to_check)
            tuple(groups_to_check)
        else:
            groups_to_check = (groups_to_check, )

    # Check to ensure that a valid scope is defined
    scope_types = ['any', 'all', 'each']
    if scope not in scope_types:
        if ignore_exceptions:
            error_msg = f"The supplied scope '{scope}' is not recognized and the default scope of 'any' will be used."
            eprint(error_msg)
        else:
            raise errors.exceptions.InvalidScopeError

    # Check the groups supplied against the list of memberships
    groups_found = []
    all_results = []
    for group in groups_to_check:
        if group in user_memberships:
            groups_found.append(group)
            all_results.append(True)
        else:
            all_results.append(False)

    # Define and return the Boolean response based on the scope
    result = False
    if scope == "any":
        if len(groups_found) > 0:
            result = True
    elif scope == "all":
        if len(groups_found) == len(groups_to_check):
            result = True
    elif scope == "each":
        result = all_results
    return result


# Define function to add a user to a security group
def add_user_to_group(group_id, user_value, lookup_type="id", return_mode="none",
                      print_results=True, ignore_exceptions=True):
    """This function adds a user to a security group.

    :param group_id: The Group ID of the security group to which the user should be added
    :type group_id: int, str
    :param user_value: The value with which to look up the user (e.g. User ID, email address)
    :type user_value: int, str
    :param lookup_type: Defines whether the user value is a User ID or an email address (Default: ``id``)
    :type lookup_type: str
    :param return_mode: Determines what--if anything--should be returned by the function (Default: ``none``)
    :type return_mode: str
    :param print_results: Determines whether or not all results (including success messages) should be printed onscreen
    :type print_results: bool
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``True``)
    :type ignore_exceptions: bool
    :returns: The resulting status code, a Boolean value indicating the success of the operation, or nothing
    :raises: POSTRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Define the default Boolean return value
    added_to_group = False

    # Obtain the Jive ID if an email address is provided for the user information
    valid_lookup_types = ('id', 'email')
    if lookup_type not in valid_lookup_types:
        if ignore_exceptions:
            error_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                        "lookup types include 'id' and 'email')"
            eprint(error_msg)
        else:
            raise errors.exceptions.InvalidLookupTypeError
    if lookup_type == "email":
        user_value = users.get_user_id(user_value)

    # Define the query parameters
    query_uri = f"{base_url}/securityGroups/{group_id}/members"
    user_uri = f'["{base_url}/people/{user_value}"]'

    # Add the user to the group
    response = requests.post(query_uri, data=user_uri, auth=api_credentials,
                             headers={"Content-Type": "application/json", "Accept": "application/json"})
    added_to_group = errors.handlers.check_api_response(response, 'post', ignore_exceptions=ignore_exceptions)

    # The remainder of the function assumes exceptions are being ignored
    if added_to_group:      # True if status code == 204
        if print_results:
            success_msg = f"The user (User ID {user_value}) has been added successfully to Group ID {group_id}."
            print(success_msg)
    else:
        fail_msg = f"The user (User ID {user_value}) failed to be added to Group ID " + \
                   f"{group_id} with a {response.status_code}" + \
                   f" status code and the following message: {response.text}"
        eprint(fail_msg)

    # Define what is returned at the end of the function
    if return_mode.lower() == "status":
        try:
            return response.status_code
        except UnboundLocalError:
            return 500
    elif return_mode.lower() == "bool":
        try:
            return added_to_group
        except UnboundLocalError:
            return False
    else:
        return


# Define function to get the members (or admins) of a security group
def get_group_memberships(group_id, user_type="member", only_id=True, return_type="list", ignore_exceptions=False):
    """This function gets the memberships (including administrator membership) for a specific security group.

    :param group_id: The Group ID for the security group
    :type group_id: int, str
    :param user_type: Determines if the function should return ``admin`` or ``member`` users (Default: ``member``)
    :type user_type: str
    :param only_id: Determines if only the User ID for the members should be returned or full data (Default: ``True``)
    :type only_id: bool
    :param return_type: Determines if a ``list`` or ``dataframe`` should be returned (Default: ``list``)
    :type return_type: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``True``)
    :type ignore_exceptions: bool
    :returns: A list or dataframe of security group memberships
    :raises: ValueError
    """
    # Define internal function to query for a paginated list of users and then add them to the master list
    def __add_paginated_members(_base_query_uri, _response_data_type, _start_index,
                                _ignore_exceptions, _return_fields, _all_users):
        _paginated_users = core.get_paginated_results(_base_query_uri, _response_data_type, _start_index,
                                                      ignore_exceptions=_ignore_exceptions,
                                                      return_fields=_return_fields)
        _all_users = core_utils.add_to_master_list(_paginated_users, _all_users)
        return _all_users, len(_paginated_users)

    # Verify that the core connection has been established
    verify_core_connection()

    # Initiate an empty list for the user data
    all_users = []
    return_fields = []

    # Define the base query URI
    if user_type in Groups.membership_types:
        base_query_uri = f"{base_url}/securityGroups/{group_id}/{Groups.membership_types.get(user_type)}"
    else:
        raise ValueError(f"The '{user_type}' value is not a valid user type.")

    # Determine if only the User IDs should be returned
    if only_id:
        return_fields.append('id')

    # Get the response data type
    response_data_type = Groups.user_type_mapping.get(user_type)

    # Perform the first query to get up to the first 100 members or admins
    start_index = 0
    all_users, users_returned = __add_paginated_members(base_query_uri, response_data_type, start_index,
                                                        ignore_exceptions, return_fields, all_users)

    # Continue querying for groups until none are returned
    while users_returned > 0:
        start_index += 100
        all_users, users_returned = __add_paginated_members(base_query_uri, response_data_type, start_index,
                                                            ignore_exceptions, return_fields, all_users)

    # Return the data as a master list of group dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_users = core_utils.convert_dict_list_to_dataframe(all_users)
    elif return_type == "list" and only_id is True:
        all_users = core_utils.convert_single_pair_dict_list(all_users)
    return all_users
