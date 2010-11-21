
from pygame.locals import MOUSEBUTTONDOWN

from nwgui.label import Label


class Tab(Label):
    def __init__(self, tabbedPages, tabName, *args, **kwargs):
        Label.__init__(self, tabName, *args, **kwargs)
        self.tabName = tabName
        self._tabbedPages = tabbedPages

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self._tabbedPages.showPage(self.tabName)
            self._tabbedPages.setActive()
