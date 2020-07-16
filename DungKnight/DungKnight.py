### modules
import pygame as pg ## change the module name to pg
import random

## check for errors in pg module
try: pg.init()
except: print('error in pygame module!!!')

## window dimensions
WIDTH = 640
HEIGHT = 512

## window dimension
window_dimension = (WIDTH,HEIGHT)

## game window
window = pg.display.set_mode(window_dimension)

## game title
window_title = 'DungKnight'

## set the window title
set_title = pg.display.set_caption(window_title)

## game state
run = True

## game sprites

knight_sprite = 'assets/entities/knight_1.png'

tile_sprite = 'assets/tiles/floor_purple_dirt_tile.png'

hud_sprites = {
'status':'assets/hud/status_background.png',
'life':'assets/hud/life.png',
'life_up':'assets/hud/life_up.png'
}

env_sprites = {
'bush1':'assets/envirement/green_bush_1.png',
'stone1':'assets/envirement/stone_1.png'
}

pickup_sprite = {
'meat':'assets/pickups/meat_pickup.png',
}

color = {
'white':(255 ,255 ,255 ),
'black':(0 ,0 ,0 ),
'red':(100 ,0 ,0 ),
'green':(0 ,100 ,0 ),
'blue':(0 ,0 ,100 ),
}

room_tile_width = WIDTH // 64
room_tile_height = HEIGHT // 64

room_tiles = []

room_envirement_objects = []

room_pickups = []

life_list = []

## object class

class object:

	def __init__(self ,x ,y ,sprite_path ,name='object' ):

		self.x = x
		self.y = y
		self.solid = False
		self.sprite = pg.image.load( sprite_path )
		self.name = name

	def draw(self):

		window.blit(self.sprite , (self.x ,self.y ) )

	def check_collision(self ,x ,y ,object_list ):

		for other in object_list:

			if self.x + x == other.x and self.y + y == other.y:

				return True

			else:
				
				continue

	def is_collide(self,obj_list):

		for other in obj_list:

			if self.x == other.x and self.y == other.y:

				del obj_list[obj_list.index(other)]
				return True
			else:

				continue

### game functions

### create the game floor
def create_game_floor_tile(sprite):
	
	## positions
	x = 0
	y = 0

	## count
	count = 0

	while x < room_tile_width:

		room_tiles.append( object(64 * x ,64 ,sprite ,'tile_' + str( count ) ) )

		count += 1

		while y < room_tile_height:
			
			room_tiles.append ( object(64 * x ,64 * (y + 1) ,sprite ,'tile_' + str( count ) ) )

			count += 1

			y += 1

			if y >= room_tile_height:

				y = 0

				break
		x += 1

### draw all the objects inside a list
def draw_a_list(list):

	for object in list:

		object.draw()

### create the envirement objects (random)
def create_envirement_objects(env_list,sprite,name,times):


	for t in range(times):

		## positions		
		x = random.randint(0 ,(WIDTH - 1) // 64) * 64
		y = random.randint(1 ,(HEIGHT) // 64) * 64

		## add the object to the list
		env_list.append(object(x ,y ,sprite ,name + '_{}'.format(t) ) ) 

def create_player_life(lifes):

	for l in range(lifes):

		life_list.append(object((17*l)+6 ,6,hud_sprites['life'] ,'life_'+str(l) ) )

def life_up(obj,obj_life_list,lvl):

	if obj.life < life_max:

		obj.life += 1

		obj_life_list.append(object((17*len(life_list))+6 ,6,hud_sprites['life_up'] ,'life_'+str(len(obj_life_list)) ) )



## player object
knight = object(64 ,64 ,knight_sprite ,'Knight')

## status bg object
status_background = object(0 ,0 ,hud_sprites['status'] ,'status_bg' )

## create the game floor
create_game_floor_tile(tile_sprite)

## create envirement objects
create_envirement_objects(
room_envirement_objects , ## object list
env_sprites['bush1'] ,    ## sprites
'bush' , ## name
5 ) 	 ## amount

## ^ bush
create_envirement_objects(
room_envirement_objects ,
env_sprites['stone1'] ,
'stone' ,
5 )	
##  ^ stone

knight.life = 5
life_max = knight.life+1

create_player_life(knight.life)

create_envirement_objects(
room_pickups ,
pickup_sprite['meat'] ,
'meat',
5 )	


## game loop
while run:

	for event in pg.event.get():

		## quit game event
		if event.type == pg.QUIT:

			run = False

		if event.type == pg.KEYDOWN:

			if knight.life > 0:
				### right
				if event.key == pg.K_d and not knight.check_collision(64,0,room_envirement_objects) and knight.x < WIDTH-64:

					knight.x += 64
				### left
				if event.key == pg.K_a and not knight.check_collision(-64,0,room_envirement_objects) and knight.x > 0:

					knight.x -= 64
				### down
				if event.key == pg.K_s and not knight.check_collision(0,64,room_envirement_objects) and knight.y < HEIGHT-64:

					knight.y += 64
				### up
				if event.key == pg.K_w and not knight.check_collision(0,-64,room_envirement_objects) and knight.y > 64:

					knight.y -= 64
				#### TEST
				if event.key == pg.K_e:
					if len(life_list) > 0:

						del life_list[-1]
						knight.life -= 1

				if knight.is_collide(room_pickups):

					life_up(knight,life_list,1)

	## fill the screen bg
	window.fill(color['black'])

	### draw the game tiles
	draw_a_list(room_tiles)
	
	### draw the envirement objects
	draw_a_list(room_envirement_objects)

	draw_a_list(room_pickups)

	### draw the player
	knight.draw()
	
	### draw the status bg
	status_background.draw()

	draw_a_list(life_list)

	## update screen
	pg.display.flip()