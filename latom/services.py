from simple_term_menu import TerminalMenu
from banner import refresh
from constants import ILLEGAL_CHARS, PATH
from os import path, system
from time import sleep
from sty import fg

# TODO - use Pyinquirer instead of simple_term_menu
def selector(list_items:list, multiple=False) -> list:
  list_items.append("> Select multiple") if not multiple else None
  list_items.append("> Delete unwanted") if not multiple else None
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
    if list_items[res] == "> Select multiple":
      list_items.pop()
      list_items.pop()
      res = selector(list_items, True)
      return res
    elif list_items[res] == "> Delete unwanted":
      list_items.pop()
      list_items.pop()
      res = selector(list_items, True)
      res = [i for i in range(len(list_items)) if i not in res]
      return res
    else:
      return res
  if not isinstance(res, int) and multiple:
    return res


def playlist_selecetor(videos: list) -> list:
  list_items = []
  for video in videos:
    list_items.append(f"({video['duration']})  {video['title'][:60]}" )

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
    lines.remove(PATH+"\n")
    songs = [line.replace(".webm\n", "") for line in lines if line.count(".webm")]
  return songs


def checker(current_songs:list, videos_to_download:list) -> list:
  """
    splits the list of videos to download into two lists:
    - already acquired
    - new

    Args:
        current_songs (list): _description_
        videos_to_download (list): _description_

    Returns:
        list: of list of dict{title, duration, url}
  """  """"""
  acquired = []
  for video in videos_to_download:
    for song in current_songs:
      if video["title"] in song  or video["title"] == song:
        acquired.append(video)

  new = [video for video in videos_to_download if video not in acquired]

  return [acquired, new, videos_to_download]


def title_formatter(title:str) -> str:
  return "".join([i for i in title if i not in ILLEGAL_CHARS])

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

    try:
      conf = input("\nDownload new tracks only? (y/n): ")
    except:
      refresh("Byee!")
      system(exit(69))
    refresh("Download all ? ", endl="")
    try:
      mult = input()
    except KeyboardInterrupt:
      refresh("Byee!")
      system(exit(69))
    refresh()
    mult = True if mult in ["", "y", "yes"] else False
    if conf in ["y", "", "yes"]:
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
    try:
      mult = input("\nDownload all ? ")
    except KeyboardInterrupt:
      refresh("Byee!")
      system(exit(69))
    mult = True if mult in ["", "y", "yes"] else False
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

