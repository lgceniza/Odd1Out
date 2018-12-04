""" Interface Elements
This module contains the elements which are necessary to create the interface
of the game: text labels, images, sounds, colors, and button objects. This module requires
the 'elements' module, as well as 'pyglet' to be installed.

This module can be imported and contains the following:
	* Tuples defining the background color and dimensions of the game window
	* Image texture object of the title sprite and of the game images watermarks
	* Audio effects to play throughout the game
	* Imports a font to use throughout the game
	* Lists of game tile images for use in the game
	* List of labels to display with text taken from instructions.txt
	* Labels displaying in-game screen captions:
		** howtoplay_label - displays "HOW TO PLAY" on the appropriate screen
		** timelabel - displays the timer in the game screen
		** selectdiff_label - displays "SELECT DIFFICULTY" on the appropriate screen
		** confirm_label - displays a confirmation message about the chosen
			difficulty on the appropriate screen
		** score_display - displays the player's current score on the game screen
		** yourscore_label - displays "YOUR SCORE" on the appropriate screen
		** name_label - displays the name of the previous player
		** score_label - displays the score of the previous player
		** scoreboard_label - displays "SCOREBOARD" on the appropriate screen
	* Labels displaying name and score for the "SCOREBOARD" screen
	* Button objects to be displayed in the window
	* GameTimer objects to be displayed in the game window
"""

import pyglet, elements

# WINDOW ATTRIBUTES. BACKGROUND COLOR AND WINDOW DIMENSIONS
bgcolor = (240/255, 133/255, 28/255, 1)
width, height = (850,650)

# TITLE IMAGE
title = pyglet.resource.image("assets/Ozone.jpg")
title.anchor_x = title.width/2
title.anchor_y = title.height/2
ozone = pyglet.sprite.Sprite(title, x=width/2, y=height//1.6)

# REGULAR SOUND EFFECTS
click_sound = pyglet.resource.media('assets/music/click.wav', streaming=False)
timeout_sound = pyglet.resource.media('assets/music/timeout.wav', streaming=False)
correct_sound = pyglet.resource.media('assets/music/correct.wav', streaming=False)

# IMPORTING FONT TO BE USED THROUGHOUT THE GAME
# SOURCE: https://github.com/JulietaUla/Montserrat
pyglet.font.add_file("assets/MontserratEL.ttf")
pyglet.font.load("Montserrat ExtraLight", bold = True)

# LISTS OF GAME TILES TO BE RANDOMLY PICKED PER BOARD
# SOURCE: https://thenounproject.com/nickbluth/collection/pandas/
Cats = ["cat1", "cat2", "cat3"]
Dogs = ["dog1", "dog2", "dog3"]
Octopi = ["octopus1", "octopus2", "octopus3"]
Raccoons = ["raccoon1", "raccoon2", "raccoon3"]
# SOURCE: https://thenounproject.com/aomam/collections/
Pandas = ["panda1", "panda2", "panda3"]
# LIST OF GAME TILE SETS TO BE RANDOMLY PICKED PER BOARD
tileset_list = [Cats, Dogs, Octopi, Pandas, Raccoons]

# IMAGE WATERMARKS
watermark = pyglet.resource.image("assets/watermarks.png")
watermark_sprite = pyglet.sprite.Sprite(watermark)
watermark_sprite.opacity = 0

instructions = []

# FILLING THE instructions LIST WITH LABEL OBJECTS TO BE DRAWN
def batch_fill():
	## IMPORTING TEXT FILE TO DISPLAY IN THE 'HOW TO PLAY' SCREEN
	instructions_file = open("assets/instructions.txt")
	for line in instructions_file:
		instruction = pyglet.text.Label(line, font_name = "Montserrat ExtraLight", font_size = 20,
			bold = True, x=width/2, y=height/2, width=width-200, height=height-400,
			anchor_x="center", anchor_y="center", align = "center", multiline = True)
		if "?" in line:
			instruction.height -= instruction.height+150
		instructions.append(instruction)
	instructions_file.close()
# CLEARING ALL THE ITEMS IN THE instructions LIST
def batch_clear():
	instructions.clear()

# LOADING THE LEADERBOARD TEXT FILE
def load_leaderboard():
	leaderboard_file = open("assets/leaderboard.txt", "r")
	line = leaderboard_file.readlines()
	leaderboard_file.close()
	## RETURNS ALL THE LINES IN THE FILE. EACH LINE CONTAINS A NAME AND A SCORE
	return line

# TAKES THE NAMES AND SCORES FROM THE LEADERBOARD FILE
def get_scores(score_info, namelabel, scorelabel):
	score = score_info[0]
	name = score_info[1]
	namelabel.text = name
	scorelabel.text = score

# SETS THE SCORES AND NAMES INTO PRE-MADE LABELS
def set_scores(names):
	one.text = "1."
	two.text = "2."
	three.text = "3."
	if len(names) == 1:
		score_info = names[0].split()
		get_scores(score_info, name1, score1)
	elif len(names) == 2:
		score_info = names[0].split()
		score_info2 = names[1].split()
		get_scores(score_info, name1, score1)
		get_scores(score_info2, name2, score2)
	else:
		score_info = names[-3].split()
		score_info2 = names[-2].split()
		score_info3 = names[-1].split()
		get_scores(score_info, name1, score1)
		get_scores(score_info2, name2, score2)
		get_scores(score_info3, name3, score3)

# DISPLAYS SCREEN CAPTIONS IN THE APPROPRIATE SCREENS
# BATCH RENDERING
labelbatch = pyglet.graphics.Batch()
howtoplay_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 60,
	bold = True, x=width/2, y=height-height/5, anchor_x="center", anchor_y="center", batch = labelbatch)
timelabel = pyglet.text.Label("",
	font_name = "Montserrat ExtraLight", font_size = 36, bold = True, italic = True,
	x=width/2, y=height-50, anchor_x="center", anchor_y="baseline", batch = labelbatch)
selectdiff_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 50,
	x=width/2, y=height-height/3, anchor_x="center", anchor_y="center", batch = labelbatch)
confirm_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 60,
	x=width/2, y=height-height/2.8, anchor_x="center", anchor_y="center", batch = labelbatch)
score_display = pyglet.text.Label("", font_name = "Century Gothic", font_size = 72, x=720, y=550, batch = labelbatch)
yourscore_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 45,
	x=width/2, y=height-height/5, anchor_x="center", anchor_y="center", batch = labelbatch)
name_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 80,
	x=width/2, y=height-height/2.8, anchor_x="center", anchor_y="center", batch = labelbatch)
score_label = pyglet.text.Label("", font_name = "Century Gothic", font_size = 160,
	x=width/2, y=height/1.9, anchor_x="center", anchor_y="center", batch = labelbatch)
scoreboard_label = pyglet.text.Label("", font_name = "Montserrat ExtraLight", font_size = 45,
	x=width/2, y=height-height/6, anchor_x="center", anchor_y="baseline", batch=labelbatch)

# DISPLAYS THE SCORES IN THE SCOREBOARD SCREEN
# BATCH RENDERING
scoreslabelbatch = pyglet.graphics.Batch()
one = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/6, y=650-650/3, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
two = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/6, y=one.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
three = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/6, y=two.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
name1 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/2, y=650-650/3, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
name2 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/2, y=one.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
name3 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850/2, y=two.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
score1 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850-850/6, y=650-650/3, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
score2 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850-850/6, y=one.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)
score3 = pyglet.text.Label("", font_name = "Century Gothic", font_size = 45,
	x=850-850/6, y=two.y-100, anchor_x="center", anchor_y="center", batch=scoreslabelbatch)

# BUTTON OBJECTS TO BE DISPLAYED IN THE OFF-GAME SCREENS
# BATCH RENDERING
buttonbatch = pyglet.graphics.Batch()
playbutton = elements.Button("Title_Play", width/2, height/1.92, buttonbatch)
nextpage = elements.Button("Next", width/2, height/6, buttonbatch)
nextchoice = elements.Button("Right_Arrow", width/1.18, height/2.7, buttonbatch)
previouschoice = elements.Button("Left_Arrow", width/7, height/2.7, buttonbatch)
easydiff = elements.Button("Easy", width/2, height/2.85, buttonbatch)
mediumdiff = elements.Button("Medium", width/2, height/2.85, buttonbatch)
harddiff = elements.Button("Hard", width/2, height/2.85, buttonbatch)
yeschoice = elements.Button("Yes", width/1.4, height//5, buttonbatch)
nochoice = elements.Button("No", width/3.8, height//5, buttonbatch)
playagain = elements.Button("Play_Again", width/4, height/6, buttonbatch)
scoretable = elements.Button("Score", width-width/4, height/6, buttonbatch)
exitbutton = elements.Button("Exit", width/2, height//5, buttonbatch)
backbutton = elements.Button("Back", 80, 10, buttonbatch)

# LIST OF OBJECTS MADE FOR EASIER DRAWING/CLEARING
labellist = [howtoplay_label, timelabel, selectdiff_label, confirm_label, score_display,
				yourscore_label, name_label, score_label, scoreboard_label]
scorelabellist = [one, two, three, name1, name2, name3, score1, score2, score3]
buttonlist = [playbutton, nextpage, nextchoice, previouschoice, easydiff, mediumdiff, harddiff,
				yeschoice, nochoice, playagain, scoretable, exitbutton, backbutton]

# GAMETIMER OBJECTS TO BE DISPLAYED DURING THE GAME
easytime = elements.GameTimer(1, 30)
mediumtime = elements.GameTimer(1, 00)
hardtime = elements.GameTimer(0, 30)