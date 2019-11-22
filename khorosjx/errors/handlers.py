# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.errors.handlers
:Synopsis:       Collection of error handler functions relating to the khorosjx library
:Usage:          import khorosjx.errors.handlers
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  22 Nov 2019
"""

import warnings

from . import exceptions


# Define function to raise a Khoros JX exception
def raise_exception(exception_name):
    """This function raises a custom exception with a specific error message.

    :param exception_name: A nickname for the exception to be raised
    :type exception_name: str
    :returns: None
    :raises: KhorosJXError
    """
    # Trigger the deprecation warning for this function
    warning_msg = "The raise_exception() function will soon be deprecated in a future release once the " + \
                  "custom exception classes are all updated to have default messages."
    warnings.warn(warning_msg, PendingDeprecationWarning)

    # Perform the tasks within the function
    for category_list in exceptions.ExceptionGrouping.exception_group_mapping.keys():
        if exception_name in category_list:
            category_exceptions = exceptions.ExceptionGrouping.exception_group_mapping.get(category_list)
            exception_to_raise, error_msg = category_exceptions.get(exception_name)
            raise exception_to_raise(error_msg)
        else:
            print(f"The exception name '{exception_name}' was not recognized and therefore a generic exception " +
                  "will be raised instead.")
            raise exceptions.KhorosJXError("An exception was raised for the current operation.")
    return


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
    :raises: GETRequestError
    """
    # Define the default return status
    successful_response = True

    # Define the status code and response message from the API response
    status_code = response.status_code
    message = response.text

    # Check if the API response was successful
    # TODO: Add support for other request types (e.g. PUT)
    if request_type.lower() == "get" and status_code != 200:
        error_msg = f"The API request returned a {status_code} status code with the following message: {message}"
        if ignore_exceptions:
            warnings.warn(error_msg)
        else:
            if status_code == 401:
                raise exceptions.BadCredentialsError
            if request_type.lower() == "get":
                raise exceptions.GETRequestError(error_msg)
            else:
                raise exceptions.PUTRequestError(error_msg)
        successful_response = False
    return successful_response
