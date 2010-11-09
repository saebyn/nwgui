
import unittest

from nwgui.buttonbar import ButtonBar

from widget_test import GameMock, GUIMock

class ButtonBarTest(unittest.TestCase):
    def _createWidget(self):
        guimock = GUIMock()
        return ButtonBar(100, 36, root=guimock)

    def testConstructorWorks(self):
        self._createWidget()

    def testAddBankWorks(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
    
    def testGetBanksListsBank(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
        self.assertTrue("name" in buttonbar.getBanks())

    def testGetButtonsListsButton(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
        buttonbar.addButton("buttonsprite")
        self.assertTrue("buttonsprite" in map(lambda x: x[0], buttonbar.getButtons()))

    def testGetButtonsReturnsWithCallbacks(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
        callback = lambda name: None
        buttonbar.addButton("buttonsprite", callback=callback)
        self.assertEqual(filter(lambda x: x[0]=="buttonsprite", buttonbar.getButtons())[0][1], callback)

    def testActivateDoesCurrentBank(self):
        buttonbar = self._createWidget()
        self.correctCallback = False
        def callback(name):
            self.correctCallback = True

        buttonbar.addBank("first")
        buttonbar.addButton("1", callback=None)
        buttonbar.addBank("second")
        buttonbar.addButton("2", callback=callback)
        buttonbar.activate(0)

        self.assertTrue(self.correctCallback)

    def testActivateWorksWithCorrectBankAfterSwitch(self):
        buttonbar = self._createWidget()
        self.incorrectCallback = False
        def callback(name):
            self.incorrectCallback = True

        buttonbar.addBank("first")
        buttonbar.addButton("1", callback=None)
        buttonbar.addBank("second")
        buttonbar.addButton("2", callback=callback)

        buttonbar.switchBank("first")
        buttonbar.activate(0)

        self.assertFalse(self.incorrectCallback)

    def testGetButtonsWithSpecificBank(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
        buttonbar.addButton("buttonsprite")
        buttonbar.addBank("name2")
        buttonbar.addButton("buttonsprite2")

        self.assertTrue("buttonsprite" in map(lambda x: x[0], buttonbar.getButtons(bank="name")))
 
    def testClearBankRemovesAllWidgets(self):
        buttonbar = self._createWidget()
        buttonbar.addBank("name")
        buttonbar.addButton("buttonsprite")
        buttonbar.addButton("buttonsprite")
        buttonbar.addButton("buttonsprite")
        buttonbar.clearBank("name")
        self.assertEqual(len(buttonbar._bankContainers["name"].widgets), 0)
