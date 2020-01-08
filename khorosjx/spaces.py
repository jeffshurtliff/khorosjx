# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.spaces
:Synopsis:          Collection of deprecated functions relating to spaces/places
:Usage:             ``import khorosjx.spaces``
:Example:           ``space_info = khorosjx.spaces.get_space_info(1234)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Jan 2020
"""

import warnings

from .places import spaces
from .places import base as places_core


# Define function to get basic group information for a particular Group ID
def get_space_info(place_id, return_fields=[], ignore_exceptions=False):
    """This function obtains the space information for a given Space ID.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.get_space_info` function should be used.

    :param place_id: The Place ID (aka Browse ID) of the space whose information will be requested
    :type place_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the space information
    :raises: GETRequestError, InvalidDatasetError
    """
    warnings.warn(
        "The khorosjx.spaces.get_space_info function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.spaces.get_space_info instead.",
        DeprecationWarning
    )
    space_info = spaces.get_space_info(place_id, return_fields, ignore_exceptions)
    return space_info


# Define function to get the Place ID for a space
def get_place_id(space_id, return_type='str'):
    """This function retrieves the Place ID (aka Browse ID) for a space given its ID.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.get_place_id` function should be used.

    :param space_id: The Space ID for the space to query
    :type space_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Place ID (aka Browse ID) for the space
    :raises: GETRequestError
    """
    warnings.warn(
        "The khorosjx.spaces.get_place_id function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.base.get_place_id instead.",
        DeprecationWarning
    )
    place_id = places_core.get_place_id(space_id, return_type)
    return place_id


# Define function to get the Browse ID for a space
def get_browse_id(space_id, return_type='str'):
    """This function retrieves the Browse ID (aka Place ID) for a space given its ID.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.get_browse_id` function should be used.

    :param space_id: The Space ID for the space to query
    :type space_id: int, str
    :param return_type: Determines whether to return the value as a ``str`` or an ``int`` (Default: ``str``)
    :type return_type: str
    :returns: The Browse ID (aka Place ID) for the space
    :raises: GETRequestError
    """
    warnings.warn(
        "The khorosjx.spaces.get_browse_id function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.base.get_browse_id instead.",
        DeprecationWarning
    )
    browse_id = places_core.get_place_id(space_id, return_type)
    return browse_id


def __verify_browse_id(_id_value, _id_type):
    """This function checks for a Browse ID and converts another value to get it if necessary.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.__verify_browse_id` function should be used.
    """
    warnings.warn(
        "The khorosjx.spaces.__verify_browse_id function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.base.__verify_browse_id instead.",
        DeprecationWarning
    )
    _id_value = places_core.__verify_browse_id(_id_value, _id_type)
    return _id_value


# Define function to get a space list from a CSV or Excel file
def get_spaces_list_from_file(full_path, file_type='csv', has_headers=True,
                              id_column='', id_type='browse_id', excel_sheet_name='', filter_info={}):
    """This function retrieves a list of space identifiers from a file.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.base.get_places_list_from_file` function should be used.

    :param full_path: The full path to the file to import
    :type full_path: str
    :param file_type: Defines if the file to be imported is a ``csv`` (Default), ``xlsx``, ``xls`` or ``txt`` file.
    :param has_headers: Defines if the import file uses column headers (``True`` by default)
    :type has_headers: bool
    :param id_column: Defines the column name (if applicable) which contains the space identifier (Null by default)
    :type id_column: str
    :param id_type: Defines if the ID type is a ``browse_id`` (Default) or ``place_id`` (aka ``container_id``)
    :type id_type: str
    :param excel_sheet_name: The sheet name to retrieve if an Excel file is supplied (First sheet imported by default)
    :type excel_sheet_name: str
    :param filter_info: Dictionary used to apply any filter to the imported data if necessary (Null by default)
    :type filter_info: dict
    :returns: A list of space identifiers
    :raises: InvalidFileTypeError
    """
    warnings.warn(
        "The khorosjx.spaces.get_spaces_list_from_file function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.base.get_places_list_from_file instead.",
        DeprecationWarning
    )
    spaces_list = places_core.get_places_list_from_file(full_path, file_type, has_headers, id_column,
                                                        id_type, excel_sheet_name, filter_info)
    return spaces_list


# Define function to get the permitted content types for a space
def get_permitted_content_types(id_value, id_type='browse_id', return_type='list'):
    """This function returns the permitted content types for a given space.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.get_permitted_content_types` function should be used.

    :param id_value: The space identifier as a Browse ID (default), Place ID or Space ID
    :type id_value: int, str
    :param id_type: Determines if the ``id_value`` is a ``browse_id`` (Default), ``place_id`` or ``space_id``
    :type id_type: str
    :param return_type: Determines if the result should be returned in ``list`` (Default), ``tuple`` or ``str`` format
    :type return_type: str
    :returns: The permitted content types in list, tuple or string format
    :raises: SpaceNotFountError, GETRequestError
    """
    warnings.warn(
        "The khorosjx.spaces.get_permitted_content_types function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.spaces.get_permitted_content_types instead.",
        DeprecationWarning
    )
    content_types = spaces.get_permitted_content_types(id_value, id_type, return_type)
    return content_types


# Define function to get space permissions for a space
def get_space_permissions(id_value, id_type='browse_id', return_type='list'):
    """This function returns all of the defined permissions for a specific space.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.get_space_permissions` function should be used.

    :param id_value: The space identifier as a Browse ID (default), Place ID or Space ID
    :type id_value: int, str
    :param id_type: Determines if the ``id_value`` is a ``browse_id`` (Default), ``place_id`` or ``space_id``
    :type id_type: str
    :param return_type: Determines if the result should be returned as a ``list`` (Default) or pandas ``dataframe``
    :type return_type: str
    :returns: The list or dataframe with the space permissions
    :raises: SpaceNotFoundError, GETRequestError
    """
    warnings.warn(
        "The khorosjx.spaces.get_space_permissions function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.places.spaces.get_space_permissions instead.",
        DeprecationWarning
    )
    all_permissions = spaces.get_space_permissions(id_value, id_type, return_type)
    return all_permissions


# Define function to get the unique fields for the permissions data
def __get_unique_permission_fields(_permissions_dict_list):
    """This function gets the unique fields from a space permissions list.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.__get_unique_permission_fields` function should be used.

    :param _permissions_dict_list: A list of dictionaries containing space permissions
    :type _permissions_dict_list: list
    :returns: List of unique field names
    """
    warnings.warn(
        "The khorosjx.spaces.__get_unique_permission_fields function is deprecated and will be removed " +
        "in v3.0.0. Use khorosjx.places.spaces.__get_unique_permission_fields instead.",
        DeprecationWarning
    )
    _unique_fields = spaces.__get_unique_permission_fields(_permissions_dict_list)
    return _unique_fields


# Define function to generate a dataframe with the space permissions
def __generate_permissions_dataframe(_permissions_dict_list):
    """This function converts a list of dictionaries containing space permissions into a pandas dataframe.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.places.spaces.__generate_permissions_dataframe` function should be used.

    :param _permissions_dict_list: A list of dictionaries containing space permissions
    :type _permissions_dict_list: list
    :returns: A pandas dataframe with the permissions data
    """
    warnings.warn(
        "The khorosjx.spaces.__generate_permissions_dataframe function is deprecated and will be removed " +
        "in v3.0.0. Use khorosjx.places.spaces.__generate_permissions_dataframe instead.",
        DeprecationWarning
    )
    _permissions_data = spaces.__generate_permissions_dataframe(_permissions_dict_list)
    return _permissions_data
