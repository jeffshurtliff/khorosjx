# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.users
:Synopsis:       Collection of functions relating to user accounts and profiles
:Usage:          ``import khorosjx``
:Example:        ``user_info = khorosjx.users.get_people_followed(user_id)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 Nov 2019
:Version:        1.0.0
"""

import json

from . import core
from . import errors
from .utils import core_utils
from .utils.classes import Users


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


# Define function to return JSON field data for a user
def get_json_field(json_data, field_names):
    """This function retrieves a value for a specific field from the JSON data for a user.

    :param json_data: The JSON data from which the field value must be retrieved
    :type json_data: json
    :param field_names: The field name along with any parent field paths
    :type field_names: tuple, list
    :returns: The value for the specific field in its original format
    :raises: ValueError, TypeError, KeyError
    """
    if type(field_names) == str:
        field_value = json_data[field_names]
    elif (type(field_names) == tuple) or (type(field_names) == list):
        if len(field_names) == 2:
            field_one, field_two = field_names
            field_value = json_data[field_one][field_two]
        elif len(field_names) == 3:
            field_one, field_two, field_three = field_names
            field_value = json_data[field_one][field_two][field_three]
        elif len(field_names) == 4:
            field_one, field_two, field_three, field_four = field_names
            field_value = json_data[field_one][field_two][field_three][field_four]
    else:
        field_value = None
    return field_value


# Define function to populate a dictionary with user account and profile information
def parse_user_fields(json_data):
    """This function populates a dictionary with the user information retrieved from the API response.

    :param json_data: The user data retrieved from the API in JSON format
    :type json_data: json
    :returns: Dictionary of user information that has been validated and normalized
    """
    # Populate the fields
    user_info = {}
    for db_field, json_field in Users.UserJSON.fields.items():
        try:
            user_info[db_field] = get_json_field(json_data, json_field)
            if db_field == 'user_address_street':
                user_info[db_field] = user_info.get(db_field).replace('\n', '')
            elif (db_field == 'user_first_login') or (db_field == 'user_last_login'):
                raw_timestamp = user_info.get(db_field)[:19]
                user_info[db_field] = core_utils.validate_timestamp(raw_timestamp)
            elif db_field == 'user_tags':
                user_info[db_field] = ', '.join(user_info.get(db_field))
            elif db_field == 'user_profile':
                profile = user_info[db_field]
                for idx in range(0, len(profile)):
                    if profile[idx]['jive_label'] in Users.UserJSON.profile_fields:
                        profile_field_name = Users.UserJSON.profile_fields.get(profile[idx]['jive_label'])
                        user_info[profile_field_name] = profile[idx]['value']
                del user_info['user_profile']
        except (KeyError, IndexError, AttributeError) as e:
            # Continue on to the next field
            continue
    # Return the user information
    return user_info


# Define function to get someone's User ID when provided with their email address
def get_user_id(email):
    """This function obtains the User ID for a user by querying the API against the user's email address.

    :param email: Email address of the user
    :type email: str
    :returns: User ID for the user
    """
    user_data = core.get_data('people', email, 'email', return_json=True)
    user_id = user_data['id']
    return user_id


# Define function to get someone's username using their email address or user ID (default)
def get_username(lookup_value, lookup_type="id"):
    """This function obtains the username for a user by looking up their User ID or email address.

    :param lookup_value: The User ID or email address for which to look up the user
    :type lookup_value: str
    :param lookup_type: Determines if the User ID or email address should be used to find the user (Default: ``id``)
    :type lookup_type: str
    :returns: The username for the user
    """
    if lookup_type != "id" and lookup_type != "email":
        warn_msg = f"The lookup type {lookup_type} is not recognized. The function will " + \
                   f"default to treating the lookup value as an email address."
        print(warn_msg)
        endpoint = "email"
    user_data = core.get_data('people', lookup_value, lookup_type, return_json=True)
    username = user_data['jive']['username']
    return username


# Define function to get a user's profile URL using their email address or user ID (default)
def get_profile_url(lookup_value, lookup_type="id"):
    """This function constructs the URL to a user's profile.

    :param lookup_value: The lookup value to locate the user
    :type lookup_value: str
    :param lookup_type: Determines if the lookup value is a User ID, email address or username (Default: ``id``)
    :type lookup_type: str
    :returns: The URL of the user's profile
    """
    if lookup_type == "username":
        username = lookup_value
    else:
        username = get_username(lookup_value, lookup_type)
    profile_url = f"https://community.rsa.com/people/{username}"
    return profile_url


# Define function to get the count of content created by a user
def get_user_content_count(user_id, start_index=0):
    """This function obtains the number of content items created by a particular user.

    :param user_id: The User ID of the user
    :type user_id: int
    :param start_index: The startIndex value in the REST API call (Default: ``0``)
    :type start_index: int
    :returns: The count of content found for the user in integer format
    """
    def __get_count(_user_uri, _start_index, _count=100):
        """This function identifies the content count for an individual REST API call.
        :param _user_uri: The URI for the user using the ``people`` API endpoint
        :type _user_uri: str
        :param _start_index: The startIndex value in the REST API call
        :type _start_index: int
        :param _count:  The number of results to return from the API (Default: ``100``)
        :type _count: int
        :returns: The count of content found for the individual REST API call in integer format
        """
        _content_uri = f"{base_url}/contents?filter=author({_user_uri})&count={_count}&startIndex={_start_index}"
        _response = core.get_request_with_retries(_content_uri)
        if _response.status_code == 200:
            _response_json = _response.json()
            _content_count = len(_response_json['list'])
        else:
            _content_count = 0
        return _content_count

    # Define the variable to track the total content count and structure the user URI
    total_count = 0
    user_uri = f"{base_url}/people/{user_id}"

    # Get the content count for the first 100 results and increment the total count accordingly
    content_count = __get_count(user_uri, start_index)
    total_count += content_count

    # Continue rolling through the user content until all assets have been identified
    while content_count > 0:
        start_index += 100
        content_count = __get_count(user_uri, start_index)
        total_count += content_count
    return total_count


# Define function to get the people followed by a particular user
def get_people_followed(user_id, ignore_exceptions=False, return_type=list, start_index=0):
    """This function returns a comma-separated list of users followed by a particular user.

    :param user_id: The User ID for the user against which to check
    :type user_id: int
    :param ignore_exceptions: Determines whether non-200 API responses should raise an exception (Default: ``False``)
    :type ignore_exceptions: bool
    :param return_type: Determines whether to return a comma-separated string, tuple or list (Default: ``list``)
    :type return_type: type
    :param start_index: The startIndex for the API call (Default: ``0``)
    :type start_index: int
    :returns: The User IDs of all people followed by the queried user
    """
    def __get_followed(_user_id, _ignore_exceptions=False, _start_index=0, _count=100):
        """This function performs the API call to get the users followed from a single GET request.

        :param _user_id: The User ID for the user against which to check
        :type _user_id: int
        :param _ignore_exceptions: Determines whether non-200 responses should raise an exception (Default: ``False``)
        :type _ignore_exceptions: bool
        :param _start_index: The startIndex for the API call (Default: ``0``)
        :type _start_index: int
        :param _count: The maximum number of results to return in the API call (Default: ``100``)
        :type _count: int
        :returns: The data from the @following sub-endpoint in JSON format
        """
        _following_url = f"{base_url}/people/{_user_id}/@following?count={_count}" + \
                         f"&startIndex={_start_index}"
        _response = core.get_request_with_retries(_following_url)
        if _response.status_code == 200:
            _following_data = _response.json()
        else:
            if _ignore_exceptions:
                _empty_response = {"list": []}
                _following_data = core_utils.convert_dict_to_json(_empty_response)
            else:
                if _response.status_code == 404:
                    errors.raise_exception('user_not_found')
                else:
                    errors.raise_exception('user_query_error')
        return _following_data

    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the initial API call
    people_followed = []
    following_data = __get_followed(user_id, ignore_exceptions)

    # Continue looping through the data from subsequent calls until an empty list is found in the JSON response
    while len(following_data['list']) > 0:
        for user_followed in following_data['list']:
            # Append reach User ID to the list
            people_followed.append(user_followed['id'])

        # Perform the next API call for the next 100 users
        start_index += 100
        following_data = __get_followed(user_id, ignore_exceptions, start_index)

    # Convert the list to a comma-separated string and return the value
    if return_type == str:
        people_followed = ','.join(people_followed)
    elif return_type == tuple:
        people_followed = tuple(people_followed)
    return people_followed
