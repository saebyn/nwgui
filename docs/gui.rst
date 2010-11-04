
GUI
===

The nwgui module requires a `game` object to function. This object
must be an instance of a class that:

1. Provides an attribute `guiSprites` that is an instance of
   `pygame.sprite.LayeredUpdates`.

2. Provides an `addGUISprite(sprite)` method which calls 
   `guiSprites.add(sprite)`.

3. Provides a `getSheet(sheetName)` method which returns an instance of
   `Spritesheet` (or a subclass of that class).

4. Provides an attribute `screen` that at least provides `get_width()`
   and `get_height()` methods (for instance, this could be the display 
   surface).
