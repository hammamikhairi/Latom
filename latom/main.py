
from banner import refresh
from spotify import (connect, handle_album_download, handle_artist_download,
                     handle_plalist_download, handle_track_download, test_auth)
from youtube import (download_single, handle_search_download,
                     handle_yt_channel_download, handle_yt_playist_download)

playlist_testing_url1= "https://www.youtube.com/playlist?list=PLGkfMLpx7lj_C6pjva7Y1VaREh4qYJ8Vq"
playlist_testing_url2= "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc"
channel_testing_url= "https://www.youtube.com/channel/UCbRrwIaXV_lJLzTPtcafh2w/about"
 

def main() -> None:
  refresh("enter link : ", endl="")
  url = input()
  refresh()

  if "spotify" in url:
    test_auth()
    if "playlist" in url:
      handle_plalist_download(url)
    elif "track" in url:
      handle_track_download(url)
    elif "artist" in url:
      handle_artist_download(url)
    elif "album" in url:
      handle_album_download(url)

  elif "youtube" in url:
    if "playlist" in url:
      handle_yt_playist_download(url)
    elif "/c/" in url or "/channel/" in url:
      handle_yt_channel_download(url)
    else:
      download_single(url)

  elif "https://" in url:
    refresh("Not supported yet :/", endl="\n")

  else:
    handle_search_download(url)


if __name__=="__main__":
  main()
