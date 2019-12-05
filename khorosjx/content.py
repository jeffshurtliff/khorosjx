# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.content
:Synopsis:       Collection of functions relating to content
:Usage:          ``from khorosjx import content``
:Example:        ``content_id = content.get_content_id(url, 'discussion')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  05 Dec 2019
"""

import re
import json

import requests
import pandas as pd

from . import core
from . import errors
from .utils.classes import Content


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


# Define function to get the content ID from a URL
def get_content_id(url, content_type="document"):
    """This function obtains the Content ID for a particular content asset. (Supports all but blog posts)

    :param url: The URL to the content
    :type url: str
    :param content_type: THe content type for the URL for which to obtain the Content ID (Default: ``document``)
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


# Define function to overwrite the body of a document
def overwrite_doc_body(url, body_html, minor_edit=True, ignore_exceptions=False):
    """This function overwrites the body of a document with new HTML content.

    :param url: THe URL of the document to be updated
    :type url: str
    :param body_html: The new HTML body to replace the existing document body
    :param minor_edit: Determines whether the *Minor Edit* flag should be set (Default: ``True``)
    :type minor_edit: bool
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: The response of the PUT request used to update the document
    :raises: ContentPublishError
    """
    # TODO: Verify and add the data type for the body_html argument in the docstring above and below
    # Define function to perform the overwrite operation
    def __perform_overwrite_operation(_url, _body_html, _minor_edit, _ignore_exceptions):
        """This function performs the actual overwrite operation on the document.

        :param _url: The URI for the API request
        :type _url: str
        :param _body_html: The new HTML body to replace the existing document body
        :param _minor_edit: Determines whether the *Minor Edit* flag should be set (Default: ``True``)
        :type _minor_edit: bool
        :param _ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
        :type _ignore_exceptions: bool
        :returns: The response of the PUT request used to update the document
        :raises: ContentPublishError
        """
        # Define the script name, Content ID and URI
        _content_id = get_content_id(_url)
        _content_url = f"{base_url}/contents/{_content_id}"

        # Perform a GET request for the document to obtain its JSON
        _response = core.get_data('contents', _content_id)

        # Construct the payload from the new body HTML
        _doc_body_payload = {'text': _body_html}

        # Update the document JSON with the new body HTML
        _doc_json = _response.json()
        _doc_json['content'] = _doc_body_payload

        # Flag the update as a "Minor Edit" to suppress email notifications if specified
        if _minor_edit:
            _doc_json['minor'] = 'true'

        # Perform the PUT request with retry handling for timeouts
        _put_response = core.put_request_with_retries(_content_url, _doc_json)
        if _put_response.status_code != 200:
            _error_msg = f"The attempt to update the document {_url} failed with " + \
                        f"a {_put_response.status_code} status code."
            if _ignore_exceptions:
                print(_error_msg)
            else:
                raise errors.exceptions.ContentPublishError(_error_msg)
        return _put_response

    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the overwrite operation
    put_response = __perform_overwrite_operation(url, body_html, minor_edit, ignore_exceptions)

    # Check for any 502 errors and try the function one more time if found
    if put_response.status_code == 502:
        retry_msg = "Performing the overwrite operation again in an attempt to overcome the 502 " + \
                    "Bad Gateway / Service Temporarily Unavailable issue that was encountered."
        print(retry_msg)
        put_response = __perform_overwrite_operation(url, body_html, minor_edit, ignore_exceptions)

    # Return the response from the PUT query
    return put_response


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


# Define function to get basic group information for a particular Group ID
def get_document_info(lookup_value, lookup_type='doc_id', return_fields=[], ignore_exceptions=False):
    """This function obtains the group information for a given document.

    :param lookup_value: The value with which to look up the document
    :type lookup_value: int, str
    :param lookup_type: Identifies the type of lookup value that has been provided (Default: ``doc_id``)
    :type lookup_type: str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the group information
    :raises: GETRequestError, InvalidDatasetError, InvalidLookupTypeError, LookupMismatchError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the Content ID if not supplied
    lookup_value = __convert_lookup_value(lookup_value, lookup_type)

    # Initialize the empty dictionary for the group information
    doc_info = {}

    # Perform the API query to retrieve the group information
    query_uri = f"{base_url}/contents/{lookup_value}?fields=@all"
    response = core.get_request_with_retries(query_uri)

    # Verify that the query was successful
    successful_response = errors.handlers.check_api_response(response, ignore_exceptions=ignore_exceptions)

    # Parse the data if the response was successful
    if successful_response:
        # Determine which fields to return
        doc_json = response.json()
        doc_info = core.get_fields_from_api_response(doc_json, 'document', return_fields)
    return doc_info


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


# Define function to get the attachments in a document
def get_document_attachments(lookup_value, lookup_type='doc_id', return_dataframe=False):
    """This function retrieves information on any attachments associated with a document.

    :param lookup_value: The value with which to look up the document
    :type lookup_value: str, int
    :param lookup_type: Identifies the type of lookup value that has been provided (Default: ``doc_id``)
    :type lookup_type: str
    :param return_dataframe: Determines whether or not a pandas dataframe should be returned
    :type return_dataframe: bool
    :returns: A list, dictionary or pandas dataframe depending on the number of attachments and/or function arguments
    :raises: GETRequestError, InvalidDatasetError, InvalidLookupTypeError, LookupMismatchError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Get the attachments data from the API
    try:
        attachment_info = get_document_info(lookup_value, lookup_type, ['attachments'])
        attachment_info = attachment_info['attachments']
        attachment_info = __trim_attachments_info(attachment_info)

        # Convert the data to a dataframe if indicated
        if return_dataframe:
            column_names = list(attachment_info[0].keys())
            data = []
            for idx in range(0,len(attachment_info)):
                data.append(list(attachment_info[idx].values()))
            attachment_info = pd.DataFrame(data, columns=column_names)

        # Trim the data down to the inner dictionary if there is only one attachment
        elif len(attachment_info) == 1:
            attachment_info = attachment_info[0]

    # Initiate an empty list to return if no attachments are found
    except IndexError:
        attachment_info = []

    # Return a list, dataframe or dictionary depending on the data and arguments
    return attachment_info
