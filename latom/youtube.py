import json
import os
from os import system
from pprint import pprint  # logs
from time import sleep

import pafy
import yaml  # logs
from rich.console import Console
from youtubesearchpython import (Channel, ChannelsSearch, Playlist, Video,
                                 VideosSearch, playlist_from_channel_id)

from banner import refresh, rerror
from constants import PATH
from services import checker, get_current_songs
from soang import Soang

youtube_video_url = 'https://www.youtube.com/watch?v=UA7NSpzG98s'
# pprint.pprint()


def download_youtube_audio(url: str, filename: str) -> None:
  """
    Downloads the audio (format : webm) from youtube video in PATH directory

    Args:
        url (str): youtube url
        filename (str): filename should be with extension
  """
  # yt = YouTube(url)
  # streams = yt.streams.filter(only_audio=True)
  # av = [s for s in streams if "webm" in str(s)]
  # av[-1].download(f"{PATH}", filename)
  yt = pafy.new(url)
  audiostreams = yt.audiostreams
  streams = [i for i in audiostreams if i.extension == "m4a"]
  #ANCHOR - dont forget this dirty hack
  os.chdir("../Music")
  streams[-1].download(filename + ".m4a",quiet=True)

download_youtube_audio("https://www.youtube.com/watch?v=UA7NSpzG98s", "test")

def get_youtube_video_name(url: str) -> str :
  video_data = Video.get(url)
  return video_data["title"]

def get_youtube_playlist_name(url:str) -> str:
  playlist = Playlist.getInfo(url)
  return playlist["title"]

def get_channel_id_name(url: str) -> str:
  """
  Get channel id and name from youtube url 
  (from id in url)

  Args:
      url (str): youtube url

  Returns:
      str: 2 seperate strings (id, name)
  """
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
    except Exception:
      rerror("Check your channel link")
      system(exit(69))

  return channel_id, channel_name

def fetcher(playlist: Playlist) -> list:
  while playlist.hasMoreVideos:
    playlist.getNextVideos()
    
  videos = []
  for video in playlist.videos:
    videos.append(Soang(video["title"], video["duration"], video["link"]))
  checked = checker(get_current_songs(), videos)
  return checked

def get_playlist_videos(url: str) -> list:
  """
    get playlist videos from youtube url

    Args:
        url (str): youtube playlist url "~/plalist/:id"

    Returns:
        list: of list[new, acquired, all, name] each is a list of dict{title, duration, link}
  """
  console = Console()
  with console.status('[bold cyan]Fetching Playlist ', speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    try:
      playlist = Playlist(url)
    except Exception as e:
      if "Name" in str(e):
        rerror("Check your internet bro")
      else:
        rerror("Check your playlist link")
      system(exit(69))
    sleep(5)
    checked = fetcher(playlist)
    name = get_youtube_playlist_name(url)

    checked.append(name)
    return checked



def get_channel_videos(url: str) -> list:
  """
    practicallly same as get_playlist_videos
  """
  console = Console()
  with console.status("[bold cyan]Fetching channel", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    channel_id, channel_name = get_channel_id_name(url)
    playlist = Playlist(playlist_from_channel_id(channel_id))
    checked = fetcher(playlist)
    checked.append(channel_name)
  return checked

def download_single(url:str) -> None:
  """
  Implements the interface for download_youtube_audio
  """
  console = Console()
  refresh()
  with console.status("[bold cyan]Fetching", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    name = get_youtube_video_name(url)
  refresh()
  with console.status(f"[bold cyan]Downloading : {name}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    download_youtube_audio(url, name+".webm")
  #TODO: add progress bar and make the fucking interface prettier
  print(name)

def download_playlist_audios(videos: list) -> None:
  """
  Da loop

  Args:
      videos : list of dict
  """
  console = Console()
  for video in videos:
    with console.status(f"[bold cyan]Downloading : {video.title}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
      download_youtube_audio(video.link, f'{video.title}.webm')
      print(video.title)


##! search

# results = VideosSearch('Rap God - lyrics', limit = 5).result()["result"]
# res = []
# for result in results:
#   res.append(Soang(result["title"], result["duration"], result["link"]))
#   pass



# print(json.dumps(results, sort_keys=False, indent=4))
