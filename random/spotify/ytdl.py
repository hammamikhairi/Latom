# from __future__ import unicode_literals
# import youtube_dl


# ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
# }


# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(['https://www.youtube.com/watch?v=UA7NSpzG98s', "test.webm"])



from pytube import YouTube
import os

yt = YouTube('https://www.youtube.com/watch?v=UA7NSpzG98s')

video = yt.streams.filter(only_audio=True).first()

video.download(output_path=".", "test.webm")
