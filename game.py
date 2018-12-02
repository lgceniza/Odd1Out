""" Main Game
This script runs the game. It requires the modules 'elements', 'interface',
'text_input', and 'random' to be imported, and also most necessarily requires
'pyglet' to be installed, as the entire game is written with pyglet.

This script contains the following 8 functions:
	* Difficulty - creates the 'select difficulty' screen
	* Confirm - creates the 'confirm difficulty' screen
	* Scoreboard - creates the 'previous score' screen, resets game elements
		to their initial state, and saves the score
	* timer_deplete - depletes the in-game timer
	* tileset_pick - randomly chooses a set of tiles for one game screen
	* board_create - creates the game board
	* initialize - calls the functions tileset_pick() and board_create() to make
		one game screen, and also initializes the odd one out checker
	* gameloop - runs the game recursively until the timer runs out

This script contains the following events:
	* on_draw - draws the window
	* on_mouse_motion - calls functions in case of mouse motion; used mainly for
		displaying button hover state
	* on_mouse_press - calls functions in case of mouse button press; used mainly
		for displaying pressed button state
	* on_mouse_release - calls functions in case of mouse button release; used
		for displaying unpressed button state, and for calling functions to clear
		the window to draw the next game scene
"""

import pyglet, elements, interface, text_input, random
from pyglet.window import mouse

def Difficulty():
	""" This function creates the 'select difficulty' screen whenever needed. """
	interface.selectdiff_label.text = "CHOOSE DIFFICULTY"
	interface.previouschoice.button_show()
	interface.nextchoice.button_show()
	interface.easydiff.button_show()

def Confirm(dependentstring):
	""" This function creates the 'confirm difficulty' screen whenever needed.

	Parameters
	----------
	dependentstring : str
		the game mode choice to be confirmed by the player
	"""

	interface.click_sound.play()
	interface.selectdiff_label.text = ""
	interface.previouschoice.button_clear()
	interface.nextchoice.button_clear()
	interface.confirm_label.text = dependentstring
	interface.yeschoice.button_show()
	interface.nochoice.button_show()

def Scoreboard(dt):
	""" This function creates the 'previous score' screen, resets game
	elements to their initial state, and saves the score.
	"""

	# GLOBAL VARIABLES TO INITIALIZE FOR ENDING THE GAME LOOP
	global game_start
	global score
	game_start = False
	interface.score_display.text = ""
	pyglet.clock.unschedule(timer_deplete)
	interface.watermark_sprite.opacity = 0
	# PLAYS A SOUND SIGNALLING THE END OF ONE PLAYTHROUGH
	interface.timeout_sound.play()
	for tile in board:
		tile.button_clear()
	interface.easytime.TimerReset()
	interface.mediumtime.TimerReset()
	interface.hardtime.TimerReset()
	interface.timelabel.text = ""
	# 'YOUR PREVIOUS SCORE' GAME SCENE.
	interface.scoreboard_label.text = "YOUR PREVIOUS SCORE:"
	# THESE WILL NOT SHOW ANYTHING IF IT WAS THE FIRST GAME.
	interface.name_label.text = interface.prevname
	interface.score_label.text = interface.prevscore
	# SAVING THE LATEST ACHIEVED SCORE INTO A TEXT FILE
	file = open("assets/leaderboard.txt", "a+")
	file.write(str(score))
	file.close()
	# RESETTING THE SCORE
	score = 0
	interface.diffselect.button_show()
	# SAVING THE PLAYER'S NAME ALONGSIDE THEIR SCORE
	textwindow = text_input.Text_Input()

def timer_deplete(dt):
	""" This function depletes the in-game timer to prevent a non-ending game.

	Parameters
	----------
	dt : float
		the rate of function calls
	"""

	# GLOBAL VARIABLE TO INITIALIZE FOR STARTING THE GAME TIMER
	global mode
	# IF-ELSE STATEMENTS ARE NECESSARY TO PREVENT A WEIRD-LOOKING TIMER.
	if mode == "EASY":
		interface.easytime.RunSeconds()
		if interface.easytime.second > 9:
			interface.timelabel.text = "0{}:{}".format(interface.easytime.minute, interface.easytime.second)
		else:
			interface.timelabel.text = "0{}:0{}".format(interface.easytime.minute, interface.easytime.second)
	elif mode == "MEDIUM":
		interface.mediumtime.RunSeconds()
		if interface.mediumtime.second > 9:
			interface.timelabel.text = "0{}:{}".format(interface.mediumtime.minute, interface.mediumtime.second)
		else:
			interface.timelabel.text = "0{}:0{}".format(interface.mediumtime.minute, interface.mediumtime.second)
	elif mode == "HARD":
		interface.hardtime.RunSeconds()
		if interface.hardtime.second > 9:
			interface.timelabel.text = "00:{}".format(interface.hardtime.second)
		else:
			interface.timelabel.text = "00:0{}".format(interface.hardtime.second)

def tileset_pick(tileset_list):
	""" This function randomly chooses a set of game tiles for one game screen.

	A set of 3 tiles is randomly picked from a set of 5 tile sets. Then, 2 out
	of these 3 tiles are randomly picked to be the (a) common tile and then the
	(b) odd tile, respectively.

	Parameters
	----------
	tileset_list : list
		a list of 5 tile sets from which 1 set will be picked

	Returns
	-------
	random_tiles : list
		a list of the images used to create the game board
	check_tile : dict
		a dictionary containing only 0s and a 1 as values, where keys with a
		value 0 are common tiles and the key with the value 1 is the odd tile
	"""

	tileset = random.choice(tileset_list)
	# POPS THE COMMON TILE SO IT WILL NOT BE PICKED AGAIN AS AN ODD TILE
	default_tile = tileset.pop(tileset.index(random.choice(tileset)))
	# ADDS COMMON TILES 1 LESS THAN THE SIZE OF THE BOARD
	random_tiles = [default_tile for i in range(35)]
	# CREATES A CHECKER OF THE ODD TILE
	check_tile = ({}.fromkeys(random_tiles, 0))
	odd = random.choice(tileset)
	random_tiles.append(odd)
	random.shuffle(random_tiles)
	check_tile[odd] = 1
	# RETURNS THE COMMON TILE TO THE TILE SET
	tileset.append(default_tile)
	return random_tiles, check_tile

def board_create(random_tiles):
	""" This function creates the game board, initializing each game button
	with x- and y-coordinates

	Parameters
	----------
	random_tiles : list
		a list of image names to be made into buttons

	Returns
	-------
	board : list
		a list of button objects with their corresponding sprites and positions
	"""

	board = []
	x_position = 125
	y_position = 10
	initial_x = x_position
	
	for tile in random_tiles:
		square = elements.GameButton(tile, batch)
		square.buttonimage.set_position(x_position, y_position)
		board.append(square)

		if len(board) % 6 == 0 and len(board) != 36:
			x_position = initial_x
			y_position += square.height
		else:
			x_position += square.width
	return board

def initialize():
	""" This function calls the functions tileset_pick() and board_create()
	to make one game screen, and also to initialize the odd one out checker.

	Returns
	-------
	board : list
		a list of button objects with their corresponding sprites and positions
	random_tiles : list
		a list of the images used to create the game board
	check_tile : dict
		a dictionary containing only 0s and a 1 as values, where keys with a
		value 0 are common tiles and the key with the value 1 is the odd tile
	"""

	random_tiles, check_tile = tileset_pick(interface.tileset_list)
	board = board_create(random_tiles)
	return board, random_tiles, check_tile

def gameloop(x, y):
	""" This function runs the game loop.

	With this function, the game runs recursively until the in-game timer runs
	out. It checks whether or not the player has clicked on the correct odd
	tile, and then tallies the score. After each correct answer, this function
	reinitializes the game buttons on the board, their corresponding images, and
	the checker that comes with it. It changes the sprites on the board and the
	coordinates of the odd tile, and then calls itself.

	Parameters
	----------
	x : int
		horizontal position of the cursor
	y : int
		vertical position of the cursor
	"""

	# GLOBAL VARIABLE INITIALIZED TO BE ABLE TO REDRAW EACH SCREEN
	global board
	global random_tiles
	global check_tile
	global score
	for tile in board:
		tile.button_show()
	interface.score_display.text = str(score)
	index = 0
	# BOOLEAN TO DETERMINE IF THE PLAYER HAS FOUND THE ODD ONE OUT
	found = False
	for square in board:
		checker = check_tile.get(random_tiles[index])
		if checker:
			if square.buttonimage.visible and square.when_hovered(square.buttonimage.x, square.buttonimage.y, x, y):
					score += 1
					# PLAYS A SOUND AFTER SCORING A POINT
					interface.correct_sound.play()
					interface.score_display.text = str(score)
					found = True
					break
		index += 1
	if found:
		board, random_tiles, check_tile = initialize()
		i = 0
		for square in board:
			square.buttonimage.image = pyglet.resource.image("assets/gameimages/" + random_tiles[i] + ".png")
			i += 1
		gameloop(x, y)

# THE GAME WINDOW
window = pyglet.window.Window(850, 650)
pyglet.gl.glClearColor(*interface.bgcolor)

# THE GAME BOARD DRAWN IN A BATCH TO IMPROVE PERFORMANCE OF SPRITE RENDERING
batch = pyglet.graphics.Batch()
board, random_tiles, check_tile = initialize()

# INITIAL GAME VALUES
mode = ""
game_start = False
score = 0

# CREATES A LOOP OF BACKGROUND MUSIC
sound = pyglet.media.load('assets/music/background.wav')
looper = pyglet.media.SourceGroup(sound.audio_format, None)
looper.loop = True
looper.queue(sound)
music_player = pyglet.media.Player()
music_player.queue(looper)
music_player.play()

@window.event
def on_mouse_motion(x, y, dx, dy):
	""" This event is generated whenever the mouse cursor moves. This is
	mainly used for displaying button hover state.

	Parameters
	----------
	x : int
		horizontal position of the cursor
	y : int
		vertical position of the cursor
	dx : int
		change in the horizontal position of the cursor
	dy : int
		change in the vertical position of the cursor
	"""

	interface.playbutton.when_hovering(x,y)
	interface.exitbutton.when_hovering(x,y)
	interface.nextpage.when_hovering(x,y)
	interface.nextchoice.when_hovering(x,y)
	interface.previouschoice.when_hovering(x,y)
	interface.easydiff.when_hovering(x,y)
	interface.mediumdiff.when_hovering(x,y)
	interface.harddiff.when_hovering(x,y)
	interface.yeschoice.when_hovering(x,y)
	interface.nochoice.when_hovering(x,y)
	interface.diffselect.when_hovering(x,y)

@window.event
def on_mouse_press(x, y, button, modifiers):
	""" This event is generated whenever the mouse button is pressed. This is
	mainly used for displaying pressed button state.

	Parameters
	----------
	x : int
		horizontal position of the cursor
	y : int
		vertical position of the cursor
	"""

	if interface.playbutton.buttonimage.visible and interface.playbutton.when_hovered(x,y):
		interface.playbutton.when_pressed()
		interface.click_sound.play()
	if interface.exitbutton.buttonimage.visible and interface.exitbutton.when_hovered(x,y):
		interface.exitbutton.when_pressed()
		interface.click_sound.play()
	if interface.nextpage.buttonimage.visible and interface.nextpage.when_hovered(x,y):
		interface.nextpage.when_pressed()
		interface.click_sound.play()
	if interface.nextchoice.buttonimage.visible and interface.nextchoice.when_hovered(x,y):
		interface.nextchoice.when_pressed()
		interface.click_sound.play()
	if interface.previouschoice.buttonimage.visible and interface.previouschoice.when_hovered(x,y):
		interface.previouschoice.when_pressed()
		interface.click_sound.play()
	if interface.yeschoice.buttonimage.visible and interface.yeschoice.when_hovered(x,y):
		interface.yeschoice.when_pressed()
		interface.click_sound.play()
	if interface.nochoice.buttonimage.visible and interface.nochoice.when_hovered(x,y):
		interface.nochoice.when_pressed()
		interface.click_sound.play()
	if interface.diffselect.buttonimage.visible and interface.diffselect.when_hovered(x,y):
		interface.diffselect.when_pressed()
		interface.click_sound.play()

@window.event
def on_mouse_release(x, y, button, modifiers):
	""" This event is generated whenever the mouse button is released. This is
	mainly used	for displaying unpressed button state, and for calling functions
	to clear the window to draw the next game scene.

	Parameters
	----------
	x : int
		horizontal position of the cursor
	y : int
		vertical position of the cursor
	"""

	if interface.playbutton.buttonimage.visible and interface.playbutton.when_hovered(x,y):
		interface.playbutton.when_not_pressed()
		interface.ozone.opacity = 0
		interface.playbutton.button_clear()
		interface.exitbutton.button_clear()
		interface.howtoplay_label.text = "HOW TO PLAY"
		interface.batch_fill()
		interface.nextpage.button_show()
	if interface.exitbutton.buttonimage.visible and interface.exitbutton.when_hovered(x,y):
		pyglet.app.exit()
	if interface.nextpage.buttonimage.visible and interface.nextpage.when_hovered(x,y):
		interface.nextpage.when_not_pressed()
		interface.nextpage.button_clear()
		interface.howtoplay_label.text = ""
		interface.batch_clear()
		Difficulty()
	if interface.nextchoice.buttonimage.visible and interface.nextchoice.when_hovered(x,y):
		interface.nextchoice.when_not_pressed()
		if interface.easydiff.buttonimage.visible:
			interface.easydiff.button_clear()
			interface.mediumdiff.button_show()
		elif interface.mediumdiff.buttonimage.visible:
			interface.mediumdiff.button_clear()
			interface.harddiff.button_show()
		elif interface.harddiff.buttonimage.visible:
			interface.harddiff.button_clear()
			interface.easydiff.button_show()
	if interface.previouschoice.buttonimage.visible and interface.previouschoice.when_hovered(x,y):
		interface.previouschoice.when_not_pressed()
		if interface.easydiff.buttonimage.visible:
			interface.easydiff.button_clear()
			interface.harddiff.button_show()
		elif interface.mediumdiff.buttonimage.visible:
			interface.mediumdiff.button_clear()
			interface.easydiff.button_show()
		elif interface.harddiff.buttonimage.visible:
			interface.harddiff.button_clear()
			interface.mediumdiff.button_show()
	if interface.easydiff.buttonimage.visible and interface.easydiff.when_hovered(x,y):
		interface.easydiff.when_not_pressed()
		interface.easydiff.button_clear()
		Confirm("PLAY ON EASY?")
	if interface.mediumdiff.buttonimage.visible and interface.mediumdiff.when_hovered(x,y):
		interface.mediumdiff.when_not_pressed()
		interface.mediumdiff.button_clear()
		Confirm("PLAY ON MEDIUM?")
	if interface.harddiff.buttonimage.visible and interface.harddiff.when_hovered(x,y):
		interface.harddiff.when_not_pressed()
		interface.harddiff.button_clear()
		Confirm("PLAY ON HARD?")
	if interface.nochoice.buttonimage.visible and interface.nochoice.when_hovered(x,y):
		interface.nochoice.when_not_pressed()
		interface.yeschoice.button_clear()
		interface.nochoice.button_clear()
		interface.confirm_label.text = ""
		Difficulty()
	if interface.yeschoice.buttonimage.visible and interface.yeschoice.when_hovered(x,y):
		# GLOBAL VARIABLES TO INITIALIZE FOR STARTING THE GAME
		global mode
		global game_start
		interface.yeschoice.when_not_pressed()
		interface.yeschoice.button_clear()
		interface.nochoice.button_clear()
		# SCHEDULES THE NEXT SCREEN TO SHOW IN ACCORDANCE TO THE GAME TIMER
		# AT THAT GAME MODE
		if "EASY" in interface.confirm_label.text:
			mode = "EASY"
			interface.timelabel.text = interface.easytime.start
			pyglet.clock.schedule_once(Scoreboard, 90)
		elif "MEDIUM" in interface.confirm_label.text:
			mode = "MEDIUM"
			interface.timelabel.text = interface.mediumtime.start
			pyglet.clock.schedule_once(Scoreboard, 60)
		else:
			mode = "HARD"
			interface.timelabel.text = interface.hardtime.start
			pyglet.clock.schedule_once(Scoreboard, 30)
		interface.confirm_label.text = ""
		pyglet.clock.schedule_interval(timer_deplete,1)
		# NECESSARY TO NOT ACCIDENTALLY TRIGGER THE START OF THE GAME LOOP
		game_start = True
	if game_start:
		interface.watermark_sprite.opacity = 255
		gameloop(x,y)
	if interface.diffselect.buttonimage.visible and interface.diffselect.when_hovered(x,y):
		interface.diffselect.when_not_pressed()
		interface.diffselect.button_clear()
		interface.scoreboard_label.text = ""
		interface.name_label.text = ""
		interface.score_label.text = ""
		# LOADS THE LATEST PLAYER NAME AND THEIR SCORE TO SHOW IN THE NEXT
		# 'YOUR PREVIOUS SCORE' SCENE
		interface.load_leaderboard()
		Difficulty()

@window.event
def on_draw():
	""" This event is generated whenever the window is drawn. This function
	draws all the buttons, labels, and sprites.
	"""

	window.clear()

	interface.ozone.draw()
	interface.playbutton.buttonimage.draw()
	interface.exitbutton.buttonimage.draw()
	interface.howtoplay_label.draw()
	for label in interface.instructions:
		label.draw()
	interface.nextpage.buttonimage.draw()
	interface.selectdiff_label.draw()
	interface.mediumdiff.buttonimage.draw()
	interface.easydiff.buttonimage.draw()
	interface.harddiff.buttonimage.draw()
	interface.nextchoice.buttonimage.draw()
	interface.previouschoice.buttonimage.draw()
	interface.timelabel.draw()
	interface.confirm_label.draw()
	interface.yeschoice.buttonimage.draw()
	interface.nochoice.buttonimage.draw()
	interface.diffselect.buttonimage.draw()
	interface.watermark_sprite.draw()
	batch.draw()
	interface.score_display.draw()
	interface.scoreboard_label.draw()
	interface.name_label.draw()
	interface.score_label.draw()

pyglet.app.run()