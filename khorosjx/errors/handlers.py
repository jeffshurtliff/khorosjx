# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.errors.handlers
:Synopsis:       Collection of error handler functions relating to the khorosjx library
:Usage:          ``from khorosjx.errors import handlers``
:Example:        ``successful_response = check_api_response(response)``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  23 Nov 2019
"""

import warnings

from . import exceptions
from ..utils.core_utils import eprint


# Define function to check an API response status code for an error
def check_api_response(response, request_type='get', ignore_exceptions=False):
    """This function checks an API response to determine if it was successful

    :param response: The API response obtained via the requests package
    :type response: class
    :param request_type: The type of API request that was performed. (Default: ``get``)
    :type request_type: str
    :param ignore_exceptions: Determines whether or not exceptions should be ignored and not raised (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A Boolean value indicating whether or not the API request was deemed successful
    :raises: GETRequestError, POSTRequestError, PUTRequestError, BadCredentialsError
    """
    def __raise_exception_for_status_code(_status_code, _request_type, _result_msg=""):
        if _status_code == 401:
            raise exceptions.BadCredentialsError
        if _request_type.lower() == "put":
            raise exceptions.PUTRequestError(_result_msg)
        elif _request_type.lower() == "post":
            raise exceptions.POSTRequestError(_result_msg)
        else:
            raise exceptions.GETRequestError(_result_msg)

    # Define the default return status
    successful_response = True

    # Define the status code and response message from the API response
    status_code = response.status_code
    message = response.text
    if status_code == 502:
        message = "Site Temporarily Unavailable"
    result_msg = f"The API request returned a {status_code} status code with the following message: {message}"

    # Check if the API response was successful
    if (request_type.lower() == "get" and status_code != 200) or \
       (request_type.lower() == "post" and status_code != 204):
        # TODO: Add conditional above for PUT requests
        # Print an error or raise an exception depending on the ignore_exceptions value
        if ignore_exceptions:
            eprint(result_msg)
        else:
            __raise_exception_for_status_code(status_code, request_type, result_msg)
        successful_response = False
    return successful_response


def check_json_for_error(json_data, data_type='space'):
    """This function checks to see if JSON from an API response contains an error.

    :param json_data: The API response data in JSON format
    :type json_data: dict
    :param data_type: Determines what type of data was being queried (Default: ``space``)
    :type data_type: str
    :returns: None
    :raises: SpaceNotFoundError, NotFoundResponseError, GETRequestError
    """
    not_found_exceptions = {
        'space': exceptions.SpaceNotFoundError
    }
    try:
        error_status_code = json_data['error']['status']
        # Check if the error was because the space could not be found
        if error_status_code == 404:
            if data_type in not_found_exceptions:
                raise not_found_exceptions.get(data_type)
            else:
                raise exceptions.NotFoundResponseError
        else:
            exception_msg = f"The API request failed with a {error_status_code} status code and the " + \
                            f"following error: {json_data['error']['message']}"
            raise exceptions.GETRequestError(exception_msg)
    except KeyError:
        pass
    return


def bad_lookup_type(lookup_type, good_examples):
    """This function raises the InvalidLookupTypeError exception and provides a custom message."""
    raise exceptions.InvalidLookupTypeError(f"The lookup type '{lookup_type}' is invalid. " +
                                            f"Use '{good_examples[0]}' or '{good_examples[1]}' instead.")
