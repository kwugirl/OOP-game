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