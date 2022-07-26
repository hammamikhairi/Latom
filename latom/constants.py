import os
from multiprocessing import cpu_count


ROOT = os.getcwd()
PATH = f"/home/{os.getlogin()}/Music"
ILLEGAL_CHARS = ["?", ">", "<", "|", ":", "/", "\\", "*"]

# you can overclock the download by setting CORES to a high value
CORES = cpu_count()