# -*- coding: utf-8 -*-
"""
:Module:        khorosjx.utils.core_utils
:Synopsis:      Useful tools and utilities to assist in managing a Khoros JX (formerly Jive-x) or Jive-n community
:Usage:         ``import khorosjx``
:Example:       ``timestamp = get_timestamp(time_format="delimited")``
:Created By:    Jeff Shurtliff
:Last Modified: Jeff Shurtliff
:Modified Date: 30 Nov 2019
"""

import sys
import json
from datetime import datetime

import pandas as pd
from dateutil import tz

from .classes import TimeUtils


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
def convert_dict_list_to_dataframe(dict_list):
    """This function converts a list of dictinoaries into a pandas dataframe.

    :param dict_list: List of dictionaries
    :type dict_list: list
    :returns: A pandas dataframe of the data
    """
    # Identify the dataframe column names
    column_names = []
    for field_name in dict_list[0].keys():
        column_names.append(field_name)

    # Identify the data for each column
    df_data = []
    for idx in range(0, len(dict_list)):
        row_data = []
        for field_value in dict_list[idx].values():
            row_data.append(field_value)
        df_data.append(row_data)

    # Create and return the dataframe
    dataframe = pd.DataFrame(df_data, columns=column_names)
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
