# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.videos
:Synopsis:          Collection of functions relating to videos (e.g. https://community.example.com/videos/1234)
:Usage:             ``from khorosjx.content import videos``
:Example:           ``content_id = videos.get_content_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Jan 2020
"""

import os.path

from .. import core, errors
from . import base
from ..utils import core_utils


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


def get_video_id(lookup_value, lookup_type='url'):
    """This function returns the video ID for a video when given its URL or a Content ID.

    :param lookup_value: The URL or Content ID with which to identify the video
    :type lookup_value: str, int
    :param lookup_type: Defines the type of value given to identify the video as ``url`` (default) or ``content_id``
    :type lookup_type: str
    :returns: The Video ID for the video
    :raises: InvalidLookupTypeError
    """
    if lookup_type == 'url':
        video_id = lookup_value.split('videos/')[1]
    elif lookup_type == 'content_id' or lookup_type == 'id':
        video_json = core.get_data('contents', lookup_value, return_json=True)
        video_id = video_json['id']
    else:
        errors.handlers.bad_lookup_type(lookup_type, ('url', 'content_id'))
    return video_id


def __construct_url_from_id(_video_id):
    """This function returns the URL to a video when supplied its Video ID."""
    return f"{core.get_base_url(api_base=False)}/videos/{_video_id}"


# Define function to get the content ID from a URL
def get_content_id(lookup_value, lookup_type='url'):
    """This function obtains the Content ID for a particular video.

    :param lookup_value: The URL or Video ID associated with the video
    :type lookup_value: str, int
    :param lookup_type: Defines the type of value given to identify the video as ``url`` (default) or ``id``
    :returns: The Content ID for the video
    :raises: ValueError, InvalidLookupTypeError
    """
    accepted_lookup_types = ['url', 'id', 'video_id']
    if lookup_type not in accepted_lookup_types:
        errors.handlers.bad_lookup_type(lookup_type, ('url', 'id'))
    if lookup_type != 'url':
        lookup_value = __construct_url_from_id(lookup_value)
    content_id = base.get_content_id(lookup_value, 'video')
    return content_id


# Define function to download a video when supplied with its download URL
def download_video(video_url, output_path, output_name="", default_type="mp4", verbose=False):
    """This function downloads a video file when provided its URLs and an output name and location.

    :param video_url: The direct download URL with its accompanying authorization token
    :type video_url: str
    :param output_path: The full path to the directory where the video file should be downloaded
    :type output_path: str
    :param output_name: The name of the output file (e.g. ``video.mp4``)
    :type output_name: str
    :param default_type: Defines a default file extension (``mp4`` by default) if an extension is not found
    :type default_type: str
    :param verbose: Determines if verbose console output should be displayed (``False`` by default)
    :type verbose: bool
    :returns: None
    """
    try:
        if "." not in output_name:
            output_name = f"{output_name}.{default_type}"
        output_path = os.path.join(output_path, output_name)
        api_response = core.get_request_with_retries(video_url)
        core_utils.print_if_verbose('Processing...', verbose)
        f = open(output_path, 'wb')
        for chunk in api_response.iter_content(chunk_size=255):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
        core_utils.print_if_verbose(f'The video has been exported here: {output_path}', verbose)
        f.close()
    except Exception as exception_msg:
        print(f"The video could not be downloaded due to the following error: {exception_msg}")
    return


def get_native_videos_for_space(browse_id, return_fields=[], return_type='list', ignore_exceptions=False):
    """This function returns information on all native (i.e. non-attachment and not third party) for a given space.

    :param browse_id: The Browse ID associated with the space
    :type browse_id: int, str
    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param return_type: Determines if the data should be returned in a list or a pandas dataframe (Default: ``list``)
    :type return_type: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of dictionaries or a dataframe containing information for each group
    :raises: InvalidDatasetError
    """
    def __append_videos(_all_videos, _query, _start_index, _return_fields, _ignore_exceptions):
        """This function retrieves paginated results and appends them to a master list."""
        _videos = core.get_paginated_results(_query, 'video', _start_index, filter_info=('type', 'video'),
                                             return_fields=_return_fields, ignore_exceptions=_ignore_exceptions)
        _all_videos = core_utils.add_to_master_list(_videos, _all_videos)
        return _all_videos, len(_videos)
        
    # Initialize the master list that will contain all of the video data
    all_videos = []

    # Perform the first query to get up to the first 100 groups
    start_index = 0
    query = core.get_query_url('places', browse_id, 'contents')
    all_videos, assets_returned = __append_videos(all_videos, query, start_index, return_fields, ignore_exceptions)

    # Continue querying for videos until none are returned
    while assets_returned > 0:
        start_index += 100
        all_videos, assets_returned = __append_videos(all_videos, query, start_index, return_fields, ignore_exceptions)

    # Return the data as a master list of group dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_videos = core_utils.convert_dict_list_to_dataframe(all_videos)
    return all_videos


def find_video_attachments(document_attachments):
    """This function identifies any attached videos in a collection of document attachments.

    :param document_attachments: Attachments associated with a document
    :type document_attachments: list, dict
    :returns: A list of dictionaries containing info on any video attachments
    """
    if isinstance(document_attachments, dict):
        document_attachments = [document_attachments]
    video_info_list = []
    for collection in document_attachments:
        if "video" in collection['contentType']:
            size = round(collection['size']/1048576, 2)
            video_info_list.append({"download_url": collection['url'], "size": size})
    return video_info_list


def get_video_info(lookup_value, lookup_type='content_id'):
    """This function retrieves information about a given video in JSON format.

    :param lookup_value: The value with which to look up the video
    :type lookup_value: str, int
    :param lookup_type: Defines whether the lookup value is a ``content_id`` (default), ``video_id`` or ``url``
    :type lookup_type: str
    :returns: The video information in JSON format
    """
    accepted_lookup_types = ['url', 'content_id', 'video_id']
    if lookup_type not in accepted_lookup_types:
        errors.handlers.bad_lookup_type(lookup_type, ('url', 'content_id'))
    if lookup_type != 'content_id':
        if lookup_type == 'video_id':
            lookup_value = __construct_url_from_id(lookup_type)
        lookup_value = get_content_id(lookup_value, 'url')
    return core.get_data('contents', lookup_value, return_json=True)


def check_if_embedded(lookup_value, lookup_type='content_id'):
    """This function checks to see if a native video is embedded in a document or just a standalone video.

    :param lookup_value: The value with which to look up the video
    :type lookup_value: str, int
    :param lookup_type: Defines if the lookup value is a ``content_id`` (default), ``video_id`` or ``url``
    :type lookup_type: str
    :returns: A Boolean value indicating whether or not the video is embedded
    :raises: InvalidLookupTypeError
    """
    video_json = get_video_info(lookup_value, lookup_type)
    return video_json['embedded']


def get_video_dimensions(lookup_value, lookup_type='content_id'):
    """This function returns the dimensions of a given video.

    :param lookup_value: The value with which to look up the video
    :type lookup_value: str, int
    :param lookup_type: Defines if the lookup value is a ``content_id`` (default), ``video_id`` or ``url``
    :type lookup_type: str
    :returns: The video dimensions in string format
    :raises: InvalidLookupTypeError
    """
    video_json = get_video_info(lookup_value, lookup_type)
    dimensions = f"{video_json['width']}x{video_json['height']}"
    return dimensions
