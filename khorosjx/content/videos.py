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
