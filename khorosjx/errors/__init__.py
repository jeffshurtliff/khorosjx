# -*- coding: utf-8 -*-
"""
:Package:        khorosjx.errors
:Synopsis:       This package includes custom exceptions and accompanying function
:Usage:          ``import khorosjx.errors`` (Imported by default in primary package)
:Example:        ``khorosjx.errors.raise_exception('missing_username_or_password')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  20 Nov 2019
"""
# Define all modules that will be imported with the "import *" method
__all__ = ['exceptions', 'handlers']

# Always import the warnings package and the exceptions module
import warnings

from . import exceptions, handlers


# Define function to raise a Khoros JX exception
def raise_exception(exception_name):
    """This function raises a custom exception with a specific error message.

    :param exception_name: A nickname for the exception to be raised
    :type exception_name: str
    :returns: None
    :raises: KhorosJXError
    """
    # Trigger the deprecation warning for this function
    warning_msg = "The exception_to_raise() function has been moved into the khorosjx.errors.handlers module and " + \
                  "will be removed from the __init__ module within khorosjx.errors in a future release."
    warnings.warn(warning_msg, DeprecationWarning)

    # Call the function from the khorosjx.errors.handlers module
    handlers.raise_exception(exception_name)
    return
