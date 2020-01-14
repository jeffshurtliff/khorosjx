# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.places.base
:Synopsis:          Collection of core functions relating to places (i.e. spaces and blogs)
:Usage:             ``import khorosjx.places.base as places_core``
:Example:           ``place_info = khorosjx.spaces.core.get_place_info(browse_id)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Jan 2020
"""

from .. import core, errors
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


# Define function to get basic place information for a particular Place ID
def get_place_info(place_id, return_fields=[], ignore_exceptions=False):
    """This function obtains the place information for a given Place ID. (aka Browse ID)

    :param place_id: The Place ID (aka Browse ID) of the place whose information will be requested
    :type place_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the place information
    :raises: GETRequestError, InvalidDatasetError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty dictionary for the space information
    place_info = {}

    # Perform the API query to retrieve the space information
    query_uri = f"{base_url}/places/{place_id}?fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful
    successful_response = errors.handlers.check_api_response(response, ignore_exceptions=ignore_exceptions)

    # Parse the data if the response was successful
    if successful_response:
        # Determine which fields to return
        place_json = response.json()
        place_info = core.get_fields_from_api_response(place_json, 'place', return_fields)
    return place_info


# Define function to get the Place ID for a place
def get_place_id(container_id, return_type='str'):
    """This function retrieves the Place ID (aka Browse ID) for a place given its Container ID.

    :param container_id: The Container ID for the space to query
    :type container_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Place ID (aka Browse ID) for the place
    :raises: GETRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the API query to retrieve the information
    query_uri = f"{base_url}/places?filter=entityDescriptor(14,{container_id})&fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful and raise an exception if not
    successful_response = errors.handlers.check_api_response(response)

    # Get the placeID value from the JSON response
    if successful_response:
        place_json = response.json()
        place_dict = core.get_fields_from_api_response(place_json['list'][0], 'place', ['placeID'])
        place_id = place_dict.get('placeID')
    if return_type == 'int':
        place_id = int(place_id)
    return place_id


# Define function to get the Browse ID for a space
def get_browse_id(container_id, return_type='str'):
    """This function retrieves the Browse ID (aka Place ID) for a place given its Container ID.

    :param container_id: The Space ID for the space to query
    :type container_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Browse ID (aka Place ID) for the place
    :raises: GETRequestError
    """
    browse_id = get_place_id(container_id, return_type)
    return browse_id


def __verify_browse_id(_id_value, _id_type):
    """This function checks for a Browse ID and converts another value to get it if necessary."""
    _accepted_id_types = ['browse_id', 'place_id', 'space_id', 'blog_id', 'container_id']
    if _id_type in _accepted_id_types:
        if _id_type != "browse_id" and _id_type != "place_id":
            _id_value = get_browse_id(_id_value)
    else:
        _exception_msg = "The supplied lookup type for the API query is not recognized. (Examples of valid " + \
                         "lookup types include 'browse_id' and 'container_id')"
        raise errors.exceptions.InvalidLookupTypeError(_exception_msg)
    return _id_value


def get_uri_for_id(destination_id, browse_id=True):
    """This function generates the full URI for a place given an identifier.

    :param desination_id: A Jive ID or Place ID (aka Browse ID) for a place
    :type destination_id: int, str
    :param browse_id: Defines whether or not the identifier provided is a Browse ID (``True`` by default)
    :type browse_id: bool
    :returns: The full URI in string format
    """
    verify_core_connection()
    if not browse_id:
        destination_id = get_browse_id(destination_id)
    uri = f"{base_url}/places/{destination_id}"
    return uri


# Define function to get a list of places from a CSV or Excel file
def get_places_list_from_file(full_path, file_type='csv', has_headers=True,
                              id_column='', id_type='browse_id', excel_sheet_name='', filter_info={}):
    """This function retrieves a list of place identifiers from a file.

    :param full_path: The full path to the file to import
    :type full_path: str
    :param file_type: Defines if the file to be imported is a ``csv`` (Default), ``xlsx``, ``xls`` or ``txt`` file.
    :param has_headers: Defines if the import file uses column headers (``True`` by default)
    :type has_headers: bool
    :param id_column: Defines the column name (if applicable) which contains the place identifier (Null by default)
    :type id_column: str
    :param id_type: Defines if the ID type is a ``browse_id`` (Default) or ``container_id``
    :type id_type: str
    :param excel_sheet_name: The sheet name to retrieve if an Excel file is supplied (First sheet imported by default)
    :type excel_sheet_name: str
    :param filter_info: Dictionary used to apply any filter to the imported data if necessary (Null by default)
    :type filter_info: dict
    :returns: A list of place identifiers
    :raises: InvalidFileTypeError
    """
    # Make changes to the arguments depending on whether or not headers are present
    if has_headers is False:
        try:
            id_column = int(id_column)
        except ValueError:
            id_column = 0

    # Ensure that any filter columns are returned
    return_cols = [id_column]
    if len(filter_info) > 0:
        for filter_col in filter_info.keys():
            return_cols.append(str(filter_col))

    # Determine the use case for importing the data based on the supplied arguments
    if file_type == 'csv' or file_type == 'txt':
        dataframe = df_utils.import_csv(full_path, columns_to_return=return_cols, has_headers=has_headers)
    elif file_type == 'xlsx' or file_type == 'xls':
        use_first_sheet = True if excel_sheet_name == '' else False
        dataframe = df_utils.import_excel(full_path, excel_sheet_name, use_first_sheet=use_first_sheet,
                                          columns_to_return=return_cols, has_headers=has_headers)
    else:
        raise errors.exceptions.InvalidFileTypeError

    # Apply any given filters
    if len(filter_info) > 0:
        for filter_key, filter_val in filter_info.items():
            dataframe = dataframe.loc[dataframe[filter_key] == filter_val]

    # Convert the IDs to a list and return it
    places_list = dataframe[id_column].tolist()
    return places_list
