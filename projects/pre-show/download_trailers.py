#!/usr/bin/env python

"""This is a Python script to download HD trailers from the Apple Trailers
website. It uses the same "Just Added" JSON endpoint to discover new trailers
that is used on the trailers website and keeps track of the ones it has
already downloaded so they aren't re-downloaded.

Some imports are declared inside of functions, so that this script can be
# used as a library from other Python scripts, without requiring unnecessary
# dependencies to be installed.
"""

# Started on: 10.14.2011
#
# Copyright 2011-2017 Adam Goforth
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import io
import json
import logging
import os.path
import re
import shutil
import socket

try:
    # For Python 3.0 and later
    from configparser import ConfigParser
    from configparser import Error
    from configparser import MissingSectionHeaderError
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError
    from urllib.error import URLError
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2's naming
    from ConfigParser import Error
    from ConfigParser import MissingSectionHeaderError
    from ConfigParser import SafeConfigParser as ConfigParser
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError
    from urllib2 import URLError
    from urlparse import urlparse


def get_trailer_file_urls(page_url, res, types, download_all_urls):
    """Get all trailer file URLs from the given movie page in the given
    resolution and having the given trailer types.
    """
    urls = []

    # Strip trailing slash from URL if it exists
    if page_url and page_url[-1] == "/":
        page_url = page_url[:-1]

    film_data = load_json_from_url(page_url + '/data/page.json')
    if not film_data:
        return urls

    title = film_data['page']['movie_title']
    apple_size = map_res_to_apple_size(res)

    # Remove beginning, end, and duplicate whitespace from titles
    all_video_types = [' '.join(c['title'].split()) for c
                       in film_data['clips']]
    download_types = get_download_types(types, all_video_types)

    # The user wants all videos from this movie regardless of the video_types
    # setting
    download_all = get_url_path(page_url) in download_all_urls

    for clip in film_data['clips']:
        # Remove beginning, end, and duplicate whitespace
        video_type = ' '.join(clip['title'].split())

        if video_type in download_types or download_all:
            if apple_size in clip['versions']['enus']['sizes']:
                file_info = clip['versions']['enus']['sizes'][apple_size]
                urls.append({
                    'res': res,
                    'title': title,
                    'type': video_type,
                    'url': convert_src_url_to_file_url(file_info['src'], res),
                })
            else:
                logging.error('*** No %sp file found for %s', res, video_type)

    return urls


def map_res_to_apple_size(res):
    """Map a video resolution to the equivalent value used in the data JSON file.
    """
    res_mapping = {'480': u'sd', '720': u'hd720', '1080': u'hd1080'}
    if res not in res_mapping:
        res_string = ', '.join(res_mapping.keys())
        raise ValueError("Invalid resolution. Valid values: %s" % res_string)

    return res_mapping[res]


def convert_src_url_to_file_url(src_url, res):
    """Convert a video source URL as specified in the data JSON to the actual
    URL used on the server."""
    src_ending = "_%sp.mov" % res
    file_ending = "_h%sp.mov" % res
    return src_url.replace(src_ending, file_ending)


def get_download_types(requested_types, all_video_types):
    """Given the requested video types and all video types for this movie,
    return the list of types that should be downloaded"""
    download_types = []
    requested_types = requested_types.lower()

    # Normalize whitespace
    video_types = [' '.join(t.split()) for t in all_video_types]

    # Remove types that were empty or only whitespace
    video_types = [t for t in video_types if t]

    # Remove duplicates
    video_types = list(set(video_types))

    # Sort for consistent results and finding the first trailer
    video_types = sorted(video_types)

    if requested_types == 'all':
        download_types = video_types

    elif requested_types == 'single_trailer':
        video_types = [t for t in video_types
                       if t.lower().startswith('trailer')]
        download_types = video_types[0:1]

    elif requested_types == 'trailers':
        download_types = [t for t in video_types
                          if t.lower().startswith('trailer')
                          or t.lower().startswith('teaser')
                          or t.lower() == 'first look']

    return download_types


def get_downloaded_files(dl_list_path):
    """Get the list of downloaded files from the text file"""
    file_list = []
    if os.path.exists(dl_list_path):
        utf8_file = io.open(dl_list_path, mode='r', encoding='utf-8')
        for line in utf8_file:
            file_list.append(line.strip())
        utf8_file.close()
    return file_list


def write_downloaded_files(file_list, dl_list_path):
    """Write the list of downloaded files to the text file"""
    new_list = [filename + u'\n' for filename in file_list]
    downloads_file = io.open(dl_list_path, mode='w', encoding='utf-8')
    downloads_file.writelines(new_list)
    downloads_file.close()


def record_downloaded_file(filename, dl_list_path):
    """Appends the given filename to the text file of already downloaded
    files"""
    file_list = get_downloaded_files(dl_list_path)
    file_list.append(filename)
    write_downloaded_files(file_list, dl_list_path)


def file_already_downloaded(file_list, movie_title, video_type, res,
                            requested_types):
    """Returns true if the file_list contains a file that matches the file
    properties."""

    if requested_types.lower() == 'single_trailer':
        clean_title = clean_movie_title(movie_title)
        trailer_prefix = '{}.trailer'.format(clean_title.lower())
        movie_trailers = [f for f in file_list
                          if f.lower().startswith(trailer_prefix)]
        return bool(movie_trailers)

    trailer_file_name = get_trailer_filename(movie_title, video_type, res)
    return trailer_file_name in file_list


def download_trailer_file(url, destdir, filename):
    """Accepts a URL to a trailer video file and downloads it
    You have to spoof the user agent or the site will deny the request
    Resumes partial downloads and skips fully-downloaded files"""
    file_path = os.path.join(destdir, filename)
    file_exists = os.path.exists(file_path)

    existing_file_size = 0
    if file_exists:
        existing_file_size = os.path.getsize(file_path)

    data = None
    headers = {}

    resume_download = False
    if file_exists and (existing_file_size > 0):
        resume_download = True
        headers['Range'] = 'bytes={}-'.format(existing_file_size)

    req = Request(url, data, headers)

    try:
        server_file_handle = urlopen(req)
    except HTTPError as ex:
        if ex.code == 416:
            logging.debug("*** File already downloaded, skipping")
            return

        if ex.code == 404:
            logging.error("*** Error downloading file: file not found")
            return

        logging.error("*** Error downloading file")
        return
    except URLError:
        logging.error("*** Error downloading file")
        return

    # Buffer 1MB at a time
    chunk_size = 1024 * 1024

    try:
        if resume_download:
            logging.debug("  Resuming file %s", file_path)
            with open(file_path, 'ab') as local_file_handle:
                shutil.copyfileobj(server_file_handle, local_file_handle,
                                   chunk_size)
        else:
            logging.debug("  Saving file to %s", file_path)
            with open(file_path, 'wb') as local_file_handle:
                shutil.copyfileobj(server_file_handle, local_file_handle,
                                   chunk_size)
    except socket.error as ex:
        logging.error("*** Network error while downloading file: %s", ex)
        return


def download_trailers_from_page(page_url, settings):
    """Takes a page on the Apple Trailers website and downloads the trailer
    for the movie on the page. Example URL:
    http://trailers.apple.com/trailers/lions_gate/thehungergames/"""

    logging.debug('Checking for files at %s', page_url)
    trailer_urls = get_trailer_file_urls(page_url, settings['resolution'],
                                         settings['video_types'],
                                         settings['download_all_urls'])
    downloaded_files = get_downloaded_files(settings['list_file'])

    for trailer_url in trailer_urls:
        trailer_file_name = get_trailer_filename(trailer_url['title'],
                                                 trailer_url['type'],
                                                 trailer_url['res'])
        already_downloaded = (
            file_already_downloaded(downloaded_files, trailer_url['title'],
                                    trailer_url['type'], trailer_url['res'],
                                    settings['video_types'])
        )

        if not already_downloaded:
            logging.info('Downloading %s: %s', trailer_url['type'],
                         trailer_file_name)
            download_trailer_file(trailer_url['url'], settings['download_dir'],
                                  trailer_file_name)
            record_downloaded_file(trailer_file_name, settings['list_file'])
        else:
            logging.debug('*** File already downloaded, skipping: %s',
                          trailer_file_name)


def clean_movie_title(title):
    """Take a movie title and convert it to a safe, normalized title for use
    in filenames.
    In addition to stripping leading and trailing whitespace from the title
    and converting to unicode, this function also removes characters that
    should not be used in filenames on various operating systems."""
    clean_title = u''.join(s for s in title
                           if s not in r'\/:*?<>|#%&{}$!\'"@+`=')
    # Remove repeating spaces
    clean_title = re.sub(r'\s\s+', ' ', clean_title).strip()

    return clean_title


def get_trailer_filename(film_title, video_type, res):
    """Take video info and convert it to a cononical filename."""
    clean_title = clean_movie_title(film_title)
    trailer_file_name = u'{}.{}.{}p.mov'.format(clean_title, video_type, res)
    return trailer_file_name


def get_url_path(url):
    """Take a full URL and reduce it to just the path, with starting and ending
    whitespace as well as the trailing slash removed, if they exist."""
    url = url.strip()
    path = urlparse(url).path
    if path and path[-1] == "/":
        path = path[:-1]

    return path


def validate_settings(settings):
    """Validate the settings in the given dictionary. If any setting is
    invalid, raises an Error with a user message"""
    valid_resolutions = ['480', '720', '1080']
    valid_video_types = ['single_trailer', 'trailers', 'all']
    valid_output_levels = ['debug', 'downloads', 'error']

    required_settings = ['resolution', 'download_dir', 'video_types',
                         'output_level', 'list_file']

    for setting in required_settings:
        if setting not in settings:
            raise ValueError("cannot find value for '{}'".format(setting))

    if settings['resolution'] not in valid_resolutions:
        res_string = ', '.join(valid_resolutions)
        raise ValueError("invalid resolution. Valid values: {}"
                         .format(res_string))

    if not os.path.exists(settings['download_dir']):
        raise ValueError('the download directory must be a valid path')

    if settings['video_types'].lower() not in valid_video_types:
        types_string = ', '.join(valid_video_types)
        raise ValueError("invalid video type. Valid values: {}"
                         .format(types_string))

    if settings['output_level'].lower() not in valid_output_levels:
        output_string = ', '.join(valid_output_levels)
        raise ValueError("invalid output level. Valid values: {}"
                         .format(output_string))

    if not os.path.exists(os.path.dirname(settings['list_file'])):
        raise ValueError('the list file directory must be a valid path')

    return True


def get_config_values(config_path, defaults):
    """Get the script's configuration values and return them in a dict

    If a config file exists, merge its values with the defaults. If no config
    file exists, just return the defaults.
    """

    config = ConfigParser(defaults)
    config_values = config.defaults()

    config_paths = [
        config_path,
        os.path.join(os.path.expanduser('~'), '.trailers.cfg'),
    ]

    config_file_found = False
    for path in config_paths:
        if os.path.exists(path):
            config_file_found = True
            config.read(path)
            config_values = config.defaults()
            break

    if config_values.get('download_all_urls', ''):
        config_values['download_all_urls'] = (
            [get_url_path(s) for
             s in config_values['download_all_urls'].split(',')])
    else:
        config_values['download_all_urls'] = []

    if not config_file_found:
        logging.info('Config file not found. Using default values.')

    return config_values


def get_settings():
    """Validate and return the user's settings as a combination of the default
    settings, the settings file (if it exists) and the command-line options
    (if given)."""

    # Don't include list_file in the defaults, because the default value is
    # dependent on the configured download_dir, which isn't known until the
    # command line and config file have been parsed.
    script_dir = os.path.abspath(os.path.dirname(__file__))
    defaults = {
        'download_dir': script_dir,
        'output_level': 'debug',
        'resolution': '720',
        'video_types': 'single_trailer',
    }

    args = get_command_line_arguments()

    config_path = args.get('config_path', "{}/settings.cfg".format(script_dir))
    config = get_config_values(config_path, defaults)

    settings = config.copy()
    settings.update(args)

    settings['download_dir'] = os.path.expanduser(settings['download_dir'])
    settings['config_path'] = config_path

    if ('list_file' not in args) and ('list_file' not in config):
        settings['list_file'] = os.path.join(
            settings['download_dir'],
            'download_list.txt'
        )

    settings['list_file'] = os.path.expanduser(settings['list_file'])

    validate_settings(settings)

    return settings


def get_command_line_arguments():
    """Return a dictionary containing all of the command-line arguments
    specified when the script was run.
    """

    parser = argparse.ArgumentParser(
        description='Download movie trailers from the Apple website. With no '
        'arguments, will download all of the trailers in the current '
        '"Just Added" list. When a trailer page URL is specified, will only '
        'download the single trailer at that URL. Example URL: '
        'http://trailers.apple.com/trailers/lions_gate/thehungergames/'
    )

    parser.add_argument(
        '-c, --config',
        action='store',
        dest='config',
        help='The location of the config file. Defaults to "settings.cfg"' +
        'in the script directory.'
    )

    parser.add_argument(
        '-d, --dir',
        action='store',
        dest='dir',
        help='The directory to which the trailers should be downloaded. ' +
        'Defaults to the script directory.'
    )

    parser.add_argument(
        '-l, --listfile',
        action='store',
        dest='filepath',
        help='The location of the download list file. The names of the ' +
        'previously downloaded trailers are stored in this file. ' +
        'Defaults to "download_list.txt" in the download directory.'
    )

    parser.add_argument(
        '-r, --resolution',
        action='store',
        dest='resolution',
        help='The preferred video resolution to download. Valid options are ' +
        '"1080", "720", and "480".'
    )

    parser.add_argument(
        '-u, --url',
        action='store',
        dest='url',
        help='The URL of the Apple Trailers web page for a single trailer.'
    )

    parser.add_argument(
        '-v, --videotypes',
        action='store',
        dest='types',
        help='The types of videos to be downloaded. Valid options are ' +
        '"single_trailer", "trailers", and "all".'
    )

    parser.add_argument(
        '-o, --output_level',
        action='store',
        dest='output',
        help='The level of console output. Valid options are ' +
        '"debug", "downloads", and "error".'
    )

    results = parser.parse_args()
    args = {
        'config_path': results.config,
        'download_dir': results.dir,
        'list_file': results.filepath,
        'page': results.url,
        'resolution': results.resolution,
        'video_types': results.types,
        'output_level': results.output,
    }

    # Remove all pairs that were not set on the command line.
    set_args = {}
    for name in args:
        if args[name] is not None:
            set_args[name] = args[name]

    return set_args


def configure_logging(output_level):
    """Configure the logger to print messages with at least the level of the given
    configuration value.
    """
    output_level = output_level.lower()

    log_level = logging.DEBUG
    if output_level == 'downloads':
        log_level = logging.INFO
    elif output_level == 'error':
        log_level = logging.ERROR

    logging.basicConfig(format='%(message)s')
    logging.getLogger().setLevel(log_level)


def load_json_from_url(url):
    """Takes a URL and returns a Python dict representing the JSON of the
    URL's contents. If there is an error fetching the URL or invalid JSON is
    returned, an empty dict is returned."""
    try:
        response = urlopen(url)
        str_response = response.read().decode('utf-8')
        return json.loads(str_response)
    except (URLError, ValueError):
        logging.error("*** Error: could not load data from %s", url)
        return {}


def main():
    """The main script function.
    """
    # Set default log level so we can log messages generated while loading
    # the settings.
    configure_logging('')

    try:
        settings = get_settings()
    except MissingSectionHeaderError:
        logging.error('Configuration file is missing a header section, '
                      'try adding [DEFAULT] at the top of the file')
        return
    except (Error, ValueError) as ex:
        logging.error("Configuration error: %s", ex)
        return

    configure_logging(settings['output_level'])

    logging.debug("Using configuration values:")
    logging.debug("Loaded configuration from %s", settings['config_path'])
    for name in sorted(settings):
        if name != 'config_path':
            logging.debug("    %s: %s", name, settings[name])

    logging.debug("")

    # Do the download
    if 'page' in settings:
        # The trailer page URL was passed in on the command line
        download_trailers_from_page(settings['page'], settings)

    else:
        just_added_url = ('http://trailers.apple.com/trailers/'
                          'home/feeds/just_added.json')
        newest_trailers = load_json_from_url(just_added_url)

        for trailer in newest_trailers:
            url = 'http://trailers.apple.com' + trailer['location']
            download_trailers_from_page(url, settings)


if __name__ == '__main__':
    main()
