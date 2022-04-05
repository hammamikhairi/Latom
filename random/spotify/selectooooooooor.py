from simple_term_menu import TerminalMenu

def main():
  options = ["[a] apple", "[b] banana", "[o] orange"]
  terminal_menu = TerminalMenu(options,title="batata", menu_cursor_style=("fg_purple", "bold"), search_highlight_style=("fg_black", "bg_cyan", "bold") )
  menu_entry_index = terminal_menu.show()
  print(menu_entry_index)

if __name__ == "__main__":
    main()