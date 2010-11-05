
import unittest

from nwgui.gui import GUI
from nwgui.widget import Widget
from nwgui.renderers.dummy_renderer import DummyRenderer

class GameMock(object):
    def getSpriteSource(self, name):
        return None

class GUIMock(object):
    def __init__(self):
        self.setNameValue = None
        self.activeWidget = None

    def setName(self, name, widget):
        self.setNameValue = name

    def setActive(self, widget):
        self.activeWidget = widget

    def getGameObject(self):
        return GameMock()

class WidgetTest(unittest.TestCase):
    def _createWidget(self, klass, renderer=None, root=None, *args, **kwargs):
        if renderer is None:
            renderer = DummyRenderer()

        if root is None:
            root = GUIMock()

        return klass(*args, root=root, renderer=renderer, **kwargs)

    def testWidgetConstructorWorks(self):
        widget = self._createWidget(Widget, width=100, height=100)

    def testMoveToFrontWorks(self):
        renderer = DummyRenderer()
        widget1 = self._createWidget(Widget, width=100, height=100, renderer=renderer)
        widget2 = self._createWidget(Widget, width=100, height=100, renderer=renderer)
        widget2.moveToFront()
        self.assertTrue(widget1.getLayer() < widget2.getLayer())

    def testMoveToBackWorks(self):
        renderer = DummyRenderer()
        widget1 = self._createWidget(Widget, width=100, height=100, renderer=renderer)
        widget2 = self._createWidget(Widget, width=100, height=100, renderer=renderer)
        widget2.moveToBack()
        self.assertTrue(widget1.getLayer() > widget2.getLayer())

    def testSetNameUpdatesGUI(self):
        root = GUIMock()
        widget = self._createWidget(Widget, width=100, height=100, root=root)
        widget.setName('test')
        self.assertEqual(root.setNameValue, 'test')

    def testSetActiveBubblesWhenParentAdded(self):
        renderer = DummyRenderer()
        root = GUIMock()
        widget1 = self._createWidget(Widget, width=100, height=100, renderer=renderer, root=root)
        widget2 = self._createWidget(Widget, width=100, height=100, renderer=renderer, root=root)

        widget1.setParent(root)

        widget2.setActive()

        self.assertNotEqual(root.activeWidget, widget2)
        
        widget2.setParent(widget1)

        self.assertEqual(root.activeWidget, widget2)
