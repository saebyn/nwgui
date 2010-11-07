
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

import operator

from nwgui.widget import Widget
from nwgui.tab import Tab

class Container(Widget):
    def __init__(self, width, height, *args, **kwargs):
        self.image = pygame.Surface((width, height))
        Widget.__init__(self, width, height, *args, **kwargs)

        if kwargs.has_key('background'):
            background = kwargs['background']
        else:
            background = (255, 255, 255)

        if kwargs.has_key('border'):
            border = kwargs['border']
        else:
            border = None

        self.image.fill(background)

        if border is not None:
            pygame.draw.rect(self.image, border[1], self.rect, border[0])

        self.widgets = []

    def handleEvent(self, event):
        # handle mouse events by deciding which widgets are in the clicked area
        for widget in self.widgets:
            if event.type in [MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP]:
                if widget.rect.contains(pygame.Rect(pygame.mouse.get_pos(),
                                                    (1, 1))):
                    widget.handleEvent(event)
            else:
                widget.handleEvent(event)

    def _getWidgetsByLayer(self):
        layers = {}

        currentLayer = 0
        for widget in sorted(self.widgets, key=operator.attrgetter('layer')):
            if widget.layer != currentLayer:
                currentLayer = widget.layer
                layers[currentLayer] = []

            layers[currentLayer].append(widget)

        return layers

    def moveToFront(self):
        Widget.moveToFront(self)

        # move all child widgets to their appropriate layers in front of self
        widgets = self._getWidgetsByLayer()
        layers = widgets.keys()
        # sort the keys so that we proceed from lowest layer to highest
        layers.sort()
        for layer in layers:
            # move this first widget to the front
            firstWidget = widgets[layer][0]
            firstWidget.moveToFront()

            # move the remaining widgets in this layer to the same layer
            for widget in widgets[layer][1:]:
                widget.changeLayer(firstWidget.layer)

    def moveToBack(self):
        # move all child widgets to their appropriate layers in front of self
        widgets = self._getWidgetsByLayer()
        layers = widgets.keys()
        # sort the keys so that we proceed from highest layer to lowest
        layers.sort(reverse=True)
        for layer in layers:
            # move this first widget to the back
            firstWidget = widgets[layer][0]
            firstWidget.moveToBack()

            # move the remaining widgets in this layer to the same layer
            for widget in widgets[layer][1:]:
                widget.changeLayer(firstWidget.layer)

        Widget.moveToBack(self)

    def changeLayer(self, layer):
        Widget.changeLayer(self, layer)
        for widget in self.widgets:
            widget.updateLayer()

    def updateLayer(self):
        Widget.updateLayer(self)
        for widget in self.widgets:
            widget.updateLayer()

    def show(self):
        Widget.show(self)

        for widget in self.widgets:
            widget.show()

    def hide(self):
        Widget.hide(self)

        for widget in self.widgets:
            widget.hide()

    def remove(self, widget):
        self.widgets.remove(widget)
        widget.kill()

    def removeAll(self):
        for widget in self.widgets:
            self.remove(widget)

    def kill(self):
        for widget in self.widgets:
            widget.kill()

        Widget.kill(self)

    def add(self, widget):
        self.widgets.append(widget)
        widget.setParent(self)
        widget.updateLayer()

class ArrangedContainer(Container):
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        self.last = 0
        if kwargs.has_key('padding'):
            self.padding = kwargs['padding']
        else:
            self.padding = (0, 0)

    def _findPosition(self, widget):
        raise NotImplementedError

    def add(self, widget):
        Container.add(self, widget)
        widget.setPosition(self._findPosition(widget))

    def remove(self, widget):
        Container.remove(self, widget)
        # reset our position to rearrange the remaining widgets
        self._refreshPositions()

    def _refreshPositions(self):
        self.setPosition(self.rect.topleft)

    def setPosition(self, position):
        Container.setPosition(self, position)
        self.last = 0
        for widget in self.widgets:
            if widget.isVisible():
                widget.setPosition(self._findPosition(widget))

class HorizontalContainer(ArrangedContainer):
    def _findPosition(self, widget):
        oldLast = self.last + self.padding[0]
        self.last += widget.rect.width + self.padding[0]
        return (oldLast + self.rect.left, self.rect.top + self.padding[1])

class VerticalContainer(ArrangedContainer):
    def _findPosition(self, widget):
        oldLast = self.last + self.padding[1]
        self.last += widget.rect.height + self.padding[1]
        return (self.rect.left + self.padding[0], oldLast + self.rect.top)

class TabbedContainer(Container):
    def __init__(self, width, height, *args, **kwargs):
        Container.__init__(self, width, height, *args, **kwargs)
        self.tabContents = {}
        self.tabNames = []
        self.tabSelected = None
        self.tabChanged = False

        if kwargs.has_key('tabMargin'):
            tabMargin = kwargs['tabMargin']
        else:
            tabMargin = 3

        self.tabRow = HorizontalContainer(width, 40, root=self.root, padding=(tabMargin, 0))
        Container.add(self, self.tabRow)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill( (255, 255, 255) )

    def showPage(self, tabName):
        self.tabSelected = tabName
        self.tabChanged = True

        for key, widget in self.tabContents.iteritems():
            if key == tabName:
                widget.moveToFront()
            else:
                widget.moveToBack()

    def add(self, tabName, widget):
        Container.add(self, widget)

        self.tabContents[tabName] = widget
        self.tabNames.append(tabName)  # need an ordered list of tabs here.
        widget.setPosition(self.rect.topleft)

        # add the extra widgets needed for the tabs
        tab = Tab(self, tabName, root=self.root, padding=(15, 15), background=(100, 100, 100))
        self.tabRow.add(tab)

    def remove(self, tabName):
        Container.remove(self, self.tabContents[tabName])
        del self.tabContents[tabName]

        self.tabNames.remove(tabName)
        if self.tabSelected == tabName:
            self.showPage(self.tabNames[0])

        tab = None
        for widget in self.tabRow.widgets:
            if widget.tabName == tabName:
                tab = widget

        if tab:
            self.tabRow.remove(tab)

    def setPosition(self, position):
        Container.setPosition(self, position)
        for widget in self.widgets:
            widget.setPosition(position)

        # update extra widgets
        self.tabRow.setPosition((self.rect.left, self.rect.bottom - 27))

        if self.tabSelected is None and len(self.tabNames) > 0:
            self.tabSelected = self.tabNames[0]

        self.tabChanged = True

    def update(self, *args):
        Container.update(self, *args)
        if self.tabChanged:
            self.showPage(self.tabSelected)
            self.tabChanged = False
            self.tabRow.moveToFront()

class AbsoluteContainer(Container):
    def add(self, widget, x, y):
        """
        Add the widget and position it at the coordinates (x, y) given.
        """
        Container.add(self, widget)
        widget.setPosition((x, y))
