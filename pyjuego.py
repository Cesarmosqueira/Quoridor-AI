import time
import pygame as pg
import game
from sys import setrecursionlimit
setrecursionlimit(10**4)
W, H = 800, 800
screen = pg.display.set_mode((W, H))
pg.display.set_caption('game')
over = False
rows, cols = 9,9
board = game.Board(rows,cols, screen)
turn = board.turn
aux = 0
pg.font.init()
while not over:
        time.sleep(0.05)
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    over = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    board.click(screen)
                        
                pressed = pg.key.get_pressed()
                if pressed[pg.K_b] and aux == 0:
                    aux = 25
                    board.move_pawns()

        if turn == 10 or turn == -10:
                font = pg.font.SysFont("Arial", 32)
                ts = font.render(str("Ha ganado " + ('el Verde' \
                        if turn == 10 \
                        else 'el Azul')+"\n[Space] Cerrar [R] Reset"), False, (255,0,0))
                board.mouse_shadow(screen, (-1,-1))
                center = [(H/rows)*(rows/2), (W/cols)*(cols/2)]
                center[1] -= ts.get_width()/2
                screen.blit(ts,center)
                pg.display.update()
                flag = False
                while True:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            over = True
                            quit()
                        pressed = pg.key.get_pressed()
                        if pressed[pg.K_SPACE]:
                            over = True
                            quit()
                        if pressed[pg.K_r]:
                            input("u pressed r")

                            over = False
                            board = game.Board(rows,cols,screen)
                            turn = board.turn
                            flag = True
                            break

                if flag: 
                    print("passing")
                    pass
                raise Exception("wtf")
        
        turn = board.update_board(screen) ##main func
        board.mouse_shadow(screen, pg.mouse.get_pos())
        pg.display.update()
        if aux > 0: aux -= 1
