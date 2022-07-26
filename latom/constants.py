import os

ROOT = os.getcwd()
PATH = f"/home/{os.getlogin()}/Music"
ILLEGAL_CHARS = ["?", ">", "<", "|", ":", "/", "\\", "*"]

# you can overclock the download by setting CORES to a high value
CORES = os.cpu_count()
