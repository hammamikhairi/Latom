# from youtubesearchpython import  Video




# video = Video.get("https://www.youtube.com/watch?v=Tv2q5Oigp_w")

# print(video["title"])












from youtubesearchpython import VideosSearch

videosSearch = VideosSearch('心という名の不可解', limit = 2)

print(videosSearch.result())