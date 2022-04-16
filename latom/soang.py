from dataclasses import dataclass
from constants import ILLEGAL_CHARS


@dataclass
class Soang:
  def __init__(self, title:str, duration:str, link:str) -> None:
      self.title = "".join([i for i in title if i not in ILLEGAL_CHARS])
      self.duration = duration
      self.link = link
  title:str
  duration:str
  link:str
  def __str__(self):
    return f"{self.title} - {self.duration}"