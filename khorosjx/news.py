# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.news
:Synopsis:       Collection of functions relating to security groups
:Usage:          ``from khorosjx import news``
:Example:        ``all_publication = khorosjx.news.get_all_publications()``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  11 Feb 2020
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
    publications = core.get_paginated_results(query, 'publication', start_index, return_fields=return_fields,
                                              ignore_exceptions=ignore_exceptions)
    all_publications = core_utils.add_to_master_list(publications, all_publications)

    # Continue querying for groups until none are returned
    while len(publications) > 0:
        start_index += 100
        publications = core.get_paginated_results(query, 'publication', start_index, return_fields=return_fields,
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
    # Verify that the core connection has been established
    verify_core_connection()

    # Retrieve the publication
    publication = core.get_data('publications', pub_id, return_json=False, all_fields=True)
    successful_response = errors.handlers.check_api_response(publication, ignore_exceptions=ignore_exceptions)
    if successful_response:
        publication = core.get_fields_from_api_response(publication.json(), 'publication', return_fields)
    return publication


def delete_publication(pub_id, return_json=False):
    """This function deletes a publication when given its ID.

    :param pub_id: The ID of the publication
    :type pub_id: int, str
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Delete the publication
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
    # Verify that the core connection has been established
    verify_core_connection()

    # Retrieve the subscription IDs
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
        """This function filters the returned IDs by a supplied subscription ID when applicable."""
        for _subscription in _subscriptions:
            if _subscription['id'] == _sub_id:
                return _subscription
        raise errors.exceptions.SubscriptionNotFoundError

    # Verify that the core connection has been established
    verify_core_connection()

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


def get_subscribers(publication_id, subscription_id, return_type='list', only_id=True, return_fields=[],
                    ignore_exceptions=False):
    """This function retrieves the individual subscribers (i.e. users) for a given subscription within a publication.

    :param publication_id: The ID of the publication where the subscription resides
    :type publication_id: int, str
    :param subscription_id: The ID of the subscription in which to identify the subscribers
    :type subscription_id: int, str
    :param return_type: Determines whether the data should be returned as a ``list`` (default) or a pandas ``dataframe``
    :type return_type: str
    :param only_id: Determines if only the ID of each user should be returned (default) or a dict with all user data
    :type only_id: bool
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list or pandas dataframe with the subscriber information
    """
    def __get_subscriber_ids(_subscribers):
        """This function pulls the subscriber IDs out of dictionaries and into a single list."""
        _subscriber_ids = []
        for _subscriber in _subscribers:
            _subscriber_ids.append(_subscriber['id'])
        return _subscriber_ids

    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty list for the subscription information
    all_subscribers = []

    # Overwrite the return_fields list if the only_id value is True
    if only_id:
        return_fields = ['id']

    # Perform the first query to get up to the first 100 groups
    query = f"{base_url}/publications/{publication_id}/subscriptions/{subscription_id}/subscribers"
    start_index = 0
    subscribers = core.get_paginated_results(query, 'people', start_index, return_fields=return_fields,
                                             ignore_exceptions=ignore_exceptions)
    if only_id and return_type == 'list':
        subscribers = __get_subscriber_ids(subscribers)
    all_subscribers = core_utils.add_to_master_list(subscribers, all_subscribers)

    # Continue querying for groups until none are returned
    while len(subscribers) > 0:
        start_index += 100
        subscribers = core.get_paginated_results(query, 'people', start_index, return_fields=return_fields,
                                                 ignore_exceptions=ignore_exceptions)
        if only_id and return_type == 'list':
            subscribers = __get_subscriber_ids(subscribers)
        all_subscribers = core_utils.add_to_master_list(subscribers, all_subscribers)

    # Return the data as a master list of publication dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_subscribers = df_utils.convert_dict_list_to_dataframe(all_subscribers)
    return all_subscribers


def rebuild_publication(publication_id):
    """This function rebuilds a publication.

    :param publication_id: The ID of the publication to be rebuilt
    :type publication_id: int, str
    :returns: The response from the API PUT request
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the PUT request to rebuild the publication
    query = f"{base_url}/publications/{publication_id}/rebuild"
    payload = {}
    response = core.put_request_with_retries(query, payload)
    return response


def update_publication(publication_id, payload):
    """This function updates a publication using the supplied JSON payload.

    :param publication_id: The ID of the publication to be updated
    :type publication_id: int, str
    :param payload: The JSON payload with which the publication will be updated
    :type payload: dict
    :returns: The response from the API PUT request
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the PUT request to update the publication
    query = f"{base_url}/publications/{publication_id}"
    response = core.put_request_with_retries(query, payload)
    return response


def get_stream(stream_id, return_fields=[], ignore_exceptions=False):
    """This function retrieves the information on a single publication when supplied its ID.

    :param stream_id: The ID of the stream to retrieve
    :type stream_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A dictionary with the data for the publication
    :raises: InvalidDatasetError, GETRequestError
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Retrieve the publication
    stream = core.get_data('streams', stream_id, return_json=False, all_fields=True)
    successful_response = errors.handlers.check_api_response(stream, ignore_exceptions=ignore_exceptions)
    if successful_response:
        stream = core.get_fields_from_api_response(stream.json(), 'stream', return_fields)
    return stream


def update_stream(stream_id, payload):
    """This function updates a stream using the supplied JSON payload.

    :param stream_id: The ID of the stream to be updated
    :type stream_id: int, str
    :param payload: The JSON payload with which the stream will be updated
    :type payload: dict
    :returns: The response from the API PUT request
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Perform the PUT request to update the publication
    query = f"{base_url}/streams/{stream_id}"
    response = core.put_request_with_retries(query, payload)
    return response


def delete_stream(stream_id, return_json=False):
    """This function deletes a stream when given its ID.

    :param stream_id: The ID of the stream
    :type stream_id: int, str
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    """
    # Verify that the core connection has been established
    verify_core_connection()

    # Delete the publication
    stream_uri = f"{base_url}/streams/{stream_id}"
    response = core.delete(stream_uri, return_json=return_json)
    return response


# TODO: Add functions relating to the /people/{id}/streams endpoint
