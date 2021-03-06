# Introduction

Latom, is an asynchronous song downloader that accepts Youtube and spotify links. The app currently supports downloading :
- Singles 
- Playlists
- Albums
- Youtube Channels (entirely)
- Artist's entire Portfolio.

This seemed like the perfect pet project to make and consequently learn from :)



# Features

- Installs Tracks Asynchronously ( can choose how many at a time in `latom/.index.txt` )
- checks for existing songs in the `~/Music` directory 
- can select which songs to download from a playlist/channel.
- can remove unwanted songs from a playlist
- can perform youtube search ( simply enter the query instead of the url )


# Packages

- [Pafy](https://pypi.org/project/pafy/)
- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/)
- [youtubesearchpython](https://pypi.org/project/youtube-search-python/)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [simple_term_menu](https://pypi.org/project/simple-term-menu/)
- [rich](https://rich.readthedocs.io/en/stable/introduction.html)
- [sty](https://pypi.org/project/sty/)

# Support
The following audio format is supported:
- m4a

All Youtube link types are supported (channels, shorts...) <br />
All Spotify link types are supported aswell (Artists, Albums, plalists ...)



# Setup
### to install the requirements
```bash
pip install -r ./latom/requirements.txt
```
### to run the code
```bash
python ./latom/main.py
```



# Note:

### Pafy needs some adjustments :
The dislike button on youtube has been made private, so some modification on backend_youtube_dl.py is required to run pafy.

1) Navigate to :
 - C:\Users\harsh\AppData\Local\Programs\Python\Python3.8\lib\site- packages\pafy
 - /home/user/.local/lib/python3.8/site-packages/pafy

2) Open backend_youtube_dl.py file

3) Comment or remove this code (line 54): self._dislikes = self._ydl_info['dislike_count']
