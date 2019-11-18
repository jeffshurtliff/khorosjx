# -*- coding: utf-8 -*-
"""
:Package:        khorosjx.errors
:Synopsis:       This package includes custom exceptions and accompanying function
:Usage:          ``import khorosjx.errors`` (Imported by default in primary package)
:Example:        ``khorosjx.errors.raise_exception('missing_username_or_password')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  15 Nov 2019
:Version:        1.0.0
"""
# Define all modules that will be imported with the "import *" method
__all__ = ['exceptions']

# Always import the exceptions module
from . import exceptions


# Define function to raise a Khoros JX exception
def raise_exception(exception_name):
    """This function raises a custom exception with a specific error message.

    :param exception_name: A nickname for the exception to be raised
    :type exception_name: str
    :returns: None
    :raises: KhorosJXError
    """
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
