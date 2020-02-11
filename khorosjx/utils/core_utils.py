# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.utils.core_utils
:Synopsis:          Useful tools and utilities to assist in managing a Khoros JX (formerly Jive-x) or Jive-n community
:Usage:             ``import khorosjx``
:Example:           ``timestamp = khorosjx.utils.core_utils.get_timestamp(time_format="delimited")``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:      Dec 2019
"""

import sys
import json
import warnings
from datetime import datetime

from dateutil import tz

from . import df_utils
from ..errors import exceptions
from .classes import TimeUtils, Content


# Print an error message to stderr instead of stdout
# TODO: Move this function to the khorosjx.errors.handlers module
def eprint(*args, **kwargs):
    """This function behaves the same as the ``print()`` function but is leveraged to print errors to ``sys.stderr``."""
    print(*args, file=sys.stderr, **kwargs)
    return


# Define function to get the current timestamp
def get_timestamp(time_format="split"):
    """This function obtains the current timestamp in the local timezone.

    :param time_format: The format for the timestamp that will be returned (default: ``split``)
    :type time_format: str
    :returns: The current timestamp in ``%Y-%m-%d %H:%M:%S`` format as a string
    """
    # Get the appropriate formatting syntax
    formatting_syntax = get_format_syntax(time_format)

    # Get the current time
    current_timestamp = datetime.now(tz.gettz())
    current_timestamp = current_timestamp.strftime(formatting_syntax)
    return current_timestamp


def get_format_syntax(syntax_nickname):
    """This function obtains the appropriate datetime format syntax for a format nickname. (e.g. ``delimited``)

    :param syntax_nickname: The nickname of a datetime format
    :type syntax_nickname: str
    :returns: The proper datetime format as a string
    """
    if syntax_nickname in TimeUtils.time_formats:
        time_format = TimeUtils.time_formats.get(syntax_nickname)
    else:
        error_msg = f"The time format '{syntax_nickname}' is not recognized. Defaulting to delimited formatting."
        print(error_msg)
        time_format = TimeUtils.time_formats.get('delimited')
    return time_format


# Define function to validate a timestamp string to see if it is properly formatted
def validate_timestamp(timestamp, time_format="delimited", replace_invalid=True):
    """This function validates a timestamp string to ensure that it matches a prescribed syntax.

    :param timestamp: The timestamp in string format
    :type timestamp: str
    :param time_format: The format for the supplied timestamp (default: ``delimited``)
    :type time_format: str
    :param replace_invalid: States if an invalid timestamp should be replaced with a default value (Default: ``True``)
    :type replace_invalid: bool
    :returns: A valid timestamp string, either what was provided or a default timestamp
    :raises: ValueError
    """
    # Define a default timestamp to use if the supplied timestamp is invalid
    default_timestamp = "2016-01-01T01:01:01"
    if time_format == "split":
        default_timestamp = default_timestamp.replace('T', ' ')

    # Get the format syntax based on its nickname
    formatting_syntax = get_format_syntax(time_format)

    # Test the script validation by attempting to parse it as a datetime object
    try:
        parsed_timestamp = datetime.strptime(timestamp, formatting_syntax)
    except ValueError as timestamp_exception:
        if replace_invalid:
            # Log and display an error and replace timestamp with the default value before returning it
            error_msg = f"The timestamp {timestamp} is invalid and will be replaced " + \
                        f"with the default value {default_timestamp}."
            print(error_msg)
            timestamp = default_timestamp
        else:
            # Raise an exception for the invalid timestamp
            raise ValueError(timestamp_exception)
    return timestamp


# Define function to convert a dictionary to JSON
def convert_dict_to_json(data):
    """This function converts a dictionary to JSON so that it can be traversed similar to a converted requests response.

    :param data: Dictionary to be converted to JSON
    :type data: dict
    :returns: The dictionary data in JSON format
    :raises: TypeError
    """
    data = json.dumps(data)
    data = json.loads(data)
    return data


# Define function to convert a list of dictionaries to a pandas dataframe
def convert_dict_list_to_dataframe(dict_list, column_names=[]):
    """This function converts a list of dictionaries into a pandas dataframe.

    :param dict_list: List of dictionaries
    :type dict_list: list
    :param column_names: The column names for the dataframe (Optional)
    :type column_names: list
    :returns: A pandas dataframe of the data
    """
    warnings.warn(
        "The khorosjx.utils.core_utils.convert_dict_list_to_dataframe function is deprecated and will be removed "
        "in v3.0.0. Use khorosjx.utils.df_utils.convert_dict_list_to_dataframe instead.",
        DeprecationWarning
    )
    # Leverage the khorosjx.utils.df_utils.convert_dict_list_to_dataframe function to get and return the dataframe
    dataframe = df_utils.convert_dict_list_to_dataframe(dict_list, column_names)
    return dataframe


# Define function to convert a single-pair dictionary list to a normal list
def convert_single_pair_dict_list(dict_list):
    """This function converts a list of single-pair dictionaries into a normal list.

    :param dict_list: A list of single-pair dictionaries
    :type dict_list: list
    :returns: A normal list with the value from each dictionary
    """
    new_list = []
    for dict_pair in dict_list:
        for dict_val in dict_pair.values():
            new_list.append(dict_val)
    return new_list


def add_to_master_list(single_list, master_list):
    """This function appends items in a list to the master list.

    :param single_list: List of dictionaries from the paginated query
    :type single_list: list
    :param master_list: Master list of dictionaries containing group information
    :type master_list: list
    :returns: The master list with the appended data
    """
    for list_item in single_list:
        master_list.append(list_item)
    return master_list


def print_if_verbose(msg, verbose_enabled=False):
    """This function prints a message onscreen only if verbose mode is enabled.

    :param msg: The message to print onscreen
    :type msg: str
    :param verbose_enabled: Determines if verbose mode is enabled (``False`` by default)
    :type verbose_enabled: bool
    :returns: None
    """
    if verbose_enabled:
        print(msg)
    return


def identify_dataset(query_uri):
    """This function identifies the appropriate field dataset by examining a query URI.

    :param query_uri: The API query URI to be examined
    :type query_uri: str
    :returns: The appropriate dataset name in string format
    """
    dataset = ""
    for uri_identifier, dataset_mapping in Content.uri_dataset_mapping.items():
        if uri_identifier in query_uri:
            dataset = dataset_mapping
            break
    if dataset == "":
        raise exceptions.DatasetNotFoundError
    if uri_identifier == '__get_security_group_dataset':
        dataset = __get_security_group_dataset(query_uri)
    elif uri_identifier == '__get_invite_dataset':
        dataset = __get_invite_dataset(query_uri)
    elif uri_identifier == '__get_metadata_dataset':
        dataset = __get_metadata_dataset(query_uri)
    elif uri_identifier == '__get_moderation_dataset':
        dataset = __get_moderation_dataset(query_uri)
    elif uri_identifier == '__get_search_dataset':
        dataset = __get_search_dataset(query_uri)
    elif uri_identifier == '__get_support_center_dataset':
        dataset = __get_support_center_dataset(query_uri)
    elif uri_identifier == '__get_tile_dataset':
        dataset = __get_tile_dataset(query_uri)
    return dataset


def __get_security_group_dataset(_query_uri):
    """This function identifies the appropriate security group dataset."""
    _dataset = ""
    for _uri_identifier, _dataset_mapping in Content.security_group_uri_map.items():
        if _uri_identifier in _query_uri:
            _dataset = _dataset_mapping
    if _dataset == "":
        _dataset = "security_group"
    return _dataset


def __get_invite_dataset(_query_uri):
    """This function identifies the appropriate invite dataset."""
    _dataset = "invite"
    if 'invites/event' in _query_uri:
        _dataset = "event_invite"
    return _dataset


def __get_metadata_dataset(_query_uri):
    """This function identifies the appropriate metadata dataset."""
    _dataset = "metadata_property"
    if 'properties/public' in _query_uri:
        _dataset = "metadata_public_property"
    return _dataset


def __get_moderation_dataset(_query_uri):
    """This function identifies the appropriate moderation dataset."""
    _dataset = "moderation"
    if 'pending/counts' in _query_uri:
        _dataset = "moderation_pending_count"
    elif 'pending' in _query_uri:
        _dataset = "moderation_pending"
    return _dataset


def __get_search_dataset(_query_uri):
    """This function identifies the appropriate search dataset."""
    _dataset = ""
    if 'search/contents' in _query_uri:
        _dataset = "search_contents"
    elif 'search/people' in _query_uri:
        _dataset = "search_people"
    elif 'search/places' in _query_uri:
        _dataset = "search_places"
    elif 'search/tags' in _query_uri:
        _dataset = "search_tags"
    return _dataset


def __get_support_center_dataset(_query_uri):
    """This function identifies the appropriate support center dataset."""
    _dataset = ""
    if 'avatar' in _query_uri:
        _dataset = "support_center_avatar"
    elif 'banner' in _query_uri:
        _dataset = "support_center_banner"
    elif 'blocks' in _query_uri:
        _dataset = "support_center_block"
    elif 'channels' in _query_uri:
        _dataset = "support_center_channel"
    elif 'categories' in _query_uri:
        _dataset = "support_center_category"
    elif 'section' in _query_uri:
        _dataset = "section"
    return _dataset


def __get_tile_dataset(_query_uri):
    """This function identifies the appropriate tile dataset."""
    if 'categories' in _query_uri:
        _dataset = "tile_category"
    else:
        _dataset = "tile"
    return _dataset
