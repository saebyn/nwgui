
import os, os.path

from nwgui.list import List
from nwgui.label import Label

class FileBrowser(List):
    def __init__(self, path, *args, **kwargs):
        List.__init__(self, *args, **kwargs)

        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                self.add(filename, Label(filename, root=self.root))
