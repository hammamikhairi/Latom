import os
import time
from os import system

from yaml import dump

from banner import refresh
from constants import PATH
from services import tracks_list_config
from spotify import (handle_album_download, handle_artist_download,
                     handle_plalist_download, handle_track_download)
from youtube import (download_playlist_audios, download_single,
                     get_channel_videos, get_playlist_videos,
                     handle_search_download)

playlist_testing_url1= "https://www.youtube.com/playlist?list=PLGkfMLpx7lj_C6pjva7Y1VaREh4qYJ8Vq"
playlist_testing_url2= "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc"
channel_testing_url= "https://www.youtube.com/channel/UCbRrwIaXV_lJLzTPtcafh2w/about"



def main() -> None:
  refresh("enter link : ", endl="")
  url = input()


  if "spotify" in url:
    if "playlist" in url:
      refresh()
      handle_plalist_download(url)
    elif "track" in url:
      refresh()
      handle_track_download(url)
    elif "artist" in url:
      refresh()
      handle_artist_download(url)
    elif "album" in url:
      refresh()
      handle_album_download(url)
  elif "youtube" in url:
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
  elif "https://" in url:
    refresh("Not supported yet :/", endl="\n")
  else:
    handle_search_download(url)


if __name__=="__main__":
  main()



##get current directory
#   print(os.getcwd())
