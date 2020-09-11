import pygame as pg

white = (255, 255, 255)
brown = (112, 72, 60)
black = (0, 0, 0)


class Player:
    def __init__(self, side, cols, rows):
        self.x = cols//2
        self.y = {True: 0, False: rows-1}[side == True]
        self.side = side
        # [[(1,0),'V'],[(3,2), 'H']] ##max = 20 ##(x,y),side H/V
        self.fences = []

    def get_coord(self, screen, col_w, row_h):
        X, Y = int(((self.x+1)*col_w)-col_w/2), int(((self.y+1)*row_h)-row_h/2)
        return (X, Y)

    def get_col_row(self):
        return (self.x, self.y)

    def place_item(self, item, f, rows, cols):
        if f == True:
            side = {True: 'H', False: 'V'}[item.w > item.h]
            pos = ((item.left//cols)+{True: 0, False: 1}
                   [side == 'H'], (item.top//rows)+{True: 0, False: 1}[side == 'V'])
            self.fences.append([pos, side])
        # f == false???
        return


class Board:
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.w, self.h = pg.display.get_surface().get_size()
        self.w /= cols
        self.h /= rows
        self.p1 = Player(False, cols, rows)
        self.p2 = Player(True, cols, rows)
        self.p1.fences.append([(4, 5), 'V'])
        self.mouse_rect = pg.Rect(0, 0, 0, 0)
        self.mouse_fence = pg.Rect(0, 0, 0, 0)
        self.placing_fence = False

    def mouse_shadow(self, screen, pos):
        col, row = pos[0]//self.w, pos[1]//self.h
        p = 10
        self.mouse_rect = pg.Rect(
            col*self.w+p, row*self.h+p, self.w-p*2, self.h-p*2)
        hitbox = pg.Rect(pos[0], pos[1], 1, 1)

        if self.mouse_rect.contains(hitbox) and (col, row) != self.p1.get_col_row() and (col, row) != self.p2.get_col_row():
            pg.draw.rect(screen, (10, 10, 10), self.mouse_rect)
            self.placing_fence = False
        else:
            if pos[1] < self.mouse_rect.top:  # up
                self.mouse_fence = pg.Rect(
                    col*self.w, row*self.h-p, self.w*2, p*2)
            elif pos[1] < self.mouse_rect.bottom:  # down
                self.mouse_fence = pg.Rect(
                    col*self.w, (row+1)*self.h-p, self.w*2, p*2)
            elif pos[0] < self.mouse_rect.right:  # right
                self.mouse_fence = pg.Rect(
                    col*self.w-p, row*self.h, p*2, self.h*2)
            elif pos[0] > self.mouse_rect.left:  # left
                self.mouse_fence = pg.Rect(
                    (col+1)*self.w-p, row*self.h, p*2, self.h*2)
            pg.draw.rect(screen, (10, 10, 10), self.mouse_fence)
            self.placing_fence = True
        return

    def click(self):
        # turn
        if self.placing_fence == True:
            self.p1.place_item(self.mouse_fence, True, self.h, self.w)

    def update_players(self, screen, w, h):
        # draw pawns
        pg.draw.circle(screen, (252, 186,  3),
                       self.p1.get_coord(screen, w, h), int(w/2) - 5)
        pg.draw.circle(screen, (26, 112, 240),
                       self.p2.get_coord(screen, w, h), int(w/2) - 5)
        # draw fences
        f1, f2 = self.p1.fences, self.p2.fences
        for i in range(max(len(f1), len(f2))):
            if i < len(f1):  # p1
                x, y = f1[i][0]
                d = f1[i][1]
                l_w, l_h = {True: w*2, False: 10}[d == 'H'], {True: h*2, False: 10}[d == 'V']

                if d == 'H': pg.draw.rect(screen, black, (x*w, y*h - 5, l_w, l_h))
                if d == 'V': pg.draw.rect(screen, black, (x*w - 5, y*h, l_w, l_h))
            if i < len(f2):  # p2
                x, y = f2[i][0]
                d = f2[i][1]
                l_w, l_h = {True: w*2, False: 3}[d ==
                                                 'H'], {True: h*2, False: 3}[d == 'V']
                pg.draw.rect(screen, black, (x*w, y*h, l_w, l_h))

    def draw_board(self, screen, w, h, p):
        # rectangles
        for i in range(self.rows):
            for j in range(self.cols):
                pg.draw.rect(screen, white, (i*w, j*h, w, h))
                pg.draw.rect(screen, brown, (i*w+p, j*h+p, w-p*2, h-p*2))

    def update_board(self, screen):
        w, h, p = self.w, self.h, 1
        self.draw_board(screen, w, h, p)
        self.update_players(screen, w, h)
