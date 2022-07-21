
import os
from multiprocessing import Process
from os import system
from time import sleep

import pafy
from rich.console import Console
from youtubesearchpython import (Channel, ChannelsSearch, Playlist, Video,
                                 VideosSearch, playlist_from_channel_id)

from banner import refresh, rerror
from constants import PATH
from services import (checker, decrement_index, get_current_songs,
                      increment_index, read_file, tracks_list_config)
from soang import Soang


def download_youtube_audio(url: str, filename: str) -> None:
  """
    Downloads the audio (format : m4a) from youtube video in PATH directory

    Args:
        url (str): youtube url
        filename (str): filename should be with extension
  """
  yt = pafy.new(url)
  audiostreams = yt.audiostreams
  streams = [i for i in audiostreams if i.extension == "m4a"]
  #ANCHOR - dont forget this dirty hack
  #!SECTION - ADD A CALLBACK FOR DOWNLOADING
  os.chdir(os.path.relpath(PATH))
  # print(streams[-1].get_filesize())
  name = filename + ".m4a"
  streams[-1].download(name,quiet=True)

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
    videos.append(Soang(video["title"], video["duration"], video["link"], video["thumbnails"][0]["url"]))
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
        rerror("Check your internet connection!")
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
  with console.status("[bold cyan]Fetching...", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    name = get_youtube_video_name(url)
  refresh()
  with console.status(f"[bold cyan]Downloading : {name}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    download_youtube_audio(url, name)
  #TODO: add progress bar and make the fucking interface prettier
  print(name)

def download_playlist_audios(videos: list) -> None:
  """
  Da loop

  Args:
      videos : list of Soang objects
  """
  console = Console()
  for video in videos:
    with console.status(f"[bold cyan]Downloading... : {video.title}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
      try :
        download_youtube_audio(video.link, video.title)
      except Exception as e:
        download_youtube_audio(video.link, video.title)
      finally:
        print("error occured with : " + video.title)
      # write_metadata(video.title + "m4a", video.cover)
      print(video)


def Asynchronous_Download(selected: list) -> None:

  def download(data: tuple):
    try:
      try:
        download_youtube_audio(data[0], data[1])
      except:
        download_youtube_audio(data[0], data[1])
    except :
      print(f"Error downloading {data[1]}!!!")
    increment_index()

  while len(selected):
    try :
      index = int(float(read_file()))
    except:
      index = 0

    if index == 0:
      continue
    else:
      decrement_index()
      video = selected.pop()
      print(video.title)
      process = Process(target=download, args=((video.link, video.title),))
      process.start()

##! search
def handle_search_download(query: str) -> Soang:
  console = Console()
  # with console.status(f"[bold cyan]Fetching : {query}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan"):
  results = VideosSearch(query + 'lyrics', limit = 3).result()["result"]
  res = []
  for result in results:
    song = Soang(result["title"], result["duration"])
    song.link = result["link"]
    res.append(song)

  if len(res):
    shortest = [res[0]]
  else:
    rerror("No results found")
    system(exit(69))
  shortest = [i for i in res if i.duration <= shortest[0].duration]
  video = shortest[-1]


  # with console.status(f"[bold cyan]Downloading : {video.title}", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan"):
  download_youtube_audio(video.link, video.title)

def handle_yt_playist_download(url:str) -> None:
  already_have, new, all, PLAY_LIST_NAME = get_playlist_videos(url)
  refresh(f'Playlist : "{PLAY_LIST_NAME}"', endl="\n")
  print(f"{len(all)} tracks fetched.")
  selected = tracks_list_config(already_have, new, all)
  refresh()
  # download_playlist_audios(selected)
  Asynchronous_Download(selected)


def handle_yt_channel_download(url:str) -> None:
  already_have, new, all, channel_name = get_channel_videos(url)
  refresh(f'Channel : "{channel_name}"', endl="\n")
  print(f"{len(all)} tracks fetched.")
  selected = tracks_list_config(already_have, new, all)
  refresh()
  # download_playlist_audios(selected)
  Asynchronous_Download(selected)
