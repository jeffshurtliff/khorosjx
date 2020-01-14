# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.base
:Synopsis:          Collection of core functions relating to content
:Usage:             ``import khorosjx.content.base as content_core``
:Example:           ``content_id = content_core.get_content_id(url, 'document')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Jan 2020
"""

import re

from .. import core, errors
from ..utils.classes import Content


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


# Define function to get the content ID from a URL
def get_content_id(url, content_type="document"):
    """This function obtains the Content ID for a particular content asset. (Supports all but blog posts)

    :param url: The URL to the content
    :type url: str
    :param content_type: The content type for the URL for which to obtain the Content ID (Default: ``document``)
    :type content_type: str
    :returns: The Content ID for the content URL
    :raises: ValueError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the domain URL from the supplied content URL
    if content_type in Content.content_url_delimiters:
        platform_url = url.split(Content.content_url_delimiters.get(content_type))[0]
        if not platform_url.startswith('http'):
            platform_url = f"https://{platform_url}"
    else:
        error_msg = "Unable to identify the platform URL for the URL and defined content type."
        raise ValueError(error_msg)

    # Get the ID to be used in the GET request
    if content_type == "document":
        item_id = url.split('DOC-')[1]
    elif content_type == "blog post":
        raise ValueError(f"The get_content_id function does not currently support blog posts.")
    else:
        item_id = re.sub('^.*/', '', url)

    # Construct the appropriate query URL
    if content_type in Content.content_types:
        content_type_id = Content.content_types.get(content_type)
        query_url = f"{platform_url}/api/core/v3/contents?filter=entityDescriptor({content_type_id},{item_id})&count=1"
    else:
        error_msg = f"The content type {content_type} is unrecognized. Unable to perform the function."
        raise ValueError(f"{error_msg}")

    # Query the API to get the content ID
    response = core.get_request_with_retries(query_url)
    content_data = response.json()
    content_id = content_data['list'][0]['contentID']
    return content_id


# Define an internal function to convert a lookup value to a proper lookup type
def __convert_lookup_value(_lookup_value, _lookup_type, _content_type="document"):
    """This function converts a lookup value to a proper lookup type.

    :param _lookup_value: The lookup value to be converted
    :type _lookup_value: str, int
    :param _lookup_type: The current lookup type of the value to be converted
    :type _lookup_type: str
    :param _content_type: The type of content associated with the lookup value and lookup type (Default: ``document``)
    :type _content_type: str
    :returns: The properly formatted lookup value
    :raises: LookupMismatchError, InvalidLookupTypeError, CurrentlyUnsupportedError
    """
    if _content_type == "document":
        # Get the Content ID if not supplied
        if _lookup_type == "doc_id" or _lookup_type == "url":
            if _lookup_type == "doc_id":
                if 'http' in str(_lookup_value):
                    _error_msg = f"The 'doc_id' lookup_type was supplied (default) but the lookup value is a URL."
                    raise errors.exceptions.LookupMismatchError(_error_msg)
                _lookup_value = f"{base_url.split('/api')[0]}/docs/DOC-{_lookup_value}"
            _lookup_value = get_content_id(_lookup_value)
        elif _lookup_type != "id" and _lookup_type != "content_id":
            _exception_msg = "The supplied lookup type for the API is not recognized. " + \
                             "(Valid lookup types include 'id', 'content_id', 'doc_id' and 'url')"
            raise errors.exceptions.InvalidLookupTypeError(_exception_msg)
    else:
        _exception_msg = f"The '{_content_type}' content type is not currently supported."
        raise errors.exceptions.CurrentlyUnsupportedError(_exception_msg)
        # TODO: Add functionality for other content types (e.g. discussion/question threads)
    return _lookup_value


# Define internal function to trim the attachments data
def __trim_attachments_info(_attachment_info):
    """This function removes certain fields from attachments data captured via the API.

    :param _attachment_info: List containing dictionaries of attachments retrieved via the API
    :type _attachment_info: list
    :returns: The trimmed list of dictionaries
    """
    for _idx in range(0, len(_attachment_info)):
        _fields_to_ignore = ['resources', 'doUpload']
        for _ignored_field in _fields_to_ignore:
            if _ignored_field in _attachment_info[_idx].keys():
                del _attachment_info[_idx][_ignored_field]
    return _attachment_info