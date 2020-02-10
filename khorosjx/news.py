# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.news
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import news``
:Example:        ``all_publication = khorosjx.news.get_publications()``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  10 Feb 2020
"""

from . import core, errors
from .utils import core_utils, df_utils


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


def get_publications(return_fields=[], return_type='list', ignore_exceptions=False):
    """This function retrieves all publications within an environment.
    
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param return_type: Determines if the data should be returned in a list or a pandas dataframe (Default: ``list``)
    :type return_type: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of dictionaries or a dataframe containing information for each publication
    :raises: InvalidDatasetError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty list for the subscription information
    all_publications = []

    # Perform the first query to get up to the first 100 groups
    dataset = 'publications'
    start_index = 0
    publications = core.get_paginated_results(dataset, dataset, start_index, return_fields=return_fields,
                                              ignore_exceptions=ignore_exceptions)
    all_publications = core_utils.add_to_master_list(publications, all_publications)

    # Continue querying for groups until none are returned
    while len(publications) > 0:
        start_index += 100
        publications = core.get_paginated_results(dataset, dataset, start_index, return_fields=return_fields,
                                                  ignore_exceptions=ignore_exceptions)
        all_publications = core_utils.add_to_master_list(publications, all_publications)

    # Return the data as a master list of publication dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_publications = df_utils.convert_dict_list_to_dataframe(all_publications)
    return all_publications
