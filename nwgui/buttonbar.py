
import pygame

from nwgui.widget import Widget
from nwgui.container import HorizontalContainer
from nwgui.button import SpriteButton

from nwgui.util.ordereddict import OrderedDict

class ButtonBar(Widget):
    """
    A horizontal bar which contains one or more banks of buttons.

    A bank is a visible set of buttons that are associated with a single key. 
    Switching between banks causes the current set of displayed buttons to
    be hidden and the new bank of buttons to be shown instead.

    Internally, ButtonBar subclasses Widget, but composes over zero or more
    HorizontalContainer objects. Each container is used to hold a bank of
    buttons, and are hidden or shown as needed.

    >>> buttonbar = ButtonBar(width=100, height=36, root=gui)
    >>> buttonbar.addBank("main")
    >>> buttonbar.addButton("spriteName1")
    >>> buttonbar.addButton("spriteName2", callback=None, bank="main")
    >>> callback = lambda spriteName: None
    >>> buttonbar.addBank("second", {"spriteName3": callback})
    >>> buttonbar.addButton("spriteName6", callback=callback, bank="main")
    >>> buttonbar.switchBank("main")
    >>> buttonbar.addButton("spriteName4", callback=None)
    >>> buttonbar.addButton("spriteName5", callback=callback, bank="second")
    >>> buttonbar.getBanks()
    ["main", "second"]
    >>> buttonbar.getCurrentBank()
    "main"
    >>> buttonbar.getButtons(bank="main")
    {"spriteName1": None, "spriteName2": None, "spriteName4": None, "spriteName6": <function <lambda> at 0x...>}
    >>> buttonbar.switchBank("second")
    >>> buttonbar.getButtons()
    {"spriteName3": <function <lambda> at 0x...>, "spriteName5": <function <lambda> at 0x...>}
    >>> buttonbar.activate(1)
    None
    >>> buttonbar.activate(2)
    IndexError: list index out of range
    """
    def __init__(self, *args, **kwargs):
        super(ButtonBar, self).__init__(*args, **kwargs)
        self._banks = {}
        self._currentBank = None
        self._bankContainers = {}
        self.image = pygame.Surface((1, 1))
    
    def addBank(self, name):
        self._banks[name] = OrderedDict()

        if self._currentBank is not None:
            self._bankContainers[self._currentBank].hide()

        self._bankContainers[name] = HorizontalContainer(self.rect.width, self.rect.height, root=self.root)
        self._bankContainers[name].setParent(self)
        self._bankContainers[name].setPosition(self.rect.topleft)
        self._currentBank = name

    def switchBank(self, name):
        if not self._banks.has_key(name):
            raise KeyError("No such bank: %s" % (name,))

        self._bankContainers[name].hide()
        self._currentBank = name
        self._bankContainers[name].show()
        self._bankContainers[name].setPosition(self.rect.topleft)

    def clearBank(self, name):
        self._bankContainers[name].removeAll()
        self._banks[name] = {}

    def getBanks(self):
        return self._banks.keys()

    def addButton(self, spriteName, callback=None, bank=None):
        if bank is None:
            bank = self._currentBank

        self._banks[bank][spriteName] = callback
        buttonIndex = len(self._banks[bank]) - 1

        def internalCallback():
            self.activate(buttonIndex)

        self._bankContainers[bank].add(SpriteButton(spriteName, internalCallback, root=self.root))

    def getButtons(self, bank=None):
        if bank is None:
            bank = self._currentBank

        return self._banks[bank]

    def activate(self, buttonIndex):
        name, func = self._banks[self._currentBank].items()[buttonIndex]
        if func is not None:
            return func(name)

    def setPosition(self, position):
        super(ButtonBar, self).setPosition(position)
        for container in self._bankContainers.values():
            container.setPosition(position)

    def handleEvent(self, event):
        if self._currentBank is not None:
            self._bankContainers[self._currentBank].handleEvent(event)
