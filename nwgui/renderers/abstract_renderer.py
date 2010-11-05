
class AbstractRenderer(object):
    def getSpriteSource(self, name):
        raise NotImplementedError

    def font(self, name, size):
        raise NotImplementedError

    def addSprite(self, sprite):
        raise NotImplementedError

    def getTopLayer(self):
        raise NotImplementedError

    def getBottomLayer(self):
        raise NotImplementedError

    def changeLayer(self, widget, layer):
        raise NotImplementedError
