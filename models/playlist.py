"""
Playlist module
"""

from dataclasses import dataclass
from typing import List

from models.song import Song
from spotify.spotify import SpotifyClient
from utilities.exceptions import UrlError

def check_playlist_url(url) -> dict:
    if "open.spotify.com" not in url or "playlist" not in url:
        raise UrlError(f"Invalid URL: {url}")

    try:
        data_exists = SpotifyClient().get_playlist(url)
    except Exception as e:
        raise UrlError(f"Invalid URL: {url}")

    return data_exists


@dataclass
class Playlist:

    name: str
    owner_id: str
    public: bool
    description: str
    id: str
    url: str
    followers: int
    songs: List[Song]

    @classmethod
    def from_url(cls, url):

        playlist_raw_data = check_playlist_url(url)

        tracks = [Song.from_url(track['track']['external_urls']['spotify'])
                  for track in playlist_raw_data["tracks"]["items"]]

        return cls(
            name=playlist_raw_data["name"],
            owner_id=playlist_raw_data["owner"]["id"],
            public=playlist_raw_data["public"],
            description=playlist_raw_data["description"],
            id=playlist_raw_data["id"],
            url=playlist_raw_data["external_urls"]["spotify"],
            followers=playlist_raw_data["followers"]["total"],
            songs=tracks
        )


    def get_username(self):
        return SpotifyClient().client.user(self.owner_id)["display_name"]




if __name__ == "__main__":
    a = Playlist.from_url(r"https://open.spotify.com/playlist/7dEZMFRFZE5iFUP6Fe7NM4?si=7775ae82d61e4a87")
    print(a)