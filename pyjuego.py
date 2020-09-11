import pygame as pg
import game

W, H = 800, 800
screen = pg.display.set_mode((W, H))
pg.display.set_caption('game')
over = False
board = game.Board(10, 10, screen)
while not over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            over = True
        if event.type == pg.MOUSEBUTTONDOWN:
            board.click()
    board.update_board(screen)
    board.mouse_shadow(screen, pg.mouse.get_pos())
    pg.display.update()
