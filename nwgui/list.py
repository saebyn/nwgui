
import pygame
from pygame.locals import *

from nwgui.container import VerticalContainer

class List(VerticalContainer):
    def __init__(self, *args, **kwargs):
        kwargs['padding'] = (5, 5)
        kwargs['border'] = (1, (0, 0, 0))
        VerticalContainer.__init__(self, *args, **kwargs)
        self.items = {}
        self.itemOrder = []
        # This is the index (in itemOrder) of the item at the top of the
        # displayed list of items. It is None if there are no items.
        self.listItemViewedIndex = None
        self.selectedItem = None
        self._dirty = True
        self.callback = None

        # TODO add up/down buttons
        # TODO draw scroll location indicator

    def add(self, name, widget):
        VerticalContainer.add(self, widget)
        # TODO replace this with a ordered dict
        if self.items.has_key(name):
            raise KeyError("Item already added.")
        self.items[name] = widget
        self.itemOrder.append(name)
        if self.listItemViewedIndex is None:
            self.listItemViewedIndex = 0

    def clear(self):
        """
        Remove all items from the list.
        """
        for item in self.items.keys():
            self.remove(item)

    def remove(self, name):
        widget = self.items[name]

        VerticalContainer.remove(self, widget)
        del self.items[name]
        self.itemOrder.remove(name)

        if self.listItemViewedIndex >= len(self.itemOrder):
            self.listItemViewedIndex = len(self.itemOrder) - 1

        if self.listItemViewedIndex == -1:
            self.listItemViewedIndex = None

    def getSelected(self):
        return self.selectedItem

    def hasSelected(self):
        return self.selectedItem is not None

    def select(self, itemName):
        if self.selectedItem is not None:
            self.unselect(self.selectedItem)

        self.selectedItem = itemName
        self.items[itemName].setColor((255, 255, 255))
        self.items[itemName].setBackground((0, 0, 100))

        if self.callback is not None:
            self.callback(itemName)

    def setSelectCallback(self, callback):
        self.callback = callback

    def clearSelectCallback(self):
        self.callback = None

    def unselect(self, itemName=None):
        self.selectedItem = None

        def removeFormatting(name):
            self.items[name].setBackground((255, 255, 255))
            self.items[name].setColor((0, 0, 0))

        if itemName is None:
            for name in self.itemOrder:
                removeFormatting(name)
        elif self.items.has_key(itemName):
            removeFormatting(itemName)

    def update(self, *args):
        VerticalContainer.update(self, *args)

        if self._dirty:
            self._refreshVisibleItems()
            self._dirty = False

    def _refreshVisibleItems(self):
        for key, item in self.items.iteritems():
            item.hide()

        shownItems = self._findItemsThatFit(self.listItemViewedIndex)
        for item in shownItems:
            item.show()
            item.changeLayer(self.layer + 1)

        self._refreshPositions()

    def _findItemsThatFit(self, fromIndex):
        """
        Returns a list of items (values from self.items) starting from fromIndex
        in self.itemOrder, until the accumulated height of the items no longer
        fits in self.rect.
        """
        height = self.padding[1]
        itemsThatFit = []
        for item in self.itemOrder[fromIndex:]:
            height += self.items[item].rect.height + self.padding[1]
            if height > self.rect.height:
                break
            else:
                itemsThatFit.append(self.items[item])

        return itemsThatFit

    def scrollUp(self):
        if self.listItemViewedIndex is None:  # this implies that there are no items
            return

        # don't bother trying to scroll up if we're already at the top
        if self.listItemViewedIndex > 0:
            self.listItemViewedIndex -= 1
            self._refreshVisibleItems()

    def scrollDown(self):
        if self.listItemViewedIndex is None:  # this implies that there are no items
            return

        # don't bother trying to scroll down if we're already at the bottom
        if self.listItemViewedIndex < len(self.itemOrder) - 1:
            self.listItemViewedIndex += 1
            self._refreshVisibleItems()

    def setActive(self, widget=None):
        VerticalContainer.setActive(self, self)

    def handleEvent(self, event):
        VerticalContainer.handleEvent(self, event)

        # find clicks on children, do select
        if event.type == MOUSEBUTTONDOWN:
            for name, item in self.items.iteritems():
                if item.rect.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.select(name)
                    return
            
            self.unselect()
        # handle keys up and down, do scroll/select
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                try:
                    index = self.itemOrder.index(self.selectedItem) - 1
                except ValueError:
                    return

                if index >= 0:
                    self.scrollUp()
                    self.select(self.itemOrder[index])
            elif event.key == K_DOWN:
                try:
                    index = self.itemOrder.index(self.selectedItem) + 1
                except ValueError:
                    return

                if index < len(self.itemOrder):
                    self.scrollDown()
                    self.select(self.itemOrder[index])
