import pygame
import button
import csv
import pickle #Commenting out the original Save and Load while-loops

pygame.init()
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Limit FPS
clock = pygame.time.Clock()
FPS = 60

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Define Game Vars
ROWS = 16
MAX_COL = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS #Determines how big each of the squares on the grid are
TILE_FOLDER = 'C:/Users/cmc03/Desktop/TwitchPython/PyGames/Pygame-Tile-Level-Editor/img/tile' #MUST KNOW AND CHANGE BEFORE RUNNING
TILE_COUNT = 21 #MUST KNOW AND CHANGE BEFORE RUNNING
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
level = 0 #Current level working on
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Load Images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Store tiles in a list
img_list = []
for x in range(TILE_COUNT):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) #Make the tiles fit the grid squares
	img_list.append(img)

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Save/Load Button
save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Create Empty Tile List csv
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COL #Create a list of 16 rows * 150 '-1'.  -1 is for Empty space
	world_data.append(r)

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Force Create a Ground
for tile in range(0,MAX_COL):
	world_data[ROWS - 1][tile] = 0

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Define Colors
GREEN = (144,201,120)
WHITE = (255,255,255)
RED = (200,25,25)

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Function to outputing text to screen
font = pygame.font.SysFont('Futura', 30)
def draw_text(text, font, text_col, x,y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x,y))
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Creat Function to draw background
def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4): #(x*width) Redraw image when scrolling
		screen.blit(sky_img,((x*width)-scroll * .05,0)) #Sky scroll at slower rate
		screen.blit(mountain_img,((x*width)-scroll * .06,SCREEN_HEIGHT - mountain_img.get_height()-300)) #Offset by 300
		screen.blit(pine1_img,((x*width)-scroll * .07,SCREEN_HEIGHT - pine1_img.get_height()-150)) #Offset by 300
		screen.blit(pine2_img,((x*width)-scroll * .08,SCREEN_HEIGHT - pine2_img.get_height())) #No offset
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Draw Grid
def draw_grid():
	#Vertical Lines
	for c in range(MAX_COL + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),(c * TILE_SIZE - scroll, SCREEN_HEIGHT)) #-scroll to move grid while scrolling/.line(screen size, color, (x = c aka iterator, y),(x = c aka iterator,y))
	#Horizontal Lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE),(SCREEN_WIDTH, c * TILE_SIZE)) #.line(screen size, color, (x, y = c aka iterator),(x, = c aka iterator))

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Function for drawing world Tiles
def draw_world(): #Iterate in a for-loop through the empty tiles in the world_data list
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#Create Buttons in List
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1) #scale of 1
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1) #scale of 1
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1) #Arbitrary but looks nice. button.Button(x,y,number,scale)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
run = True

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#[][][][][][][][][][][][][][][][][][]                                                  [][][][][][][][][][][][][][]
#[][][][][][][][][][][][][][][][][][]                    GAME WINDOW                   [][][][][][][][][][][][][][]
#[][][][][][][][][][][][][][][][][][]                                                  [][][][][][][][][][][][][][]
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
while run:
	clock.tick(FPS)
	#Call Backgrounds
	draw_bg()
	draw_grid()
	draw_world()
	draw_text(f'Level: {level}', font, WHITE, 10,SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press Up or Down to change Level', font, WHITE, 10,SCREEN_HEIGHT + LOWER_MARGIN - 60)
	#Svae and Load data
	if save_button.draw(screen):
		#Save level data NOTE:NO CONFIRMATION GIVEN AFTER SAVE
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
		# with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
		# 	writer = csv.writer(csvfile, delimiter=',')
		# 	for row in world_data:
		# 		writer.writerow(row)

	if load_button.draw(screen):
		#Load in level data and reset scroll back to start of level
		#NOTE: This error handling will erase bottom floor if a level does not exist when loading.  Just re-draw bottom manually
		try:
		 scroll = 0
		 world_data = []
		 pickle_in = open(f'level{level}_data', 'rb')
		 world_data = pickle.load(pickle_in)
		except  FileNotFoundError:
			pass
		# with open(f'level{level}_data.csv', 'r', newline='') as csvfile:
		# 	reader = csv.reader(csvfile, delimiter=',')
		# 	for row in world_data:
		# 		for x, row in enumerate(reader):
		# 			for y, tile in enumerate(row):
		# 				world_data[x][y] = int(tile)

	#Draw Tile Panel and Tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH,0,SIDE_MARGIN,SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen): #draw def in Button Class in button.py, returns bool value
			current_tile = button_count
	#Highlight Selected Tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect,3) #3 = border size of rectangle

	#Scroll Map
	if scroll_left == True and scroll > 0: #Only scroll left as far as 0
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COL * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#Add new tiles to screen
	#Get mouse pos
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#Check that coords are withing tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		#erase tiles
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		#Keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				scroll_left = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				scroll_right = True
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				level += 1
			if event.key == pygame.K_DOWN or event.key == pygame.K_s and level > 0:
				level -= 1			
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 5				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				scroll_left = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				scroll_right = False
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 1






	pygame.display.update()

pygame.quit()