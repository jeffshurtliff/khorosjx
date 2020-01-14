# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content
:Synopsis:          Collection of functions relating to content
:Usage:             ``from khorosjx import content``
:Example:           ``content_id = content.base.get_content_id(url, 'document')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     14 Jan 2020
"""

import warnings

from . import base, docs, events, ideas, threads, videos

__all__ = ['base', 'docs', 'events', 'ideas', 'threads', 'videos']


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def get_content_id(url, content_type="document"):
    """This function obtains the Content ID for a particular content asset. (Supports all but blog posts)

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.base.get_content_id` function should be used.

    :param url: The URL to the content
    :type url: str
    :param content_type: The content type for the URL for which to obtain the Content ID (Default: ``document``)
    :type content_type: str
    :returns: The Content ID for the content URL
    :raises: ValueError
    """
    warnings.warn(
        "The khorosjx.content.get_content_id function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.base.get_content_id instead.",
        DeprecationWarning
    )
    content_id = base.get_content_id(url, content_type)
    return content_id


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def overwrite_doc_body(url, body_html, minor_edit=True, ignore_exceptions=False):
    """This function overwrites the body of a document with new HTML content.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.docs.overwrite_doc_body` function should be used.

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
    warnings.warn(
        "The khorosjx.content.overwrite_doc_body function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.docs.overwrite_doc_body instead.",
        DeprecationWarning
    )
    put_response = docs.overwrite_doc_body(url, body_html, minor_edit, ignore_exceptions)
    return put_response


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def __convert_lookup_value(_lookup_value, _lookup_type, _content_type="document"):
    """This function converts a lookup value to a proper lookup type.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.base.__convert_lookup_value` function should be used.

    :param _lookup_value: The lookup value to be converted
    :type _lookup_value: str, int
    :param _lookup_type: The current lookup type of the value to be converted
    :type _lookup_type: str
    :param _content_type: The type of content associated with the lookup value and lookup type (Default: ``document``)
    :type _content_type: str
    :returns: The properly formatted lookup value
    :raises: LookupMismatchError, InvalidLookupTypeError, CurrentlyUnsupportedError
    """
    warnings.warn(
        "The khorosjx.content.__convert_lookup_value function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.base.__convert_lookup_value instead.",
        DeprecationWarning
    )
    _lookup_value = base.__convert_lookup_value(_lookup_value, _lookup_type, _content_type)
    return _lookup_value


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def get_document_info(lookup_value, lookup_type='doc_id', return_fields=[], ignore_exceptions=False):
    """This function obtains the group information for a given document.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.docs.get_document_info` function should be used.

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
    warnings.warn(
        "The khorosjx.content.get_document_info function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.docs.get_document_info instead.",
        DeprecationWarning
    )
    doc_info = docs.get_document_info(lookup_value, lookup_type, return_fields, ignore_exceptions)
    return doc_info


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def __trim_attachments_info(_attachment_info):
    """This function removes certain fields from attachments data captured via the API.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.base.__trim_attachments_info` function should be used.

    :param _attachment_info: List containing dictionaries of attachments retrieved via the API
    :type _attachment_info: list
    :returns: The trimmed list of dictionaries
    """
    warnings.warn(
        "The khorosjx.content.__trim_attachments_info function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.base.__trim_attachments_info instead.",
        DeprecationWarning
    )
    _attachment_info = base.__trim_attachments_info(_attachment_info)
    return _attachment_info


# This function is deprecated and is only present until v3.0.0 to retain backward compatibility
def get_document_attachments(lookup_value, lookup_type='doc_id', return_dataframe=False):
    """This function retrieves information on any attachments associated with a document.

    .. deprecated:: 2.0.0
       The :py:func:`khorosjx.content.docs.get_document_attachments` function should be used.

    :param lookup_value: The value with which to look up the document
    :type lookup_value: str, int
    :param lookup_type: Identifies the type of lookup value that has been provided (Default: ``doc_id``)
    :type lookup_type: str
    :param return_dataframe: Determines whether or not a pandas dataframe should be returned
    :type return_dataframe: bool
    :returns: A list, dictionary or pandas dataframe depending on the number of attachments and/or function arguments
    :raises: GETRequestError, InvalidDatasetError, InvalidLookupTypeError, LookupMismatchError
    """
    warnings.warn(
        "The khorosjx.content.get_document_attachments function is deprecated and will be removed in v3.0.0. Use " +
        "khorosjx.content.docs.get_document_attachments instead.",
        DeprecationWarning
    )
    attachment_info = docs.get_document_attachments(lookup_value, lookup_type, return_dataframe)
    return attachment_info
