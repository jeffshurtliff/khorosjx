# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.errors.exceptions
:Synopsis:       Collection of exception classes relating to the khorosjx library
:Usage:          import khorosjx.errors.exceptions
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  23 Nov 2019
"""


#######################
# Khoros JX Exceptions
#######################

# --------------
# Base Exception
# --------------


# Define base exception classes
class KhorosJXError(Exception):
    """This is the base class for Khoros JX exceptions."""
    pass


# ------------------------
# Module Import Exceptions
# ------------------------


# Define module import exception classes
class InvalidKhorosJXModuleError(KhorosJXError, ModuleNotFoundError):
    """This exception is used when an invalid module is attempted to be initialized from the primary __init__ file."""
    def __init__(self, *args, **kwargs):
        default_msg = "The module to be initiated is invalid and cannot be imported."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


# -------------------------
# Authentication Exceptions
# -------------------------


# Define authentication exception classes
class NoCredentialsError(KhorosJXError, NameError):
    """This exception is used when credentials weren't found when utilizing the core functions."""
    def __init__(self, *args, **kwargs):
        default_msg = "The base URL and API credentials have not yet been defined.\nRun the khorosjx.core.connect" + \
                      "(base_url, api_credentials) function prior to calling any other khorosjx functions."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class IncompleteCredentialsError(KhorosJXError, IndexError):
    """This exception is used when a tuple containing API credentials is missing a username or password."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API credentials are missing a username or password."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class CredentialsUnpackingError(KhorosJXError, IndexError):
    """This exception is used when the tuple containing API credentials cannot be unpacked."""
    def __init__(self, *args, **kwargs):
        default_msg = "The tuple for API credentials should only contain a username and a password and cannot be " + \
                      "unpacked due to mismatched values."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class WrongCredentialTypeError(KhorosJXError, TypeError):
    """This exception is used when a username or password is not in string format."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API username and password must both be in string format."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class BadCredentialsError(KhorosJXError):
    """This exception is used when the supplied API credentials are incorrect."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API username and password combination is incorrect."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


# ------------------
# Content Exceptions
# ------------------


# Define content exception classes
class ContentPublishError(KhorosJXError):
    """This exception is used when content is unable to publish successfully."""
    def __init__(self, *args, **kwargs):
        default_msg = "The content failed to publish."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


# ----------------------
# Generic API Exceptions
# ----------------------


# Define generic REST API exception classes
class GETRequestError(KhorosJXError):
    """This exception is used for generic GET request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The GET request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class POSTRequestError(KhorosJXError):
    """This exception is used for generic POST request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The POST request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class PUTRequestError(KhorosJXError):
    """This exception is used for generic PUT request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The PUT request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class InvalidRequestTypeError(KhorosJXError):
    """This exception is used when an invalid API request type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class InvalidLookupTypeError(KhorosJXError):
    """This exception is used when an invalid API lookup type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class InvalidEndpointError(KhorosJXError):
    """This exception is used when an invalid API endpoint / service is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied endpoint for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'people' and 'contents')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class APIConnectionError(KhorosJXError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


# --------------------------
# Generic Non-API Exceptions
# --------------------------


class InvalidDatasetError(KhorosJXError, ValueError):
    """This exception is used when a supplied dataset is invalid and cannot be found."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied value is not a valid dataset."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class InvalidScopeError(KhorosJXError, ValueError):
    """This exception is used when a supplied scope is invalid and cannot be found."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied value is not a valid scope."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


# ---------------
# User Exceptions
# ---------------


# Define user exception classes
class UserQueryError(KhorosJXError, ValueError):
    """This exception is used when an API query returns an unidentified non-200 response."""
    def __init__(self, *args, **kwargs):
        default_msg = "The Core API query for the user failed for an unknown reason."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)


class UserNotFoundError(KhorosJXError, ValueError):
    """This exception is used when an API query for a user returns a 404 status code."""
    def __init__(self, *args, **kwargs):
        default_msg = "The queried user could not be found by the Core API."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args, **kwargs)
