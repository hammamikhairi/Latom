import os
import time
from yaml import dump
from constants import PATH
from services import tracks_list_config
from banner import refresh

from youtube import (download_playlist_audios, download_single,
                     get_channel_videos, get_playlist_videos)
from os import system

playlist_testing_url1= "https://www.youtube.com/playlist?list=PLGkfMLpx7lj_C6pjva7Y1VaREh4qYJ8Vq"
playlist_testing_url2= "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc"
channel_testing_url= "https://www.youtube.com/channel/UCbRrwIaXV_lJLzTPtcafh2w/about"



def main() -> None:
  refresh("enter link : ", endl="")
  url = input()
  # url = playlist_testing_url


  if "spotify" in url:
    refresh("spotify link not supported yet")
  if "youtube" in url:
    if "playlist" in url:
      refresh()
      already_have, new, all, PLAY_LIST_NAME = get_playlist_videos(url)
      refresh(f'Playlist : "{PLAY_LIST_NAME}"', endl="\n")
      print(f"{len(all)} tracks fetched.")
      selected = tracks_list_config(already_have, new, all)
      refresh()
      print(selected)
      download_playlist_audios(selected)

    elif "/c/" in url or "/channel/" in url:
      refresh()
      already_have, new, all, channel_name = get_channel_videos(url)
      refresh(f'Channel : "{channel_name}"', endl="\n")
      print(f"{len(all)} tracks fetched.")
      selected = tracks_list_config(already_have, new, all)
      refresh()
      print(selected)
      download_playlist_audios(selected)

    else:
      print("single ??")
      download_single(url)


if __name__=="__main__":
  main()





##get current directory
#   print(os.getcwd())
