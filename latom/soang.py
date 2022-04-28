from dataclasses import dataclass

from attr import field

from constants import ILLEGAL_CHARS


@dataclass
class FromSpotify:
  album:str
  artist:str
  date:str
  desc:str
  genre:str
  tracknumber:int
  discnumber:int
  comment = "Downloaded with Latom"

@dataclass
class Soang:
  title:str
  duration:str
  link:str
  cover:str = None
  Spotify:FromSpotify = None
  def __post_init__(self):
    # legal_title = "".join([i for i in self.title if i not in ILLEGAL_CHARS])
    # self.title = legal_title.replace(" ", "_")
    self.title = "".join([i for i in self.title if i not in ILLEGAL_CHARS])
    self.cover = self.cover.split("?")[0] if self.cover else None

  def __str__(self):
    return f"{self.title} - {self.duration}"
