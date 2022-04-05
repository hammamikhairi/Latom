from pytube import YouTube
import os

os.system("clear")
url = input("enter the link of the video: ")
# url = "https://www.youtube.com/watch?v=MtYOrIwW1FQ"
path = input("enter the path where you want to save the video: ")



try:
    yt_obj = YouTube(url)
    print(yt_obj.thumbnail_url)
    yt_obj.streams.get_audio_only().download(output_path='~/Music', filename='test.mp3')
    print('YouTube video audio downloaded successfully')
except Exception as e:
    print(e)

input("Press Enter to exit")
os.system("clear")