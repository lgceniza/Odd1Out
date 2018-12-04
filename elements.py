""" Game Elements
This module contains the most important elements that are essential to make the
game: the buttons, the game tiles, and the timer. This module requires 'pyglet'
to be installed.

This module can be imported and contains the following classes:
	* Button - creates off-game button objects
	* GameButton - creates in-game button objects
	* GameTimer - creates an in-game timer object
"""

import pyglet

class Button:
	"""
	A class used to create off-game button objects.

	...

	Attributes
	----------
	name : str
		name of the button image file
	x : int
		horizontal position of the button
	y : int
		vertical position of the button
	width : int
		width of the button
	height : int
		height of the button
	
	Methods
	-------
	when_pressed()
		changes the hue of the button to be a darker blue, to show pressed status
	when_not_pressed()
		changes the button back to its original hue and changes the sprite, to
		show non-pressed status
	when_hovered(xpos, ypos)
		returns the truth value of whether or not the cursor is hovering over
		the button
	when_hovering(xpos, ypos)
		changes the sprite of the button when the cursor is hovering over it
	button_show()
		makes the button visible in the screen
	button_clear()
		makes the button invisible in the screen
	"""

	def __init__(self, name, x, y, batch):
		""" Initializes the name and position of the button.
		
		Parameters
		----------
		name : str
			name of the button image file
		x : int
			horizontal position of the button
		y : int
			vertical position of the button
		batch : obj
			batch object to which the button will be appended
		"""

		self.name = name
		self.x = x
		self.y = y
		self.hoveredimage = pyglet.resource.image("assets/buttons/" + self.name + ".png")
		self.notpressedimage = pyglet.resource.image("assets/buttons/" + self.name + "_.png")
		self.width = self.notpressedimage.width
		self.height = self.notpressedimage.height
		self.buttonimage = pyglet.sprite.Sprite(self.notpressedimage,
			x=self.x-(self.width/2), y=self.y, batch=batch)

		if self.name == "Title_Play" or self.name == "Exit":
			self.buttonimage.visible = True
		else:
			self.buttonimage.visible = False

	def when_pressed(self):
		self.buttonimage.color = (150,214,242)

	def when_not_pressed(self):
		self.buttonimage.color = (255,255,255)
		self.buttonimage.image = self.notpressedimage
		self.buttonimage.draw()

	def when_hovered(self, xpos, ypos):
		""" Checks whether or not the cursor is hovering over the button.
		This method is used in mouse click events.

		Parameters
		----------
		xpos : int
			current horizontal position of the cursor
		ypos : int
			current vertical position of the cursor
		
		Returns
		-------
		boolean
			a truth value of whether or not the cursor is hovering
			over the button
		"""

		if self.x + self.width/2 >= xpos >= self.x-(self.width/2) and self.y + self.height >= ypos >= self.y:
			return True
		return False

	def when_hovering(self, xpos, ypos):
		""" Checks whether or not the cursor is hovering over the button.
		This method is used in mouse motion events.

		Parameters
		----------
		xpos : int
			current horizontal position of the cursor
		ypos : int
			current vertical position of the cursor
		"""

		if self.when_hovered(xpos,ypos):
			self.buttonimage.image = self.hoveredimage
			self.buttonimage.draw()
		else:
			self.buttonimage.image = self.notpressedimage
			self.buttonimage.draw()

	def button_show(self):
		self.buttonimage.visible = True

	def button_clear(self):
		self.buttonimage.visible = False

class GameButton:
	"""
	A class used to create in-game button objects.

	...

	Attributes
	----------
	name : str
		name of the button image file
	batch : obj
		batch object to which the button will be appended
	width : int
		width of the button
	height : int
		height of the button
	
	Methods
	-------
	when_hovered(x, y, xpos, ypos)
		returns the truth value of whether or not the cursor is hovering over
		the button
	button_show()
		makes the button visible in the screen
	button_clear()
		makes the button invisible in the screen
	"""

	def __init__(self, name, batch):
		""" Initializes the name and visibility of the game tile.

		Parameters
		----------
		name : str
			name of the button image file
		batch : graphics object
			a set of images to be drawn at once
		"""

		self.name = name
		self.gametile = pyglet.resource.image("assets/gameimages/" + self.name + ".png")
		self.gametileimage = pyglet.sprite.Sprite(self.gametile, batch = batch)
		self.width = self.gametile.width
		self.height = self.gametile.height
		self.gametileimage.visible = False

	def when_hovered(self, x, y, xpos, ypos):
		""" Checks whether or not the cursor is hovering the game tile.
		This method is used in mouse click events.

		Parameters
		----------
		x : int
			horizontal position of the game tile
		y : int
			vertical position of the game tile
		xpos : int
			horizontal position of the cursor
		ypos : int
			vertical position of the cursor
		
		Returns
		-------
		boolean
			a truth value of whether or not the cursor is hovering
			over the button
		"""

		if x + self.width >= xpos >= x and y + self.height >= ypos >= y:
			return True
		return False

	def button_show(self):
		self.gametileimage.visible = True

	def button_clear(self):
		self.gametileimage.visible = False


class GameTimer:
	"""
	A class used to create the in-game timer.

	...

	Attributes
	----------
	minute : int
		initial minute mark of the timer
	second : int
		initial second mark of the timer
	start : str
		initial timer string

	Methods
	-------
	RunMinutes()
		decreases the minute mark by 1 if minute mark is greater than 0
	RunSeconds()
		decreases the second mark by 1. If there are 0 seconds left and
		more than 0 minutes left, then it calls RunMinutes() and resets the
		seconds mark to 59.
	TimerReset()
		restores the timer to its initial state
	"""

	def __init__(self, minute, second):
		""" Initializes the duration of the timer in minutes and seconds.

		Parameters
		----------
		minute : int
			initial minute mark of the timer
		second : int
			initial second mark of the timer
		"""

		if second == 0:
			self.start = "0{}:00"
		else:
			self.start = "0{}:{}".format(minute,second)
		self.start_minute = minute
		self.start_second = second
		self.minute = self.start_minute
		self.second = self.start_second

	def RunMinutes(self):
		if self.minute > 0:
			self.minute -= 1

	def RunSeconds(self):
		if self.second > 0:
			self.second -= 1
		elif self.second == 0 and self.minute > 0:
			self.RunMinutes()
			self.second = 59

	def TimerReset(self):
		self.minute = self.start_minute
		self.second = self.start_second