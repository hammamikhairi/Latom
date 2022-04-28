import json
from pprint import pprint

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

from auth import CLIENT_ID, CLIENT_SECRET

url_single = "https://open.spotify.com/track/1cEUi8QulMj1xgrPwwGC2p?si=4dd560aa593c447d"
url_artist = "https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR"
url_album = "https://open.spotify.com/album/3MKvhQoFSrR2PrxXXBHe9B"
url_playlis = "https://open.spotify.com/playlist/0OB5iS2IlsOMXGO9pHxzKq"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))



results = sp.track(url_single, market="US")

# results = sp.artist_albums(,album_type="album", country=None, limit=2, offset=0)
# results  = sp.track("https://open.spotify.com/track/3UmaczJpikHgJFyBTAJVoz?si=f4f8002aff354692")

# print(yaml.dump(results, sort_keys=False, default_flow_style=False))
print(json.dumps(results, sort_keys=False, indent=4))

# def get_playlist_tracks(playlist_id):
  


def fetch_albums_by_atrist(artist_urn):
  results = sp.artist_albums(artist_urn,album_type="album", country=None, limit=1, offset=0)
  albums = results['items']
  for album in albums:
    print(album['name'])
    for key in album:
      print(f"{key}: {album[key]} \n") if key not in ["available_markets", "artists"] else print("3asba \n")
  return albums
