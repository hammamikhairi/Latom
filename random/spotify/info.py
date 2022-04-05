import eyed3
from eyed3 import id3
import urllib.request

audiofile = eyed3.load("Godzilla.webm")
# audiofile.tag.artist = "test"
# audiofile.tag.album = "Free For All Comp LP"
# audiofile.tag.album_artist = "Various Artists"
# audiofile.tag.title = "The Edge"
# audiofile.tag.track_num = 3

# audiofile = {}
# tag = id3.Tag()
# tag.parse("Godzilla.webm")

# tag.name = "deez"
# tag.save("Godzilla.webm")

# audiofile.tag.name = "godzilla"
# audiofile.tag.save()
print(audiofile.tag.name)



# response = urllib.request.urlopen("https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69")
# imagedata = response.read()
# print(imagedata)
# audiofile.tag.images.set(3, imagedata , "image/jpeg" ,u"Description")
# audiofile.tag.images.set(type_=3, img_data=None, mime_type=None, description=u"you can put a description here", img_url=u"https://upload.wikimedia.org/wikipedia/en/6/60/Recovery_Album_Cover.jpg")
# audiofile.tag.save()

# print(audiofile.tag)
# for key in audiofile.tag:
#   pprint.pprint(var(key))