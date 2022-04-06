from simple_term_menu import TerminalMenu
from banner import refresh
from constants import PATH
from os import path, system
from time import sleep
from sty import fg

def selector(list_items:list, multiple=False) -> list:
  list_items.append("Select multiple") if not multiple else None
  terminal_menu = TerminalMenu(
                      list_items,
                      title="Choose Bitch",
                      menu_cursor_style=("fg_purple", "bold"),
                      search_highlight_style=("fg_black", "bg_cyan", "bold"),
                      show_multi_select_hint= multiple,
                      multi_select=multiple
                    )
  res = terminal_menu.show()
  if isinstance(res, int):
    if list_items[res] == "Select multiple":
      list_items.pop()
      res = selector(list_items, True)
      return res
    else:
      return res
  if not isinstance(res, int) and multiple:
    return res

def playlist_selecetor(videos: list) -> list:
  list_items = []
  for video in videos:
    list_items.append(video["title"])

  res = selector(list_items)
  if isinstance(res, int):
    selected = [videos[res]]
  else:
    selected =  [videos[i] for i in res]
  return selected


def get_current_songs() -> list:
  system(f"tree -i {PATH} > .songs")
  with open("./.songs", "r") as f:
    lines = f.readlines()
    songs = [line.split(".")[0] for line in lines if line.count(".")>0]
  return songs


def checker(current_songs:list, videos_to_download:list) -> list:
  acquired = []
  for video in videos_to_download:
    for song in current_songs:
      if video["title"] in song  or video["title"] == song:
        acquired.append(video)

  new = [video for video in videos_to_download if video not in acquired]

  return [acquired, new, videos_to_download]


def tracks_list_config(acquired, new, all) -> list:
  mult = True
  selected= []
  if len(acquired):
    #! paatttthhhhhhhhhh
    print(f"\nyou already have Deez tracks in : {fg.da_magenta +'~'+ PATH.split('..')[-1] + fg.rs}: ")
    for song in acquired:
      print("\t"+song["title"])

    print("\nNew tracks : ")
    for song in new:
      print("\t"+song["title"]+ " "+fg.li_cyan+ song["duration"]+ fg.rs)

    conf = input("\nDownload new tracks only? (y/n): ")
    refresh("Download all ? ", endl="")
    mult = input()
    refresh()
    mult = True if mult in ["", "y"] else False
    if conf in ["y", ""]:
      if not mult:
        selected = playlist_selecetor(new)
      else:
        selected = new
    else:
      if not mult:
        selected = playlist_selecetor(all)
      else:
        selected = all

  else:
    print("\nTracks : ")
    for song in new:
      print("\t"+song["title"]+ " "+fg.li_cyan+ song["duration"]+ fg.rs)
    mult = input("\nDownload all ? ")
    mult = True if mult in ["", "y"] else False
    refresh()
    if not mult:
      selected = playlist_selecetor(all)
    else:
      selected = all
  return selected


def setup_download_path() -> None:
  path = path.relpath('/home/khairi/Music')
  with open('./constants.py') as f:
    lines = f.readlines()
    print(lines)

