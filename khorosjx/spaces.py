# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.spaces
:Synopsis:       Collection of functions relating to spaces/places
:Usage:          ``import khorosjx.spaces``
:Example:        ``space_info = khorosjx.spaces.get_space_info(1234)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  05 Dec 2019
"""

from . import core, errors


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
