import sys
from os import system
from time import sleep
import multiprocessing

banner = """
 _               _
| |       __ _  | |_    ___    _ __ ___
| |      / _` | | __|  / _ \  | '_ ` _ \\
| |___  | (_| | | |_  | (_) | | | | | | |
|_____|  \__,_|  \__|  \___/  |_| |_| |_|

"""

def displayBanner() -> None:
  system("clear")
  print(banner)

def refresh(message:str = None, endl:str = "\n") -> None:
  system("clear")
  displayBanner()
  print(message, end=endl) if message else None

class Loader:
  def loading(self) -> None:
    while True:
      blah="\|/-\|/-"
      for l in blah:
        sys.stdout.write(l)
        sys.stdout.flush()
        sys.stdout.write('\b')
        sleep(0.2)
  __loader__ = multiprocessing.Process(target=loading, args=(1,), daemon=True)


