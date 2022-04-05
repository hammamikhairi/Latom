from pytube import YouTube #to install
from youtubesearchpython import  Video, Playlist #information
import yaml #logs
from banner import Loader

youtube_video_url = 'https://www.youtube.com/watch?v=UA7NSpzG98s'



def download_youtube_audio(url: str, filename: str) -> None:
  ld = Loader()
  ld.__loader__.start()
  yt = YouTube(url)
  stream = yt.streams.filter(only_audio=True)
  av = [s for s in stream if "webm" in str(s)]
  av[-1].download(".", filename)
  ld.__loader__.terminate()


def get_youtube_audio_name(url: str) -> str :
  video_data = Video.get(url)
  return video_data["title"]


def get_playlist_videos(url: str) -> list:
  ld = Loader()
  ld.__loader__.start()
  videos = []
  playlist = Playlist(url)
  while playlist.hasMoreVideos:
    playlist.getNextVideos()


  for video in playlist.videos:
    vd = {}
    vd["title"] = video["title"]
    vd["link"] = video["link"]
    videos.append(vd)

  ld.__loader__.terminate()
  return videos

def download_playlist_audios(videos: list) -> None:
  for video in videos:
    print( video["title"])
