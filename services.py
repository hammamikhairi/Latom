from simple_term_menu import TerminalMenu




def selector(list_items:list, multiple=False):
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
      res = selector(list_items, True)
      return res
    else:
      return list_items[res]
  if not isinstance(res, int) and multiple:
    return [list_items[i] for i in res]

def playlist_selecetor(videos: dict) -> list:
  list_items = []
  for video in videos:
    list_items.append(video["title"])
  return selector(list_items)

