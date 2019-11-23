# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.content
:Synopsis:       Collection of functions relating to content
:Usage:          ``from khorosjx import content``
:Example:        ``content_id = content.get_content_id(url, 'discussion')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  23 Nov 2019
"""

import re
import json

import requests

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
