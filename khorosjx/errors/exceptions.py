# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.errors.exceptions
:Synopsis:       Collection of exception classes relating to the khorosjx library
:Usage:          import khorosjx.errors.exceptions
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  17 Nov 2019
:Version:        1.0.0
"""


"""
Khoros JX Exceptions
====================
"""

"""
Base Exception
---------------
"""


# Define base exception classes
class KhorosJXError(Exception):
    """This is the base class for Khoros JX exceptions."""
    pass


"""
Module Import Exceptions
------------------------
"""


# Define module import exception classes
class InvalidKhorosJXModuleError(KhorosJXError, ModuleNotFoundError):
    """This exception is used when an invalid module is attempted to be initialized from the primary __init__ file."""
    def __init__(self, message):
        self.message = message


"""
Authentication Exceptions
-------------------------
"""


# Define authentication exception classes
class NoCredentialsError(KhorosJXError, NameError):
    """This exception is used when credentials weren't found when utilizing the core functions."""
    def __init__(self, message):
        self.message = message


class IncompleteCredentialsError(KhorosJXError, IndexError):
    """This exception is used when a tuple containing API credentials is missing a username or password."""
    def __init__(self, message):
        self.message = message


class CredentialsUnpackingError(KhorosJXError, IndexError):
    """This exception is used when the tuple containing API credentials cannot be unpacked."""
    def __init__(self, message):
        self.message = message


class WrongCredentialTypeError(KhorosJXError, TypeError):
    """This exception is used when a username or password is not in string format."""
    def __init__(self, message):
        self.message = message


"""
User Exceptions
---------------
"""


# Define user exception classes
class UserQueryError(KhorosJXError, ValueError):
    """This exception is used when an API query returns an unidentified non-200 response."""
    def __init__(self, message):
        self.message = message


class UserNotFoundError(KhorosJXError, ValueError):
    """This exception is used when an API query for a user returns a 404 status code."""
    def __init__(self, message):
        self.message = message


"""
Exception Messages
==================
"""


# Define class to map exception "nicknames" to exception classes and accompanying error messages
class ExceptionMapping:
    """This class contains mapping dictionaries relating to raising exceptions with associated error messages."""
    # Define exception messages for module import exceptions
    module_exceptions = {
        'invalid_module': (
            InvalidKhorosJXModuleError,
            "The module to be initiated is invalid and cannot be imported."
        )
    }

    # Define exception messages for authentication exceptions
    authentication_exceptions = {
        'no_credentials': (
            NoCredentialsError,
            "The base URL and API credentials have not yet been defined.\nRun the " +
            "khorosjx.core.connect(base_url, api_credentials) function prior to calling any other khorosjx functions."
        ),
        'missing_username_or_password': (
            IncompleteCredentialsError,
            "The API credentials are missing a username or password."
        ),
        'credentials_unpacking_error': (
            CredentialsUnpackingError,
            "The tuple for API credentials should only contain a username and a password and cannot be " +
            "unpacked due to mismatched values."
        ),
        'credential_type_error': (
            WrongCredentialTypeError,
            "The API username and password must both be in string format."
        )
    }

    # Define exception messages for user exceptions
    user_exceptions = {
        'user_not_found': (
            UserNotFoundError,
            "The queried user could not be found by the Core API."
        ),
        'user_query_error': (
            UserQueryError,
            "The Core API query for the user failed for an unknown reason."
        )
    }


# Define groupings for the various exception classes
class ExceptionGrouping:
    """This class contains list indices for the exception nicknames within the ExceptionMapping class."""
    # Define the lists for each exception category
    module_exceptions_group = ('invalid_module',)
    authentication_exceptions_group = ('no_credentials', 'missing_username_or_password', 'credentials_unpacking_error',
                                       'credential_type_error')
    user_exceptions_group = ('user_not_found', 'user_query_error')

    # Define a dictionary mapping the groupings to the appropriate exception messages dictionary
    exception_group_mapping = {
        module_exceptions_group: ExceptionMapping.module_exceptions,
        authentication_exceptions_group: ExceptionMapping.authentication_exceptions,
        user_exceptions_group: ExceptionMapping.user_exceptions
    }
