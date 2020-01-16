# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.content.videos
:Synopsis:          Collection of functions relating to videos (e.g. https://community.example.com/videos/1234)
:Usage:             ``from khorosjx.content import videos``
:Example:           ``content_id = videos.get_content_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Jan 2020
"""

import os.path

from .. import core
from . import base
from ..utils.core_utils import print_if_verbose


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


# Define function to get the content ID from a URL
def get_content_id(url):
    """This function obtains the Content ID for a particular video.

    :param url: The URL of the video
    :type url: str
    :returns: The Content ID for the video
    :raises: ValueError
    """
    content_id = base.get_content_id(url, 'video')
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
        print_if_verbose('Processing...', verbose)
        f = open(output_path, 'wb')
        for chunk in api_response.iter_content(chunk_size=255):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
        print_if_verbose(f'The video has been exported here: {output_path}', verbose)
        f.close()
    except Exception as exception_msg:
        print(f"The video could not be downloaded due to the following error: {exception_msg}")
    return


# Define function to get information on all security groups
def get_videos_for_space(return_fields=[], return_type='list', ignore_exceptions=False):
    """This function returns information on all security groups found within the environment.

    :param return_fields: Specific fields to return if not all of the default fields are needed (Optional)
    :type return_fields: list
    :param return_type: Determines if the data should be returned in a list or a pandas dataframe (Default: ``list``)
    :type return_type: str
    :param ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
    :type ignore_exceptions: bool
    :returns: A list of dictionaries containing information for each group
    :raises: InvalidDatasetError
    """
    def __get_paginated_groups(_return_fields, _ignore_exceptions, _start_index):
        """This function returns paginated group information. (Up to 100 records at a time)

        :param _return_fields: Specific fields to return if not all of the default fields are needed (Optional)
        :type _return_fields: list
        :param _ignore_exceptions: Determines whether nor not exceptions should be ignored (Default: ``False``)
        :type _ignore_exceptions: bool
        :param _start_index: The startIndex API value
        :type _start_index: int, str
        :returns: A list of dictionaries containing information for each group in the paginated query
        """
        # Initialize the empty list for the group information
        _groups = []

        # Perform the API query to retrieve the group information
        _query_uri = f"{base_url}/securityGroups?fields=@all&count=100&startIndex={_start_index}"
        _response = core.get_request_with_retries(_query_uri)

        # Verify that the query was successful
        successful_response = errors.handlers.check_api_response(_response, ignore_exceptions=_ignore_exceptions)

        if successful_response:
            # Get the response data in JSON format
            _paginated_group_data = _response.json()
            for _group_data in _paginated_group_data['list']:
                _parsed_data = core.get_fields_from_api_response(_group_data, 'security_group', _return_fields)
                _groups.append(_parsed_data)
        return _groups

    # Verify that the core connection has been established
    verify_core_connection()

    # Initialize the empty list for the group information
    all_groups = []

    # Perform the first query to get up to the first 100 groups
    start_index = 0
    groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
    all_groups = core_utils.add_to_master_list(groups, all_groups)

    # Continue querying for groups until none are returned
    while len(groups) > 0:
        start_index += 100
        groups = __get_paginated_groups(return_fields, ignore_exceptions, start_index)
        all_groups = core_utils.add_to_master_list(groups, all_groups)

    # Return the data as a master list of group dictionaries or a pandas dataframe
    if return_type == "dataframe":
        all_groups = core_utils.convert_dict_list_to_dataframe(all_groups)
    return all_groups



def victor_get_videos_for_space(browse_id):
    start = 0
    max_return = 100
    total = 100000
    video_content_list = []
    while (start < total):
        msg = f"Querying for browse id {browse_id} content starting at index {start}.\n"
        print(msg)
        url = f"https://community.rsa.com/api/core/v3/places/{browse_id}/contents?count=100&startIndex={start}&fields=@all"
        r = khorosjx.core.get_request_with_retries(url)
        json_elements = r.json()['list']
        if json_elements == []:
            break
        for content in json_elements:
            content_id = content['id']
            title = content['subject']
            content_url = content['resources']['html']['ref']

            try:
                content_type = content['typeCode']
            except KeyError:
                content_type = "Unknown"
            video_info_list, video_type = find_video_info(content_url)

            if video_info_list is not None:
                for obj in video_info_list:
                    temp_dict = {
                        "content_id": content_id,
                        "title": title,
                        "content_url": content_url,
                        "content_type": content_type,
                        "video_type": video_type,
                        "download_url": obj['download_url'],
                        'size': obj['size'],
                        "browse_id": browse_id
                    }

                    try:
                        video_content_list.append(pd.DataFrame(temp_dict, index=[0]))
                    except ValueError:
                        video_content_list.append(pd.DataFrame(temp_dict))

        start += max_return
    return pd.concat(video_content_list)