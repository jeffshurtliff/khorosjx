# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.news
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import news``
:Example:        ``all_publication = khorosjx.news.get_all_publications()``
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


def get_all_publications(return_fields=[], return_type='list', ignore_exceptions=False):
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
    query = f'{base_url}/publications'
    start_index = 0
    publications = core.get_paginated_results(query, 'publications', start_index, return_fields=return_fields,
                                              ignore_exceptions=ignore_exceptions)
    all_publications = core_utils.add_to_master_list(publications, all_publications)

    # Continue querying for groups until none are returned
    while len(publications) > 0:
        start_index += 100
        publications = core.get_paginated_results(query, 'publications', start_index, return_fields=return_fields,
                                                  ignore_exceptions=ignore_exceptions)
        all_publications = core_utils.add_to_master_list(publications, all_publications)

    # Return the data as a master list of publication dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_publications = df_utils.convert_dict_list_to_dataframe(all_publications)
    return all_publications


def get_publication(pub_id, return_fields=[], ignore_exceptions=False):
    """This function retrieves the information on a single publication when supplied its ID.

    :param pub_id: The ID of the publication
    :type pub_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the data for the publication
    :raises: InvalidDatasetError, GETRequestError
    """
    publication = core.get_data('publications', pub_id, return_json=True, all_fields=True)
    successful_response = errors.handlers.check_api_response(publication, ignore_exceptions=ignore_exceptions)
    if successful_response:
        publication = core.get_fields_from_api_response(publication, 'publication', return_fields)
    return publication


def delete_publication(pub_id, return_json=False):
    """This function deletes a publication when given its ID.

    :param pub_id: The ID of the publication
    :type pub_id: int, str
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    """
    publication_uri = f"{base_url}/publications/{pub_id}"
    response = core.delete(publication_uri, return_json=return_json)
    return response


def get_subscription_data(pub_id):
    """This function returns the subscription data for a given publication.

    :param pub_id: The ID of the publication
    :type pub_id: int, str
    :returns: A list of dictionaries containing the data for each subscription
    """
    return get_publication(pub_id, ['subscriptions'])


def get_subscription_ids(pub_id, return_type='str'):
    """This function compiles a list of subscription IDs for a given publication ID.

    :param pub_id: The ID of the publication
    :type pub_id: int, str
    :param return_type: Determines if the IDs should be returned in ``str`` (default) or ``int`` format
    :returns: A list of subscription IDs
    :raises: ValueError
    """
    subscription_ids = []
    all_subscriptions = get_subscription_data(pub_id)
    for subscription in all_subscriptions:
        sub_id = subscription['id']
        if return_type == 'int':
            sub_id = int(sub_id)
        elif return_type != 'str':
            raise ValueError(f"'{return_type}' is not a valid return type")
        subscription_ids.append(sub_id)
    return subscription_ids


def get_subscriber_groups(publication_id, subscription_id='', full_uri=False):
    """This function identifies the subscriber groups for one or more subscriptions within a publication.

    :param publication_id: The ID of the publication
    :type publication_id: int, str
    :param subscription_id: The specific subscription ID for which to return subscriber groups (Optional)
    :type subscription_id: int, str
    :param full_uri: Determines whether or not to return the full URI or just the Group ID (``False`` by default)
    :type full_uri: bool
    :returns: A dictionary mapping the subscription IDs to the respective subscriber groups
    :raises: SubscriptionNotFoundError
    """
    def __filter_subscriptions_by_id(_sub_id, _subscriptions):
        for _subscription in _subscriptions:
            if _subscription['id'] == _sub_id:
                return _subscription
        raise errors.exceptions.SubscriptionNotFoundError

    # Capture the subscriber groups for each subscription
    subscriptions = get_subscription_data(publication_id)

    # Filter for a specific subscription if an ID is provided
    if subscription_id != '':
        subscriptions = __filter_subscriptions_by_id(subscription_id, subscriptions)

    # Capture the subscriber groups
    subscriber_groups = {}
    for subscription in subscriptions:
        if full_uri:
            subscriber_groups[subscription['id']] = subscription['subscribers']
        else:
            subscribers = []
            for subscriber in subscription['subscribers']:
                subscribers.append(subscriber.split('securityGroups/')[1])
            subscriber_groups[subscription['id']] = subscribers
    return subscriber_groups


def get_subscribers(publication_id, subscription_id='', full_uri=False):
    # TODO: https://developers.jivesoftware.com/api/v3/cloud/rest/PublicationService.html#getSubscriberUsers(long,%20long,%20int,%20int,%20String)
    pass


