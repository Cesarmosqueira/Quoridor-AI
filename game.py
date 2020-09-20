from players import *
import random as rnd
class Board:
	def __init__(self, rows, cols, screen):
		self.rows = rows
		self.cols = cols
		self.w, self.h = pg.display.get_surface().get_size()
		self.w /= cols
		self.h /= rows
		self.p1 = Player(False, cols, rows)
		self.p2 = Player(True, cols, rows)
		self.mouse_rect = pg.Rect(0, 0, 0, 0)
		self.mouse_fence = pg.Rect(0, 0, 0, 0)
		self.placing_fence = False
		self.turn = {True:-1,False:1}[rnd.randint(0,1) == 0]		
		####matrix#####
		self.backend = [[{True:'#', False:' '}[x==0 or x ==rows+1] for x in range(rows+2)]]*int(cols+2)
		a = ['#']*(cols+2)
		self.backend[0] = a; self.backend[-1] = a
		
	def update_backend(self):
		print(self.backend[int(self.p1.y+1)][int(self.p1.x+1)])
		self.backend[int(self.p1.y+1)][int(self.p1.x+1)] = '1'	
		self.backend[int(self.p2.y+1)][int(self.p2.x+1)] = '2'	
		for i in self.backend: print(i)	

	def mouse_shadow(self, screen, pos):
		col, row = pos[0]//self.w, pos[1]//self.h
		p = 10
		self.mouse_rect = pg.Rect(col*self.w+p, row*self.h+p, self.w-p*2, self.h-p*2)
		hitbox = pg.Rect(pos[0], pos[1], 1, 1)
		arr = {True: self.p1.get_adyacents(), False: self.p2.get_adyacents()}[self.turn == 1]
		if (col,row) in arr and self.mouse_rect.contains(hitbox) and (col, row) != self.p1.get_col_row() and (col, row) != self.p2.get_col_row():
			pg.draw.rect(screen, {True:Cshadow2, False:Cshadow1}[self.turn==-1], self.mouse_rect)
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
			pg.draw.rect(screen, {True:Cshadow2, False:Cshadow1}[self.turn==-1], self.mouse_fence)
			self.placing_fence = True
		return

	def click(self, pos):
		# turn
		if self.placing_fence == True:
			if self.turn == 1:
				self.p1.place_item(self.mouse_fence, True, self.h, self.w)
			if self.turn == -1:
				self.p2.place_item(self.mouse_fence, True, self.h, self.w)
			self.turn *= -1
		else:
			p = pos[0]//self.w, pos[1]//self.h
			if self.turn == 1 and p in self.p1.get_adyacents(): self.p1.move_to(p,self.p2.fences)
			if self.turn == -1 and p in self.p2.get_adyacents(): self.p2.move_to(p,self.p1.fences)
			self.turn *= -1	
		self.update_backend()	

	def update_players(self, screen, w, h):
		# draw pawns
		pg.draw.circle(screen, Cpawn1,self.p1.get_coord(screen, w, h), int(w/2) - 5)
		pg.draw.circle(screen, Cpawn2,self.p2.get_coord(screen, w, h), int(w/2) - 5)
		# draw fences
		f1, f2 = self.p1.fences, self.p2.fences
		for i in range(max(len(f1), len(f2))):
			if i < len(f1):  # p1
				x, y = f1[i][0]
				d = f1[i][1]
				l_w, l_h = {True: w*2, False: 10}[d == 'H'], {True: h*2, False: 10}[d == 'V']
				if d == 'H': pg.draw.rect(screen, Cpawn1, (x*w, y*h - 5, l_w, l_h))
				if d == 'V': pg.draw.rect(screen, Cpawn1, (x*w - 5, y*h, l_w, l_h))
			if i < len(f2):  # p2
				x, y = f2[i][0]
				d = f2[i][1]
				l_w, l_h = {True: w*2, False: 10}[d == 'H'], {True: h*2, False: 10}[d == 'V']
				if d == 'H': pg.draw.rect(screen, Cpawn2, (x*w, y*h - 5, l_w, l_h))
				if d == 'V': pg.draw.rect(screen, Cpawn2, (x*w - 5, y*h, l_w, l_h))

	def draw_board(self, screen, w, h, p):
		# rectangles
		for i in range(self.rows):
			for j in range(self.cols):
				pg.draw.rect(screen, Cwhite, (i*w, j*h, w, h))
				pg.draw.rect(screen, Cbrown, (i*w+p, j*h+p, w-p*2, h-p*2))

	def update_board(self, screen):
		w, h, p = self.w, self.h, 1
		self.draw_board(screen, w, h, p)
		self.update_players(screen, w, h)
		return self.turn


