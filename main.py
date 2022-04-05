from yaml import dump
from services import playlist_selecetor, selector
from banner import refresh
from youtube import download_playlist_audios, get_playlist_videos, download_youtube_audio
from os import system



refresh("enter link : ", endl="")
url = input()

if "youtube" in url:
  if "playlist" in url:
    refresh("Loading playlist...", endl="")
    videos = get_playlist_videos(url)
    refresh("Playlist loaded successfully", endl="\n")
    multiple = input("want to download all videos? (y/n) : ")
    if multiple == "y":
      download_playlist_audios(videos)
    elif multiple == "n":
      refresh()
      selected = playlist_selecetor(videos)
    else:
      print("Really??")
      system("exit")
    # print(dump(videos, sort_keys=False, default_flow_style=False))



    # print("Playlist downloaded successfully :o")


# else:
#   print(os.getcwd())
