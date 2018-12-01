""" Text Input Window
This is a modification from the link below:
inspired from pyglet documentation examples/text_input.py
www.github.com/adamlwgriffiths/Pyglet/blob/master/examples/text_input.py

This module contains the classes that initialize a new window to handle text
user-input. This module requires 'pyglet' to be installed.

This module can be imported and contains the following classes:
    * Rectangle - creates a rectangle background for TextWidget 
    * TextWidget - creates a layout for text
    * Text_input- creates a new window for text input

FIXME : Text input does not handle insertion.
"""

import pyglet

def save_name(file, name):
    """ Writes a new string on new line """ 
    name_file = open(file, 'a+')
    name_file.write(" " + name + "\n")
    name_file.close()

class Rectangle:
    """
    A class used to draw a rectangle.

    ...

    Attributes
    ----------
    x1, y1, x2, y2 : int
        vertices of the rectangle
    batch : class of Batch()
    """

    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
            )
  
class TextWidget:
    """
    A class used to create a layout for text.

    ...

    Attributes
    ----------
    x : int
        horizontal position of Rectangle
    y : int
        vertical position of Rectangle
    width : int
        width of the Rectangle
    batch : class of Batch()        
    """

    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), dict(color = (0, 0, 0, 255), font_size = 18))
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # RECTANGULAR OUTLINE
        pad = 3
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

class Text_Input(pyglet.window.Window):
    """
    A class used to create a separate window for text input.
    
    ...

    Attributes
    ----------
    x : int
        horizontal position of Rectangle
    y : int
        vertical position of Rectangle
    width : int
        width of the Rectangle
    batch : class of Batch()

    Methods
    -------
    on_draw()
        draws the background of the Text_Input window 
    on_text()
        sets the location where the caret appears 
    on_text_motion
        sets BACKSPACE as the only key to edit string_name 
    on_key_press()
        sets alphabet letter keys as the only keys to edit string_name
    on_close()
        handles no given input name when this window is closed
    set_focus()
        sets the caret location
    """

    def __init__(self, *args, **kwargs):
        super(Text_Input, self).__init__(400, 140, caption='Name entry')
        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label('Type your name:', x = 200, y = 100, anchor_x = 'center', anchor_y = 'center',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('**limit character up to 10**', x = 200, y = 25, font_size = 10, anchor_x = 'center', anchor_y = 'bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('*use letters only*', x = 200, y = 10, font_size = 10, anchor_x = 'center', anchor_y = 'bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
                        ]
        self.widgets = [TextWidget('', 110, 60, self.width - 210, self.batch)]
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.set_focus(self.widgets[0])
        self.string_name = ""

    def on_draw(self):
        """ Draws the background of the Text_input window """
        pyglet.gl.glClearColor(1,1,1,1)
        self.clear()
        self.batch.draw() 
   
    def on_text(self, text):
        """ This sets the location where the caret appears.

        Parameters
        ----------
        text : visual updating of user input
        """ 

        if self.focus: self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        """ This allows backspace as the only motion to edit string_name.

        Parameters
        ----------
        motion : constant values defined in pyglet.window.key
        """

        if motion != pyglet.window.key.MOTION_BACKSPACE:
            motion = 0 
        else:
            if self.focus: self.focus.caret.on_text_motion(motion)

    def on_key_press(self, symbol, modifiers):
        """ This handles only alphabet letter key presses to edit string_name.

        Parameters
        ----------
        symbol : constant values defined in pyglet.window.key
        modifiers : constant values defined in pyglet.window.key
        """ 

        if len(self.string_name) > 10:
            self.string_name = self.string_name[:-1]
                
        # SAVES THE STRING INPUT BY PRESSING ENTER
        if symbol == pyglet.window.key.ENTER:
            print(self.string_name)
            save_name('assets/leaderboard.txt',self.string_name.rstrip())
            pyglet.window.Window.close(self)

        if symbol == pyglet.window.key.ESCAPE: pyglet.app.exit()
        
        # CONCATENATES VALID KEY PRESSES TO STRING_NAME
        if symbol == pyglet.window.key.A: self.string_name += "A"
        if symbol == pyglet.window.key.B: self.string_name += "B"
        if symbol == pyglet.window.key.C: self.string_name += "C"
        if symbol == pyglet.window.key.D: self.string_name += "D"
        if symbol == pyglet.window.key.E: self.string_name += "E"
        if symbol == pyglet.window.key.F: self.string_name += "F"
        if symbol == pyglet.window.key.G: self.string_name += "G"
        if symbol == pyglet.window.key.H: self.string_name += "H"
        if symbol == pyglet.window.key.I: self.string_name += "I"
        if symbol == pyglet.window.key.J: self.string_name += "J"
        if symbol == pyglet.window.key.K: self.string_name += "K"
        if symbol == pyglet.window.key.L: self.string_name += "L"
        if symbol == pyglet.window.key.M: self.string_name += "M"
        if symbol == pyglet.window.key.N: self.string_name += "N"
        if symbol == pyglet.window.key.O: self.string_name += "O"
        if symbol == pyglet.window.key.P: self.string_name += "P"
        if symbol == pyglet.window.key.Q: self.string_name += "Q"
        if symbol == pyglet.window.key.R: self.string_name += "R"
        if symbol == pyglet.window.key.S: self.string_name += "S"
        if symbol == pyglet.window.key.T: self.string_name += "T"
        if symbol == pyglet.window.key.U: self.string_name += "U"
        if symbol == pyglet.window.key.V: self.string_name += "V"
        if symbol == pyglet.window.key.W: self.string_name += "W"
        if symbol == pyglet.window.key.X: self.string_name += "X"
        if symbol == pyglet.window.key.Y: self.string_name += "Y"
        if symbol == pyglet.window.key.Z: self.string_name += "Z"
        if symbol == pyglet.window.key.BACKSPACE: self.string_name = self.string_name[:-1]

    def on_close(self):
        """ Handles no given input name when this window is closed """
        if self.string_name == "":
            pyglet.text.Label('*INVALID*', x = 200, y = 120, font_size = 10, anchor_x = 'center', anchor_y = 'bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
        else:
            save_name('assets/leaderboard.txt',self.string_name.rstrip())
            pyglet.window.Window.close(self)
    
    
    def set_focus(self, focus):
        """ This sets the caret location """
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)