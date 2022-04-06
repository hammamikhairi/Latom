from pytube import YouTube #to install
from youtubesearchpython import  Video, Playlist #information
from rich.console import Console
from banner import Loader, refresh
import yaml #logs
from time import sleep
from constants import PATH

from services import checker, get_current_songs

youtube_video_url = 'https://www.youtube.com/watch?v=UA7NSpzG98s'


def download_youtube_audio(url: str, filename: str) -> None:
  yt = YouTube(url)
  stream = yt.streams.filter(only_audio=True)
  av = [s for s in stream if "webm" in str(s)]
  av[-1].download(f"{PATH}", filename)


def get_youtube_video_name(url: str) -> str :
  video_data = Video.get(url)
  return video_data["title"]

def get_youtube_playlist_name(url:str) -> str:
  playlist = Playlist.getInfo(url)
  return playlist["title"]


def get_playlist_videos(url: str) -> list:
  console = Console()
  with console.status('[bold cyan]Fetching Playlist... ', speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
    videos = []
    playlist = Playlist(url)
    while playlist.hasMoreVideos:
      playlist.getNextVideos()

    for video in playlist.videos:
      vd = {}
      vd["title"] = video["title"]
      vd["link"] = video["link"]
      videos.append(vd)

    checked = checker(get_current_songs(), videos)

  return checked


def download_single(url:str) -> None:
  console = Console()
  refresh()
  with console.status("[bold cyan]Fetching...", speed=3, spinner="simpleDotsScrolling", spinner_style="cyan") as status:
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


