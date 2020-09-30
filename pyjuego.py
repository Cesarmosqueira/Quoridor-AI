import pygame as pg
import game
from sys import setrecursionlimit
setrecursionlimit(10**4)
W, H = 800, 800
screen = pg.display.set_mode((W, H))
pg.display.set_caption('game')
over = False
board = game.Board(9,9, screen)
turn = board.turn
aux = 0
while not over:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			over = True
		if event.type == pg.MOUSEBUTTONDOWN:
			board.click(screen)
		pressed = pg.key.get_pressed()
		if pressed[pg.K_b] and aux == 0:
			aux = 100
			board.move_pawns()


	turn = board.update_board(screen) ##main func
	board.mouse_shadow(screen, pg.mouse.get_pos())
	pg.display.update()
	if aux > 0: aux -= 1
