import sys
from os import system
from time import sleep

from sty import fg

banner = fg.li_cyan + """
 _               _
| |       __ _  | |_    ___    _ __ ___
| |      / _` | | __|  / _ \  | '_ ` _ \\
| |___  | (_| | | |_  | (_) | | | | | | |
|_____|  \__,_|  \__|  \___/  |_| |_| |_|

""" + fg.rs
error = fg.da_red + """
  ___   _ __   _ __    ___    _ __
 / _ \ | '__| | '__|  / _ \  | '__|
|  __/ | |    | |    | (_) | | |
 \___| |_|    |_|     \___/  |_|

""" + fg.rs
success = fg.li_green + """
 ____                                             _
/ ___|   _   _    ___    ___    ___   ___   ___  | |
\___ \  | | | |  / __|  / __|  / _ \ / __| / __| | |
 ___) | | |_| | | (__  | (__  |  __/ \__ \ \__ \ |_|
|____/   \__,_|  \___|  \___|  \___| |___/ |___/ (_)

"""+ fg.rs


def refresh(message:str = None, endl:str = "\n") -> None:
  system("clear")
  print(banner)
  print(message, end=endl) if message else None

def rerror(message:str = None) -> None:
  system("clear")
  print(error)
  print(message) if message else None

def resuccess(message:str = None) -> None:
  system("clear")
  print(success)
  print(message) if message else None

class Loader:
  def loading(self) -> None:
    while True:
      blah=["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
      for l in blah:
        sys.stdout.write(l)
        sys.stdout.flush()
        sys.stdout.write('\b')
        sleep(0.05)
  # __loader__ = multiprocessing.Process(target=loading, args=(1,), daemon=True)
