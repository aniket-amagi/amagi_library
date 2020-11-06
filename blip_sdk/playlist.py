#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for consuming Blip Playlist API
"""
import json
import logging
import urllib.request

from datetime import datetime
from urllib.parse import urlencode

try:
    from amagi_library.helper.http_requests import HTTPRequests
except ModuleNotFoundError:
    logging.info("Module called internally")
    from helper.http_requests import HTTPRequests

class Playlist(object):
    """
    Class for consuming Playlist API from Blip
    """

    def __init__(self, **kwargs):

        # These variables are defined so that
        # codebase can be expanded based on new requirements
        self.customer = None
        self.token = None
        self.__dict__.update(kwargs)

        self.default_payload = {
            "token": self.token
        }
        self.http_requests_instance = HTTPRequests()

        logging.debug(f"Instance variables for Playlist : {self.__dict__}")

    def __del__(self):
        # Removing HTTP request session
        self.http_requests_instance.__del__()

    def get_playlist_request(self, **kwargs):
        """
        This method does a GET call to Blip to get playlist.
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist"
        logging.info(f"Base Playlist API url : {url}")
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when trying to "
                                                                           "access Blip for Playlist : ")

    def get_missing_asset_per_feed_per_playlist(self, playlist_id, **kwargs):
        """
        This method gets all the missing item in playlist from blip
        :param playlist_id: Playlist ID
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/missing"
        logging.info(f"Missing list url invoked to get details : {url}")
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when "
                                                                           "trying to "
                                                                           "access Blip for Missing assets : ")

    def get_asset_status_on_cloud_and_device(self, playlist_id, **kwargs):
        """
        This method get all the assets in a playlist and its details
        :param playlist_id: Playlist ID
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/assets.json"
        logging.info(f"Asset Status url invoked to get details : {url}")
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when trying to "
                                                                           "access Blip for Asset Status on Cloud: ")

    def get_playlist_details(self, playlist_id, **kwargs):
        """
        This method get details about the playlist
        :param playlist_id: Playlist ID
        :param kwargs: Response object from Blip API
        :return:
        """

        if "feed_id" in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}.json"
            logging.info(
                f"Playlist Details url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for Playlist Details: ")
        else:
            logging.error("feed_id is required to use this API")
            return None

    def get_playlists(self, url, params, format):
        params.update(self.default_payload)
        response = self.http_requests_instance.call_get_requests(
            url=url, params=params, error_message="Error occurred when trying to access Blip for Playlist Details: ")
        try:
            if response.status_code == 200:
                data = response.content.decode("utf-8")
                if format == "json":
                    data = json.loads(data)
                return data, format
        except Exception as e:
            logging.error(f"Error while parsing response: {e}")
            return response.text, "osc"

    def playlists_url(self, feed_id, auth_token, playlistdate, published):
        date = datetime.strptime(playlistdate, "%d-%m-%Y").date()
        datestr = "{0:4d}-{1:02d}-{2:02d}".format(
            date.year, date.month, date.day)
        params = {
            'feed_id': feed_id,
            'start_date': datestr,
            'end_date': datestr,
            'ptype': "normal",
            "auth_token": auth_token
        }
        if published:
            params['status'] = "published"
        return f"https://{self.customer}.amagi.tv/v1/api/playlist.json", params

    def playlist_date(self, playlist):
        return playlist["created_at"]
        
    def get_days_playlists(self, feed_id, token, datestr, published):
        url, params = self.playlists_url(feed_id, token, datestr, published)
        playlists, _ = self.get_playlists(url, params, "json")
        if playlists and "playlists" in playlists:
            playlists_sorted = sorted(
                playlists["playlists"], key=self.playlist_date, reverse=True)
            return playlists_sorted

    def get_playlist_csv(self, playlist_id, account_name, channel_code, feed_id = None, uploaded = False):
        csv_url = f"https://{self.customer}.amagi.tv/{account_name}/{channel_code}/playlist/{playlist_id}.csv"
        params = {
            "auth_token": self.token
        }
        if uploaded:
            csv_url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/download"
            params['feed_id'] = feed_id
        text, format = self.get_playlists(csv_url, params, "csv")
        return text, format

    def get_asset_status(self, playlist_id, **kwargs):
        url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/asset_status"
        logging.info(f"Asset Status url invoked to get details : {url}")
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs, 
            error_message="Error occurred when trying to access Blip for Asset Status")

if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format,
                        level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    playlist_instance = Playlist(customer=None, token=None)
