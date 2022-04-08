from os import system
from pytube import YouTube #to install
from youtubesearchpython import  Video, Playlist, ChannelsSearch, playlist_from_channel_id, Search, Channel
from rich.console import Console
from banner import Loader, refresh, rerror
import yaml #logs
from time import sleep
from constants import PATH

from services import checker, get_current_songs

youtube_video_url = 'https://www.youtube.com/watch?v=UA7NSpzG98s'


def download_youtube_audio(url: str, filename: str) -> None:
  yt = YouTube(url)
  streams = yt.streams.filter(only_audio=True)
  av = [s for s in streams if "webm" in str(s)]
  av[-1].download(f"{PATH}", filename)


def get_youtube_video_name(url: str) -> str :
  video_data = Video.get(url)
  return video_data["title"]

def get_youtube_playlist_name(url:str) -> str:
  playlist = Playlist.getInfo(url)
  return playlist["title"]

def get_channel_id_name(url: str) -> str:
  if url.split("/")[-1] in ["videos", "featured", "playlists", "channels", "about"]:
    url = "/".join([slice for slice in url.split("/")[:-1]])
  if "/c/" in url:
    channels = ChannelsSearch(url.split("/")[-1], limit = 1, region = 'US')
    channel_name = channels.result()['result'][0]['title']
    channel_id = channels.result()['result'][0]['id']
  else:
    channel_id = url.split("/")[-1]
    try:
      channel_name = Channel.get(url.split("/")[-1])['title']
    except Exception as e:
      rerror("Check your channel link")
      system(exit(69))

  return channel_id, channel_name

def get_playlist_videos(url: str) -> list:
  console = Console()
  with console.status('[bold cyan]Fetching Playlist ', speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    videos = []
    try:
      playlist = Playlist(url)
    except Exception as e:
      if "Name" in str(e):
        rerror("Check your internet bro")
      else:
        rerror("Check your playlist link")
      system(exit(69))

    while playlist.hasMoreVideos:
      playlist.getNextVideos()

    for video in playlist.videos:
      vd = {}
      vd["title"] = video["title"]
      vd["link"] = video["link"]
      vd["duration"] = video["duration"]
      videos.append(vd)

    checked = checker(get_current_songs(), videos)
    name = get_youtube_playlist_name(url)

    checked.append(name)
  return checked


# def sorter(playlist: list) -> list:
#   return sorted(videos, key=lambda k: k['duration'])


def get_channel_videos(url: str) -> list:
  console = Console()
  with console.status("[bold cyan]Fetching channel", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:

    channel_id, channel_name = get_channel_id_name(url)
    playlist = Playlist(playlist_from_channel_id(channel_id))


    while playlist.hasMoreVideos:
        playlist.getNextVideos()

    videos = []
    for video in playlist.videos:
      vd = {}
      vd["title"] = video["title"]
      vd["link"] = video["link"]
      vd["duration"] = video["duration"]
      videos.append(vd)

    checked = checker(get_current_songs(), videos)

    checked.append(channel_name)
  return checked

def download_single(url:str) -> None:
  console = Console()
  refresh()
  with console.status("[bold cyan]Fetching", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    name = get_youtube_video_name(url)
  refresh()
  with console.status(f"[bold cyan]Downloading : {name}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    download_youtube_audio(url, name+".webm")
  print(name)

def download_playlist_audios(videos: list) -> None:
  console = Console()
  for video in videos:
    with console.status(f"[bold cyan]Downloading : {video['title']}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
      download_youtube_audio(video["link"], f'{video["title"]}.webm')
      print(video['title'])


