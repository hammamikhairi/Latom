from pick import pick
from pick import Picker


title, options = 'Title', ['Option1', 'Option2', 'three', 'piss']
picker = Picker(options, title, multiselect=True)
def go_back(picker):
   return None, -1
picker.register_custom_handler(ord('h'),  go_back)
option, index = picker.start()

print(index)