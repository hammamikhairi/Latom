from fileinput import filename
from pytube import YouTube

youtube_video_url = 'https://www.youtube.com/watch?v=UA7NSpzG98s'

try:
    yt = YouTube(youtube_video_url)


    stream =yt.streams.filter(only_audio=True).all()
    # print(stream)
    av = [s for s in stream if "webm" in str(s)]
    # print(av)
    av[-1].download('../../Music', filename='god.webm')

    # av[-1].streams.get_audio_only().download(output_path='.', filename='audio')
    # print('YouTube video audio downloaded successfully')
except Exception as e:
    print(e)