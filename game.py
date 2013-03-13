import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7
GAME_STATE = True

#### Put class definitions here ####

class Harry(GameElement):
	IMAGE = "Harry"
	SOLID = True

	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []

	def next_pos(self, direction): # this is an instance method inside a class. self is used to refer to the instance it's inside of. Returns a tuple where [0] is the x position and [1] is the y position
		if direction == "up":
			return (self.x, self.y-1)
		elif direction == "down":
			return (self.x, self.y+1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None	

	# How other game elements interact with Harry
	def interact(self, player, name):
		if len(player.inventory) != 0:
			GAME_BOARD.draw_msg("Oh no Harry has died, game is over now.")
			
			# delete harry from the board
			GAME_BOARD.del_el(HARRY.x, HARRY.y)

			# move voldy to that position
			GAME_BOARD.del_el(player.x, player.y)
			GAME_BOARD.set_el(HARRY.x, HARRY.y, VOLDEMORT)

			global GAME_STATE # need to declare it as a global variable in the function we're using
			GAME_STATE = False # indicates that the game is now over! 

		else:
			GAME_BOARD.draw_msg("You can't kill Harry yet, you need the Sorceror's Stone! Ahh pain!!!")

class Voldemort(GameElement):
	IMAGE = "Voldemort"
	SOLID = True
	
	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []

	def next_pos(self, direction): # this is an instance method inside a class. self is used to refer to the instance it's inside of. Returns a tuple where [0] is the x position and [1] is the y position
		if direction == "up":
			return (self.x, self.y-1)
		elif direction == "down":
			return (self.x, self.y+1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None

	def interact(self, player, name):
		if len(player.inventory) != 0:
			GAME_BOARD.draw_msg("Hooray! The magical world is saved! Voldemort is dead!")
			
			# delete Voldemort from the board
			GAME_BOARD.del_el(VOLDEMORT.x, VOLDEMORT.y)

			# move Harry to that position
			GAME_BOARD.del_el(player.x, player.y)
			GAME_BOARD.set_el(VOLDEMORT.x, VOLDEMORT.y, HARRY)

			global GAME_STATE
			GAME_STATE = False

		else:
			GAME_BOARD.draw_msg("Don't run into Voldemort before you have the Hallows!")

class Gem(GameElement):
	IMAGE = "BlueGem"
	SOLID = False

	def interact(self, player, name):

		if name == "Voldemort":
			player.inventory.append(self)
			GAME_BOARD.draw_msg("%s has just acquired the Sorceror's Stone! Watch out Harry!" % name)
		else:
			GAME_BOARD.draw_msg("The Sorceror's Stone is off limits to you!")

class Hallows(GameElement):
	IMAGE = "Key"
	SOLID = False

	def interact(self, player, name):

		if name == "Harry":
			player.inventory.append(self)
			GAME_BOARD.draw_msg("%s has just acquired the Deathly Hallows! Watch out Voldemort!" % name)
		else:
			GAME_BOARD.draw_msg("The Deathly Hallows are off limits to you!")
			

####   End class definitions    ####



def initialize(): # could pass a variable in here if you wanted to start a saved game (i.e. previous player positions)
    """Put game initialization code here"""
    
    global HARRY # defines HARRY as a global variable to be able to use in other functions later on like keyboard_handler
    HARRY = Harry()
    GAME_BOARD.register(HARRY)
    harry_x = 0
    harry_y = 3
    GAME_BOARD.set_el(harry_x, harry_y, HARRY)

    global VOLDEMORT
    VOLDEMORT = Voldemort()
    GAME_BOARD.register(VOLDEMORT)
    voldemort_x = 6
    voldemort_y = 3
    GAME_BOARD.set_el(voldemort_x, voldemort_y, VOLDEMORT)

    starting_positions = [(0,3), (6,3)]

    gem = Gem()
    global gem_x # global definition because we use it later to make sure Harry can't get the Sorceror's Stone
    global gem_y
    gem_x = random.randint(0,6)
    gem_y = random.randint(0,6)
    # while loop to make sure new position isn't already taken, if it is, then make a new position
    while (gem_x, gem_y) in starting_positions:
		gem_x = random.randint(0,6)
		gem_y = random.randint(0,6)    	
	# once confirmed that this is a unique tuple of x,y position, add it to the list
    starting_positions.append((gem_x, gem_y))
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(gem_x, gem_y, gem)

    hallows = Hallows()
    global hallows_x  # global definition because we use it later to make sure Voldemort can't get the Hallows
    global hallows_y
    hallows_x = random.randint(0,6)
    hallows_y = random.randint(0,6)
    while (hallows_x, hallows_y) in starting_positions:
		hallows_x = random.randint(0,6)
		hallows_y = random.randint(0,6)    	
    starting_positions.append((hallows_x, hallows_y))
    GAME_BOARD.register(hallows)
    GAME_BOARD.set_el(hallows_x, hallows_y, hallows)

    # initial msg that shows when the game starts
    GAME_BOARD.draw_msg("Neither can live while the other survives! Arrows control Harry, #pad (1/2/3/5) controls Voldemort.")

def keyboard_handler():

	if GAME_STATE == False:
		return

	# these control the Harry player
	if KEYBOARD[key.UP]:
		character_move(HARRY,"Harry", "up")
		#harry_direction = "up"
	if KEYBOARD[key.RIGHT]:
		character_move(HARRY,"Harry", "right")
	if KEYBOARD[key.LEFT]:
		character_move(HARRY,"Harry", "left")
	if KEYBOARD[key.DOWN]:
		character_move(HARRY,"Harry", "down")

	# these control the Voldemort player
	if KEYBOARD[key.NUM_5]:
		character_move(VOLDEMORT,"Voldemort", "up")
	if KEYBOARD[key.NUM_3]:
		character_move(VOLDEMORT,"Voldemort", "right")
	if KEYBOARD[key.NUM_1]:
		character_move(VOLDEMORT,"Voldemort", "left")
	if KEYBOARD[key.NUM_2]:
		character_move(VOLDEMORT,"Voldemort", "down")

	if KEYBOARD[key.SPACE]:
		GAME_BOARD.erase_msg()


def character_move(character, name, direction):
	GAME_BOARD.erase_msg() # erases any existing message, like initial instructions or ran into something solid msg

	next_location = character.next_pos(direction) # feed direction in to call the next_pos method

	next_x = next_location[0] # first pos from the tuple for x
	next_y = next_location[1] # second pos from the tuple for y

	if GAME_BOARD.check_bounds(next_x, next_y) == False:
		GAME_BOARD.draw_msg("You can't go out of bounds! Apparition is disabled in this game!")
		return
	else:
		existing_el = GAME_BOARD.get_el(next_x, next_y)

	# have character interact with the element in the next space if necessary
	if existing_el:
		existing_el.interact(character, name)

	# make sure Harry cannot access the sorcerer's stone
	if name == "Harry" and next_x == gem_x and next_y == gem_y:
		return

	# Make sure voldemort cannot access the deathly hallows
	if name == "Voldemort" and next_x == hallows_x and next_y == hallows_y:
		return

	# move character to the next space
	if existing_el is None or not existing_el.SOLID:
		GAME_BOARD.del_el(character.x, character.y) # delete player from existing pos on board
		GAME_BOARD.set_el(next_x, next_y, character) # add player again in the new position
		print "%s's new position is:" % name, character.x, character.y