
import pygame
from pygame.locals import *

from nwgui.container import VerticalContainer

class List(VerticalContainer):
    def __init__(self, *args, **kwargs):
        kwargs['padding'] = (5, 5)
        kwargs['border'] = (1, (0, 0, 0))
        VerticalContainer.__init__(self, *args, **kwargs)
        self.items = []
        # This is the index of the item at the top of the
        # displayed list of items. It is None if there are no items.
        self.listItemViewedIndex = None
        self.selectedItem = None
        self._dirty = True
        self.callback = None

        # TODO add up/down buttons
        # TODO draw scroll location indicator

    def add(self, name, widget):
        VerticalContainer.add(self, widget)
        self.items.append((name, widget))
        if self.listItemViewedIndex is None:
            self.listItemViewedIndex = 0

    def clear(self):
        """
        Remove all items from the list.
        """
        names = map(lambda nw: nw[0], self.items)
        for name in names:
            self.remove(name)

    def _find(self, name):
        """
        Returns the widget of the first item in self.items with the matching name.
        """
        return filter(lambda nw: nw[0] == name, self.items)[0][1]

    def _has(self, name):
        """
        Returns True if one of the items in self.items has the name.
        """
        return name in map(lambda nw: nw[0], self.items)

    def _index(self, value):
        return map(lambda nw: nw[1], self.items).index(value)

    def remove(self, name):
        widget = self._find(name)

        VerticalContainer.remove(self, widget)

        self.items.remove((name, widget))

        if self.listItemViewedIndex >= len(self.items):
            self.listItemViewedIndex = len(self.items) - 1

        if self.listItemViewedIndex == -1:
            self.listItemViewedIndex = None

    def getSelected(self):
        return self.items[self.selectedItem][0]

    def getSelectedIndex(self):
        return self.selectedItem

    def hasSelected(self):
        return self.selectedItem is not None

    def select(self, itemIndex):
        if self.selectedItem is not None:
            self.unselect(self.selectedItem)

        self.selectedItem = itemIndex
        name, widget = self.items[itemIndex]
        widget.setColor((255, 255, 255))
        widget.setBackground((0, 0, 100))

        if self.callback is not None:
            self.callback(name, itemIndex)

    def setSelectCallback(self, callback):
        self.callback = callback

    def clearSelectCallback(self):
        self.callback = None

    def unselect(self, itemIndex=None):
        self.selectedItem = None

        def removeFormatting(widget):
            widget.setBackground((255, 255, 255))
            widget.setColor((0, 0, 0))

        if itemIndex is None:
            for name, widget in self.items:
                removeFormatting(widget)
        else:
            try:
                removeFormatting(self.items[itemIndex][1])
            except IndexError:
                pass

    def update(self, *args):
        VerticalContainer.update(self, *args)

        if self._dirty:
            self._refreshVisibleItems()
            self._dirty = False

    def _refreshVisibleItems(self):
        for key, item in self.items:
            item.hide()

        shownItems = self._findItemsThatFit(self.listItemViewedIndex)
        for item in shownItems:
            item.show()
            item.changeLayer(self.layer + 1)

        self._refreshPositions()

    def _findItemsThatFit(self, fromIndex):
        """
        Returns a list of items (values from self.items) starting from fromIndex
        in self.items, until the accumulated height of the items no longer
        fits in self.rect.
        """
        height = self.padding[1]
        itemsThatFit = []
        for itemName, widget in self.items[fromIndex:]:
            height += widget.rect.height + self.padding[1]
            if height > self.rect.height:
                break
            else:
                itemsThatFit.append(widget)

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
        if self.listItemViewedIndex < len(self.items) - 1:
            self.listItemViewedIndex += 1
            self._refreshVisibleItems()

    def setActive(self, widget=None):
        VerticalContainer.setActive(self, self)

    def handleEvent(self, event):
        VerticalContainer.handleEvent(self, event)

        # find clicks on children, do select
        if event.type == MOUSEBUTTONDOWN:
            for index in xrange(0, len(self.items)):
                if self.items[index][1].rect.collidepoint(pygame.mouse.get_pos()):
                    self.select(index)
                    return
            
            self.unselect()
        # handle keys up and down, do scroll/select
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                try:
                    index = self.selectedItem - 1
                except ValueError:
                    return

                if index >= 0:
                    self.scrollUp()
                    self.select(index)
            elif event.key == K_DOWN:
                try:
                    index = self.selectedItem + 1
                except ValueError:
                    return

                if index < len(self.items):
                    self.scrollDown()
                    self.select(index)
