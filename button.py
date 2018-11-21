import pyglet

class Button:
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.pressedimage = pyglet.resource.image("assets/" + self.name + ".png")
		self.notpressedimage = pyglet.resource.image("assets/" + self.name + "_.png")
		self.buttonimage = pyglet.sprite.Sprite(self.notpressedimage, x=self.x, y=self.y)
		self.width = self.notpressedimage.width
		self.height = self.notpressedimage.height

	def button_draw(self):
		self.buttonimage.draw()

	def when_pressed(self):
		self.buttonimage.image = self.pressedimage
		self.buttonimage.draw()

	def when_not_pressed(self):
		self.buttonimage.image = self.notpressedimage
		self.buttonimage.draw()

	def when_hovered(self, xpos, ypos):
		if self.x + self.width >= xpos >= self.x and self.y + self.height >= ypos >= self.y:
			return True
		return False