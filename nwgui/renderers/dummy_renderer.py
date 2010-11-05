
from nwgui.renderers.abstract_renderer import AbstractRenderer

class DummyRenderer(AbstractRenderer):
    def __init__(self):
        self.layers = {}

    def getSpriteSource(self, name):
        return None

    def font(self, name, size):
        return None

    def addSprite(self, sprite):
        pass

    def getTopLayer(self):
        layers = self.layers.keys()
        layers.sort()
        try:
            return layers[-1]
        except IndexError:
            return 0

    def getBottomLayer(self):
        layers = self.layers.keys()
        layers.sort()
        try:
            return layers[0]
        except IndexError:
            return 0

    def changeLayer(self, widget, layer):
        widget.layer = layer
        for key, value in self.layers.iteritems():
            if widget in value:
                self.layers[key].remove(widget)
                break
        
        if not self.layers.has_key(layer):
            self.layers[layer] = []

        self.layers[layer].append(widget)
