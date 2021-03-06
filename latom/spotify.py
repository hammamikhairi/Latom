
import time
from multiprocessing import Process, Value

import spotipy
from rich.console import Console
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from auth import CLIENT_ID, CLIENT_SECRET
from banner import refresh, rerror, resuccess
from services import (checker, get_current_songs, set_spotify_auth, tracks_list_config)
from soang import Soang
from youtube import handle_search_download
from constants import CORES
url_single = "https://open.spotify.com/track/1cEUi8QulMj1xgrPwwGC2p?si=4dd560aa593c447d"
url_artist = "https://open.spotify.com/artist/3MZsBdqDrRTJihTHQrO6Dq"
url_album = "https://open.spotify.com/album/3MKvhQoFSrR2PrxXXBHe9B"
url_playlis = "https://open.spotify.com/playlist/0ctbo3FtW49qComqmzKMuK"

sp = None

def connect():
  rerror("Must provide Client ID and Client Secret \n You can get them from https://developer.spotify.com/dashboard/ .")
  id, secret = set_spotify_auth()
  try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=id, client_secret=secret))
    sp.search(q='artist:' + " Joji", type='artist')
    resuccess("Successfully connected to Spotify!")
    time.sleep(2)
  except:
    rerror("Invalid Client ID or Client Secret")

def test_auth() -> bool:
  try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    res = sp.search(q='artist:' + " Joji", type='artist')
  except:
    connect()

if CLIENT_ID != "LAT" and CLIENT_SECRET != "LAT":
  try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
  except SpotifyException:
    print("Can't connect to Spotify")


def fetch_playlist_data(url: str) -> dict:
  """
  Fetches the data of a playlist

  returns a dict
  """
  if "/" in url:
    playlist_id = url.split("/")[-1]
  else:
    playlist_id = url.split(":")[-1]
  try:
    query = sp.playlist_tracks(playlist_id)
    query["title"] = sp.playlist(playlist_id)["name"]
  except SpotifyException:
    rerror("Invalid playlist url")
  return query


def get_playlist_tracks(tracks: list) -> list:
  songs = []
  for track in tracks:
    song = Soang(track["track"]["name"])
    song.artist = track["track"]["artists"][0]["name"]
    ms = track["track"]["duration_ms"]
    song.duration = f"{int(ms/60000)}:{int(ms%60000/1000):02d}"
    songs.append(song)
    print(song)
  return songs


def Asynchronous_Download(selected: list) -> None:

  def download(data: str, threads):
    try:
      try:
        handle_search_download(data)
      except :
        handle_search_download(data)
    except :
      print(f"Error downloading {data}!!!")
    finally:
      with threads.get_lock():
        threads.value += 1

  threads = Value('d', CORES)
  while len(selected):
    if threads.value:
      threads.value -= 1
      song = selected.pop()
      print(song)
      process = Process(target=download, args=(song.title + " - " + song.artist, threads))
      process.start()


def handle_plalist_download(url: str):
  data = fetch_playlist_data(url)
  songs = get_playlist_tracks(data["items"])
  acquired, new, videos_to_download  = checker(get_current_songs(), songs)
  refresh(f'Playlist : "{data["title"]}"', endl="\n")
  selected = tracks_list_config(acquired, new, videos_to_download)
  refresh()
  
  Asynchronous_Download(selected)

def fetch_track_data(url: str) -> Soang:
  try:
    query = sp.track(url)
    song = Soang(query["name"])
    song.artist = query["artists"][0]["name"]
    ms = query["duration_ms"]
    song.duration = f"{int(ms/60000)}:{int(ms%60000/1000):02d}"
    return song
  except SpotifyException :
    rerror("Invalid track url")


def handle_track_download(url: str):
  song = fetch_track_data(url)
  handle_search_download(song.title + " - " + song.artist)


def fetch_album_data(url):
  try:
    query = sp.album(url)
  except SpotifyException:
    rerror("Invalid album url")
  return query

def get_album_tracks(tracks: list) -> list:
  songs = []
  for track in tracks:
    song = Soang(track["name"])
    song.artist = track["artists"][0]["name"]
    ms = track["duration_ms"]
    song.duration = f"{int(ms/60000)}:{int(ms%60000/1000):02d}"
    songs.append(song)
  return songs


def handle_album_download(url: str):
  data = fetch_album_data(url)
  songs = get_album_tracks(data["tracks"]["items"])
  acquired, new, videos_to_download  = checker(get_current_songs(), songs)
  refresh(f'Album : "{data["name"]}"', endl="\n")
  selected = tracks_list_config(acquired, new, videos_to_download)
  refresh()

  Asynchronous_Download(selected)



def fetch_albums_by_atrist(url):
  results = sp.artist_albums(url, album_type='album')
  albums = results['items']
  while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

  res = []
  for album in albums:
    res.append(album["external_urls"]["spotify"])
  return res

def get_all_artist_songs(albums: list) -> list:
  tracks = []
  for album in albums:
    data = fetch_album_data(album)
    songs = get_album_tracks(data["tracks"]["items"])
    tracks.extend(songs)

  return tracks

def handle_artist_download(url: str):
  refresh()
  name = sp.artist(url)["name"]
  console = Console()
  with console.status(f"[bold cyan]Fetching {name}'s tracks", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan"):
    artist_urn = url.split("/")[-1]
    albums = fetch_albums_by_atrist(artist_urn)
    tracks = get_all_artist_songs(albums)
    acquired, new, videos_to_download  = checker(get_current_songs(), tracks)
  refresh(f'Artist : "{name}"', endl="\n")
  selected = tracks_list_config(acquired, new, videos_to_download)
  refresh()

  Asynchronous_Download(selected)


# results = sp.artist_albums(,album_type="album", country=None, limit=2, offset=0)
# results  = sp.track("https://open.spotify.com/track/3UmaczJpikHgJFyBTAJVoz?si=f4f8002aff354692")

# print(yaml.dump(results, sort_keys=False, default_flow_style=False))
# print(json.dumps(results, sort_keys=False, indent=4))

# def get_playlist_tracks(playlist_id):

