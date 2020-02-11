# -*- coding: utf-8 -*-
"""
:Module:        khorosjx.errors.exceptions
:Synopsis:      Collection of exception classes relating to the khorosjx library
:Usage:         ``import khorosjx.errors.exceptions``
:Example:       ``raise khorosjx.errors.exceptions.BadCredentialsError``
:Created By:    Jeff Shurtliff
:Last Modified: Jeff Shurtliff
:Modified Date: 22 Jan 2020
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
        super().__init__(*args)


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
        super().__init__(*args)


class IncompleteCredentialsError(KhorosJXError, IndexError):
    """This exception is used when a tuple containing API credentials is missing a username or password."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API credentials are missing a username or password."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class CredentialsUnpackingError(KhorosJXError, IndexError):
    """This exception is used when the tuple containing API credentials cannot be unpacked."""
    def __init__(self, *args, **kwargs):
        default_msg = "The tuple for API credentials should only contain a username and a password and cannot be " + \
                      "unpacked due to mismatched values."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class WrongCredentialTypeError(KhorosJXError, TypeError):
    """This exception is used when a username or password is not in string format."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API username and password must both be in string format."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class BadCredentialsError(KhorosJXError):
    """This exception is used when the supplied API credentials are incorrect."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API username and password combination is incorrect."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# ------------------
# Content Exceptions
# ------------------


# Define content exception classes
class ContentNotFoundError(KhorosJXError, ValueError):
    """This exception is used when an API query for content returns a 404 status code."""
    def __init__(self, *args, **kwargs):
        default_msg = "The queried content could not be found by the Core API."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class ContentPublishError(KhorosJXError):
    """This exception is used when content is unable to publish successfully."""
    def __init__(self, *args, **kwargs):
        default_msg = "The content failed to publish."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


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
        super().__init__(*args)


class POSTRequestError(KhorosJXError):
    """This exception is used for generic POST request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The POST request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(KhorosJXError):
    """This exception is used for generic PUT request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The PUT request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(KhorosJXError):
    """This exception is used when an invalid API request type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidLookupTypeError(KhorosJXError):
    """This exception is used when an invalid API lookup type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(KhorosJXError):
    """This exception is used when an a lookup value doesn't match the supplied lookup type."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidEndpointError(KhorosJXError):
    """This exception is used when an invalid API endpoint / service is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied endpoint for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'people' and 'contents')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIConnectionError(KhorosJXError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(KhorosJXError):
    """This exception is used when an API query returns a 404 response and there isn't a more specific class."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)

# --------------------------
# Generic Non-API Exceptions
# --------------------------


class InvalidDatasetError(KhorosJXError, ValueError):
    """This exception is used when a supplied dataset is invalid."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied value is not a valid dataset."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class DatasetNotFoundError(KhorosJXError, ValueError):
    """This exception is used when a dataset was not provided and/or cannot be found."""
    def __init__(self, *args, **kwargs):
        default_msg = "A valid dataset could not be found or was not provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidFileTypeError(KhorosJXError, ValueError):
    """This exception is used when a supplied file type is invalid and cannot be used."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied value is not a valid file type and cannot be utilized."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidScopeError(KhorosJXError, ValueError):
    """This exception is used when a supplied scope is invalid and cannot be found."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied value is not a valid scope."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class CurrentlyUnsupportedError(KhorosJXError):
    """This exception is used when an operation is attempted that is not yet supported."""
    def __init__(self, *args, **kwargs):
        default_msg = "The attempted operation is not yet supported. Please try again in a future version."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)

# -----------------
# Helper Exceptions
# -----------------


class InvalidHelperArgumentsError(KhorosJXError, ValueError):
    """THis exception is used when the helper function was supplied arguments instead of keyword arguments."""
    def __init__(self, *args, **kwargs):
        default_msg = "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class HelperFunctionNotFoundError(KhorosJXError, FileNotFoundError):
    """This exception is used when a function referenced in the helper config file does not exist."""
    def __init__(self, *args, **kwargs):
        default_msg = "The function referenced in the helper configuration file could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# ---------------
# News Exceptions
# ---------------


class SubscriptionNotFoundError(KhorosJXError):
    """This exception is used when a subscription referenced in a function does not exist."""

    def __init__(self, *args, **kwargs):
        default_msg = "The Subscription ID could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# -----------------
# Spaces Exceptions
# -----------------


class SpaceNotFoundError(KhorosJXError):
    """This exception is used when an API query for a space returns a 404 response."""
    def __init__(self, *args, **kwargs):
        default_msg = "The Place ID does not exist and the API returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


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
        super().__init__(*args)


class UserNotFoundError(KhorosJXError, ValueError):
    """This exception is used when an API query for a user returns a 404 status code."""
    def __init__(self, *args, **kwargs):
        default_msg = "The queried user could not be found by the Core API."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
