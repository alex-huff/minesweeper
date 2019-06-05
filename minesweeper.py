import pygame, sys, random, math, time

pygame.font.init()
pygame.display.set_icon(pygame.image.load('mine.png'))
pygame.display.set_caption('Minesweeper')

class Minesweeper:
	def __init__(self):
		self.board_width, self.board_height = 16, 16
		self.width, self.height = 800, 800
		self.height += int(self.height / 6)
		self.piece_size = int(self.width / self.board_width)
		self.edge = int(self.piece_size / 7)
		self.start_time = time.time()
		self.clicked_yet = False
		self.seconds = 0
		self.bomb_count = 50
		self.flag_count = 0
		self.font = pygame.font.SysFont('Arial', self.piece_size)
		self.flag = pygame.transform.scale(pygame.image.load('flag.png'), (self.piece_size - 2 * self.edge, self.piece_size - 2 * self.edge))
		self.bomb = pygame.transform.scale(pygame.image.load('mine.png'), (self.piece_size, self.piece_size))
		self.coordinates = []
		self.game_over = [False, False]
		self.window = pygame.display.set_mode((self.width, self.height))
		self.fps = pygame.time.Clock()

class Tile():
	def __init__(self, x, y):
		self.coord = [x, y]
		self.type = 0
		self.shown = False
		self.is_flag = False

	def get_surrounding_bombs(self):
		bombs = 0

		for y, x in [[self.coord[0] - 1, self.coord[1] - 1],
						 [self.coord[0], self.coord[1] - 1],
						 [self.coord[0] + 1, self.coord[1] - 1],
						 [self.coord[0] - 1, self.coord[1]],
						 [self.coord[0] + 1, self.coord[1]],
						 [self.coord[0] - 1, self.coord[1] + 1],
						 [self.coord[0], self.coord[1] + 1],
						 [self.coord[0] + 1, self.coord[1] + 1]]:
			if x < 0:
				pass
			elif x > minesweeper.board_width - 1:
				pass
			elif y < 0:
				pass
			elif y > minesweeper.board_height - 1:
				pass
			else:
				bombs += board[y][x].type

		return(bombs)

def game_over_final():
	pygame.quit()
	sys.exit()

def text_objects(font, text, color, text_center):
	rendered = font.render(text, True, color)
	return rendered, rendered.get_rect(center = text_center)

def get_color(num):
	if num == 1:
		return(pygame.Color(0, 0, 175))
	elif num == 2:
		return(pygame.Color(0, 150, 0))
	elif num == 3:
		return(pygame.Color(200, 0, 0))
	elif num == 4:
		return(pygame.Color(100, 43, 200))
	elif num == 5:
		return(pygame.Color(100, 10, 2))
	elif num == 6:
		return(pygame.Color(64, 200, 200))
	elif num == 7:
		return(pygame.Color(0, 0, 0))
	elif num == 8:
		return(pygame.Color(50, 50, 50))

def draw_cubie(color, x_pos, y_pos, width, height, edge, press = 'out'):
	red, green, blue = color

	rp = red + 50
	if rp > 255:
		rp = 255
	gp = green + 50
	if gp > 255:
		gp = 255
	bp = blue + 50
	if bp > 255:
		bp = 255

	rn = red - 50
	if rn < 0:
		rn = 0
	gn = green - 50
	if gn < 0:
		gn = 0
	bn = blue - 50
	if bn < 0:
		bn = 0

	if press == 'out':
		color_one = pygame.Color(rp, gp, bp)
		color_two = pygame.Color(rn, gn, bn)
	else:
		color_one = pygame.Color(rn, gn, bn)
		color_two = pygame.Color(rp, gp, bp)

	pygame.draw.polygon(minesweeper.window, color_one, [[x_pos, y_pos],
														[x_pos + edge, y_pos + edge],
														[x_pos - edge + width, y_pos + edge],
														[x_pos + width - 1, y_pos]])

	pygame.draw.polygon(minesweeper.window, color_two, [[x_pos, y_pos + height - 1],
														[x_pos + edge, y_pos - edge + height],
														[x_pos - edge + width, y_pos - edge + height],
														[x_pos + width - 1, y_pos + height - 1]])

	pygame.draw.polygon(minesweeper.window, color_one, [[x_pos, y_pos],
														[x_pos + edge, y_pos + edge],
														[x_pos + edge, y_pos - edge + height],
														[x_pos, y_pos + height - 1]])

	pygame.draw.polygon(minesweeper.window, color_two, [[x_pos + width - 1, y_pos],
														[x_pos - edge + width, y_pos + edge],
														[x_pos - edge + width, y_pos - edge + height],
														[x_pos + width - 1, y_pos + height - 1]])

	pygame.draw.rect(minesweeper.window, pygame.Color(red, green, blue), pygame.Rect(x_pos + edge, y_pos + edge, width - 2 * edge, height - 2 * edge))

def draw_tile(x_pos, y_pos, tile):
	red, green, blue = 175, 175, 175

	if tile.shown:
		pygame.draw.rect(minesweeper.window, pygame.Color(red - 50, green - 50, blue - 50), pygame.Rect(x_pos, y_pos, minesweeper.piece_size, minesweeper.piece_size))
		pygame.draw.rect(minesweeper.window, pygame.Color(red, green, blue), pygame.Rect(x_pos + 1, y_pos + 1, minesweeper.piece_size - 2, minesweeper.piece_size - 2))
		if tile.type == 0:
			num_bombs = tile.get_surrounding_bombs()
			if num_bombs != 0:
				minesweeper.window.blit(*text_objects(minesweeper.font, str(num_bombs), get_color(num_bombs), pygame.Rect([x_pos, y_pos, minesweeper.piece_size, minesweeper.piece_size]).center))
		else:
			if minesweeper.game_over[0]:
				if minesweeper.game_over[1]:
					pygame.draw.rect(minesweeper.window, pygame.Color(0, 200, 0), pygame.Rect(x_pos + 1, y_pos + 1, minesweeper.piece_size - 2, minesweeper.piece_size - 2))
				else:
					pygame.draw.rect(minesweeper.window, pygame.Color(255, 0, 0), pygame.Rect(x_pos + 1, y_pos + 1, minesweeper.piece_size - 2, minesweeper.piece_size - 2))
			minesweeper.window.blit(minesweeper.bomb, [x_pos, y_pos])
	else:
		draw_cubie((175, 175, 175), x_pos, y_pos, minesweeper.piece_size, minesweeper.piece_size, minesweeper.edge)
		if tile.is_flag:
			minesweeper.window.blit(minesweeper.flag, [x_pos + minesweeper.edge, y_pos + minesweeper.edge])

def game_over(status = 'lose'):
	global board
	global minesweeper

	minesweeper.game_over[0] = True

	if status == 'win':
		minesweeper.game_over[1] = True

	for y in range(minesweeper.board_height):
		for x in range(minesweeper.board_width):
			if board[y][x].type == 1: board[y][x].shown = True

	display()
	display_clock_score()

	pygame.draw.rect(minesweeper.window, pygame.Color(150, 150, 150), pygame.Rect(minesweeper.width / 2 - 170, minesweeper.height / 2 - 60, 340, 120))

	text = pygame.font.SysFont('Arial', 30).render('Game Over! You ' + status, True, pygame.Color(0, 0, 0))
	text_rect = text.get_rect(center = (minesweeper.width / 2, minesweeper.height / 2 - 25))

	text_2 = pygame.font.SysFont('Arial', 25).render("Press 'Enter' to continue", True, pygame.Color(0, 0, 0))
	text_rect_2 = text_2.get_rect(center = (minesweeper.width / 2, minesweeper.height / 2 + 20))

	minesweeper.window.blit(text, text_rect)
	minesweeper.window.blit(text_2, text_rect_2)

	pygame.display.flip()

	end_screen = True

	while end_screen:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over_final()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					end_screen = False

	minesweeper = Minesweeper()

	board = [[Tile(x, y) for x in range(minesweeper.board_width)] for y in range(minesweeper.board_height)]

	start()

def get_open_tiles(y, x):
	for row, col in [[-1, -1],
					 [ 0, -1],
					 [ 1, -1],
					 [-1,  0],
					 [ 1,  0],
					 [-1,  1],
					 [ 0,  1],
					 [ 1,  1]]:
		if x + col < 0:
			pass
		elif x + col > minesweeper.board_width - 1:
			pass
		elif y + row < 0:
			pass
		elif y + row > minesweeper.board_height - 1:
			pass
		else:
			if [y + row, x + col] not in minesweeper.coordinates:
				if board[y + row][x + col].get_surrounding_bombs() == 0:
					minesweeper.coordinates.append([y + row, x + col])
					get_open_tiles(y + row, x + col)
				else:
					if board[y + row][x + col].type != 1:
						minesweeper.coordinates.append([y + row, x + col])

	return(minesweeper.coordinates)

def click_piece(event):
	global board

	x, y = event.pos
	x = int(x / minesweeper.piece_size)
	y = int((y - int(minesweeper.height / 7)) / minesweeper.piece_size)
	if y >= 0:
		if not minesweeper.clicked_yet:
			board = get_new_board([[x - 1, y - 1],
								   [x, y - 1],
								   [x + 1, y - 1],
								   [x - 1, y],
								   [x, y],
								   [x + 1, y],
								   [x - 1, y + 1],
								   [x, y + 1],
								   [x + 1, y + 1]])
			minesweeper.start_time = time.time()
			minesweeper.clicked_yet = True
		if event.button == 1:
			if not board[y][x].is_flag:
				if board[y][x].type == 1:
					board[y][x].shown = True
					game_over()
				else:
					if board[y][x].get_surrounding_bombs() != 0:
						board[y][x].shown = True
					else:
						minesweeper.coordinates = [[y, x]]
						for y, x in get_open_tiles(y, x):
							board[y][x].shown = True
		elif event.button == 3:
			if not board[y][x].shown:
				if not board[y][x].is_flag:
					board[y][x].is_flag = True
					minesweeper.flag_count += 1
				else:
					board[y][x].is_flag = False
					minesweeper.flag_count -= 1

		win = True

		for y in range(minesweeper.board_height):
			for x in range(minesweeper.board_width):
				if board[y][x].type == 0 and not board[y][x].shown:
					win = False

		if win:
			game_over(status='win')

		display()
		display_clock_score()

def display():
	for y in range(minesweeper.board_height):
		for x in range(minesweeper.board_width):
			draw_tile(x * minesweeper.piece_size, y * minesweeper.piece_size + int(minesweeper.height / 7), board[y][x])

	pygame.display.flip()

def display_clock_score():
	pygame.draw.rect(minesweeper.window, pygame.Color(175, 175, 175), pygame.Rect(0, 0, minesweeper.width, int(minesweeper.height / 7)))
	draw_cubie((175, 175, 175), int(minesweeper.edge * 1.5), int(minesweeper.edge * 1.5), minesweeper.width - 2 * int(minesweeper.edge * 1.5), int(minesweeper.height / 7) - 2 * int(minesweeper.edge * 1.5), int(minesweeper.edge * 1.5), press = 'in')
	minesweeper.window.blit(*text_objects(pygame.font.SysFont('Arial', int(minesweeper.piece_size * 1.5)), str(minesweeper.seconds), pygame.Color(255, 0, 0), pygame.Rect([0, 0, int(minesweeper.width / 2), int(minesweeper.height / 7)]).center))
	minesweeper.window.blit(*text_objects(pygame.font.SysFont('Arial', int(minesweeper.piece_size * 1.5)), str(minesweeper.bomb_count - minesweeper.flag_count), pygame.Color(255, 0, 0), pygame.Rect([int(minesweeper.width / 2), 0, int(minesweeper.width / 2), int(minesweeper.height / 7)]).center))

	pygame.display.flip()

def get_new_board(no_bees):
	possible_locations = []
	final_list = [[Tile(y, x) for x in range(minesweeper.board_width)] for y in range(minesweeper.board_height)]

	for y in range(minesweeper.board_height):
		for x in range(minesweeper.board_width):
			if [x, y] not in no_bees:
				possible_locations.append([x, y])

	for i in range(minesweeper.bomb_count):
		random_index = random.randint(0, len(possible_locations) - 1)
		x, y = possible_locations[random_index]
		del(possible_locations[random_index])
		final_list[y][x].type = 1

	return(final_list)

def start():
	display()
	print('test')
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over_final()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				click_piece(event)

		if minesweeper.clicked_yet and time.time() - minesweeper.start_time >= minesweeper.seconds:
			minesweeper.seconds += 1
			display_clock_score()

		minesweeper.fps.tick(30)

minesweeper = Minesweeper()

board = [[Tile(x, y) for x in range(minesweeper.board_width)] for y in range(minesweeper.board_height)]

start()
