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
number_horcruxes = 2
GAME_ASPLODE = False

#### Put class definitions here ####

class Harry(GameElement):
	IMAGE = "Harry"
	SOLID = True

	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []
		self.timer = 0

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
			GAME_BOARD.draw_msg("Oh no Harry has died, game is over now. Hit esc to exit.")
			
			# delete harry from the board
			GAME_BOARD.del_el(HARRY.x, HARRY.y)

			# move voldy to that position
			GAME_BOARD.del_el(player.x, player.y)
			GAME_BOARD.set_el(HARRY.x, HARRY.y, VOLDEMORT)

			global GAME_STATE # need to declare it as a global variable in the function we're using to indicate within the function stackframe that we're using the outside global variable, not making a new one inside the function universe
			GAME_STATE = False # indicates that the game is now over! 

		else:
			GAME_BOARD.draw_msg("You can't kill Harry yet, you need the Elder Wand! Ahh pain!!!")

	def update(self, dt):
		global GAME_ASPLODE
		global GAME_STATE
		if GAME_ASPLODE == True: # this only runs after we've gotten to the GAME_ASPLODE being true in the code
			self.timer += dt
			GAME_STATE = False

			# insert something cool to happen while delay is going on
			board_positions = []

			for x in range(GAME_WIDTH):
				for y in range(GAME_HEIGHT):
					board_positions.append((x,y))

			for (x,y) in board_positions:
				GAME_BOARD.set_el(x, y, lightning_bolt)

		if self.timer > 5: # this is where we set how long the delay should be
			# print("Stuff happened after 5 seconds")
			self.timer = 0
			GAME_STATE = True
			GAME_ASPLODE = False

			for (x,y) in board_positions:
				GAME_BOARD.del_el(x, y)

			# reset Harry and Voldemort at new positions on the board
			position_harry = unique_rand_position("Harry")
			GAME_BOARD.set_el(position_harry[0], position_harry[1], HARRY)

			position_voldemort = unique_rand_position("Voldemort")
			GAME_BOARD.set_el(position_voldemort[0], position_voldemort[1], VOLDEMORT)

			GAME_BOARD.draw_msg("Go after Voldemort again!")


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
		if len(player.inventory) == number_horcruxes:
			# delete both from the board
			GAME_BOARD.del_el(VOLDEMORT.x, VOLDEMORT.y)
			GAME_BOARD.del_el(HARRY.x, HARRY.y)

			player.inventory.append("harry_horcrux")

			GAME_BOARD.draw_msg("Harry is having a heart-to-heart w/ Dumbledore right now...")

			global GAME_ASPLODE
			GAME_ASPLODE = True # this sets off the update function to have a delay before character reappear again. This is under the Harry interact function.
			
			
		elif len(player.inventory) == number_horcruxes+1: # harry has sacrificed himself and has attacked Voldemort a 2nd time, game over
			GAME_BOARD.draw_msg("Hooray! The magical world is saved! Voldemort is dead! Hit esc to exit.")

			# delete Voldemort from the board
			GAME_BOARD.del_el(VOLDEMORT.x, VOLDEMORT.y)
			# move Harry to that position
			GAME_BOARD.del_el(player.x, player.y)
			GAME_BOARD.set_el(VOLDEMORT.x, VOLDEMORT.y, HARRY)
			
			# ends the game
			global GAME_STATE
			GAME_STATE = False

		else:
			GAME_BOARD.draw_msg("Don't run into Voldemort before you have all the Horcruxes!")

class ElderWand(GameElement):
	IMAGE = "Elderwand"
	SOLID = False

	def interact(self, player, name):

		if name == "Voldemort":
			player.inventory.append(self)

			del positions_dict["elderwand"] # elderwand off the board, remove from positions dictionary

			GAME_BOARD.draw_msg("%s has just acquired the Elder Wand! Watch out Harry!" % name)
		else:
			GAME_BOARD.draw_msg("The Elder Wand is off limits to you!")

### This class is the object that appears on the initial game board
class Horcruxes(GameElement):
	IMAGE = "BlueGem"
	SOLID = False

	def interact(self, player, name):
		if name == "Harry" and len(player.inventory) < number_horcruxes-2: # has to be -2 because we append new items you've picked up to the inventory list AFTER you interact with it and get into the if conditional
			player.inventory.append(self)
			GAME_BOARD.draw_msg("%s now has %d Horcruxes, get the rest to kill Voldemort!" % (name, len(player.inventory)))

			position = unique_rand_position("horcrux")
			GAME_BOARD.set_el(position[0], position[1], horcrux)

		elif name == "Harry" and len(player.inventory) == number_horcruxes-2:
			player.inventory.append(self)
			GAME_BOARD.draw_msg("%s now has all but the last %d Horcrux, go get the last one!" % (name, len(player.inventory)))

			position = unique_rand_position("last_horcrux")
			GAME_BOARD.set_el(position[0], position[1], last_horcrux)

		else:
			if len(VOLDEMORT.inventory) == 0:
				GAME_BOARD.draw_msg("Voldemort doesn't care about Horcruxes, go get the Elder Wand instead!")
			else:
				GAME_BOARD.draw_msg("Voldemort has the Elder Wand now, just go after Harry!")

### This class is everything that appears conditionally			
class Last_Horcrux(GameElement):
	IMAGE = "GreenGem"
	SOLID = False

	def interact(self, player, name):

		if name == "Harry":
			player.inventory.append(self)

			del positions_dict["horcrux"] # all horcruxes off the board, remove from positions dictionary

			GAME_BOARD.draw_msg("%s has just acquired all of the Horcruxes! Watch out Voldemort!" % name)
		else:
			GAME_BOARD.draw_msg("Voldemort doesn't care about Horcruxes, go get the Elder Wand instead!")

class LightningBolt(GameElement):
	IMAGE = "Lightning"

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
    #print "Voldemort's starting position", voldemort_x, voldemort_y

### DICTIONARY TO HOLD EVERY OBJECT'S POSITION
    global positions_dict
    positions_dict = {
		"Harry": (harry_x, harry_y),
		"Voldemort": (voldemort_x, voldemort_y),
	}

### ELDER WAND THAT APPEARS IN INITIAL GAME SETUP ###
    global elderwand
    elderwand = ElderWand()
    GAME_BOARD.register(elderwand)

    position = unique_rand_position("elderwand")
    GAME_BOARD.set_el(position[0], position[1], elderwand)

### THE FIRST HORCRUX THAT HARRY HAS TO PICK UP ###
    global horcrux
    horcrux = Horcruxes()
    GAME_BOARD.register(horcrux)
    
    position = unique_rand_position("horcrux")
    GAME_BOARD.set_el(position[0], position[1], horcrux)
    
### THE LAST HORCRUX THAT APPEARS AFTER HARRY GETS THE OTHER HORCRUXES ###
    global last_horcrux
    last_horcrux = Last_Horcrux()
    GAME_BOARD.register(last_horcrux)

    # initial msg that shows when the game starts
    GAME_BOARD.draw_msg("Neither can live while the other survives! Arrows control Harry, #pad (1/2/3/5) controls Voldemort.")

### LIGHTNING BOLT DURING GAME DELAY
    global lightning_bolt
    lightning_bolt = LightningBolt()
    GAME_BOARD.register(lightning_bolt)

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
		#print existing_el

	# make sure Harry cannot access the Elder Wand
	if name == "Harry" and existing_el == elderwand:
		return

	# Make sure voldemort cannot access the horcruxes
	if name == "Voldemort" and (existing_el == horcrux or existing_el == last_horcrux):
		return

	# move character to the next space
	if existing_el is None or not existing_el.SOLID:
		GAME_BOARD.del_el(character.x, character.y) # delete player from existing pos on board
		GAME_BOARD.set_el(next_x, next_y, character) # add player again in the new position
		positions_dict[name] = (next_x, next_y) # resetting player's name position in the positions dictionary
		#print "%s's new position is:" % name, character.x, character.y
		#print HARRY.inventory, len(HARRY.inventory)
		#print positions_dict[name]

def unique_rand_position(name):
    name_x = random.randint(0,GAME_WIDTH-1)
    name_y = random.randint(0,GAME_HEIGHT-1)
    # while loop to make sure new position isn't already taken, if it is, then make a new position
    while (name_x, name_y) in positions_dict.values():
        name_x = random.randint(0,GAME_WIDTH-1)
        name_y = random.randint(0,GAME_HEIGHT-1)
    # once confirmed that this is a unique tuple of x,y position, add it to the dictionary
    positions_dict[name] = (name_x, name_y)
    return (name_x, name_y)