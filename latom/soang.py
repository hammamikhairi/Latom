from dataclasses import dataclass, field

from constants import ILLEGAL_CHARS


@dataclass
class Soang:
  title:str 
  duration:str = field(default=None)
  link:str = field(default=None)
  artist:str = field(default=None)
  cover:str = None
  def __post_init__(self):
    # legal_title = "".join([i for i in self.title if i not in ILLEGAL_CHARS])
    # self.title = legal_title.replace(" ", "_")
    self.title = "".join([i for i in self.title if i not in ILLEGAL_CHARS])
    self.cover = self.cover.split("?")[0] if self.cover else None
  def __str__(self):
    return f"{self.title} - {self.duration}"
  #ADD A REPR METHOD
  def __repr__(self):
    return f"{self.title} - {self.duration}"
