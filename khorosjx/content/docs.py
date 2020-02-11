# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.content.docs
:Synopsis:       Collection of functions relating to documents (e.g. https://community.example.com/docs/DOC-1234)
:Usage:          ``from khorosjx.content import docs``
:Example:        ``content_id = docs.get_content_id(url)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  13 Jan 2020
"""

import pandas as pd

from .. import core, errors
from . import base
from ..utils import core_utils
from ..places import base as places_core


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
def get_content_id(lookup_value, lookup_type='url'):
    """This function obtains the Content ID for a particular document.

    :param lookup_value: The URL of the document
    :type lookup_value: str
    :param lookup_type: The type of value is being used for lookup (``url`` by default)
    :type lookup_type: str
    :returns: The Content ID for the document
    :raises: ValueError, InvalidLookupTypeError
    """
    acceptable_types = ['url', 'id', 'doc_id']
    if lookup_type not in acceptable_types:
        raise errors.exceptions.InvalidLookupTypeError
    if lookup_type != 'url':
        lookup_value = get_url_for_id(lookup_value)
    content_id = base.get_content_id(lookup_value, 'document')
    return content_id


def get_url_for_id(doc_id):
    """This function constructs a full URL for a given Document ID.

    :param doc_id: The Document ID with which to construct the URL
    :type doc_id: int, str
    :returns: The fully constructed URL for the document (e.g. https://community.example.com/docs/DOC-1234)
    :raises: TypeError, ValueError
    """
    verify_core_connection()
    url = base_url.split('api/')[0]
    url = f"{url}docs/DOC-{doc_id}"
    return url


def create_document(subject, body, place_id, categories=[], tags=[]):
    """This function creates a new document.

    :param subject: The title/subject of the document
    :type subject: str
    :param body: The raw HTML making up the document body
    :type body: str
    :param place_id: The Place ID (aka Browse ID) of the space where the document should reside
    :type place_id: int, str
    :param categories: Any categories associated with the document (none by default)
    :type categories: list
    :param tags: Any tags associated with the document (none by default)
    :type tags: list
    :returns: The API response from the POST request for the document creation
    :raises: POSTRequestError, TypeError
    """
    # TODO: Allow the author to be specified
    verify_core_connection()
    place_uri = places_core.get_uri_for_id(place_id)
    content_dict = {
        "type": "text/html",
        "text": body
    }
    full_dict = {
        "content": content_dict,
        "subject": subject,
        "parent": place_uri,
        "type": "document"
    }
    if len(categories) > 0:
        full_dict["categories"] = categories
    if len(tags) > 0:
        full_dict["tags"] = tags
    payload = core_utils.convert_dict_to_json(full_dict)
    content_uri = f"{base_url}/contents"
    response = core.post_request_with_retries(content_uri, payload)
    return response


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
    lookup_value = base.__convert_lookup_value(lookup_value, lookup_type)

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
        attachment_info = base.__trim_attachments_info(attachment_info)

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
    except (IndexError, KeyError):
        attachment_info = []

    # Return a list, dataframe or dictionary depending on the data and arguments
    return attachment_info


def delete_document(lookup_value, lookup_type='content_id', return_json=False):
    """This function deletes a document.

    :param lookup_value: THe value with which to identify the document.
    :type lookup_value: str, int
    :param lookup_type: Identifies the value as a ``content_id`` (default), ``doc_id`` or ``url``
    :type lookup_type: str
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response for the DELETE request
    :raises: InvalidLookupTypeError
    """
    accepted_types = ['content_id', 'doc_id', 'url']
    if lookup_type not in accepted_types:
        raise errors.exceptions.InvalidLookupTypeError
    if lookup_type == "url":
        lookup_value = base.get_content_id(lookup_value)
    elif lookup_value == "doc_id":
        url = get_url_for_id(lookup_value)
        lookup_value = base.get_content_id(url)
    content_uri = f"{base_url}/contents/{lookup_value}"
    response = core.delete(content_uri, return_json=return_json)
    return response
