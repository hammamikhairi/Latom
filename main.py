from yaml import dump
from constants import PATH
from services import  get_current_songs, playlist_selecetor, selector, tracks_list_config
from banner import refresh
from youtube import download_playlist_audios, download_single, get_playlist_videos, get_youtube_playlist_name
from os import system

playlist_testing_url1= "https://www.youtube.com/playlist?list=PLGkfMLpx7lj_C6pjva7Y1VaREh4qYJ8Vq"
playlist_testing_url2= "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc"

refresh("enter link : ", endl="")
url = input()
# url = playlist_testing_url

def main() -> None:
  if "youtube" in url:
    if "playlist" in url:


      refresh()
      already_have, new, all = get_playlist_videos(url)
      PLAY_LIST_NAME = get_youtube_playlist_name(url)
      refresh(f'"{PLAY_LIST_NAME}" loaded successfully', endl="\n")
      print(f"{len(all)} tracks fetched.")
      selected = tracks_list_config(already_have, new, all)
      download_playlist_audios(selected)
    else:
      download_single(url)


if __name__=="__main__":
  main()


##get current directory
#   print(os.getcwd())
