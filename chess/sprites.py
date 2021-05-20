# Sprite for chess game.

import pygame
from pygame.locals import *
import random
from colors import Colors
from settings import *


class Spritesheet:
	"""Loads in a spritesheet that is used for the art."""
	def __init__(self, filename):
		self.spritesheet = pygame.image.load(filename).convert()

	def get_image(self, x, y, width, height):
		"""Extracts a certain image on a sprite sheet with coordinates and size."""
		image = pygame.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pygame.transform.scale(image, (width//2, height//2))
		return image


class Mouse(pygame.sprite.Sprite):
	"""The mouse sprite that is used for collisions."""
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((2, 2))
		self.rect = self.image.get_rect()
		self.rect.center = center


class ActiveMove(pygame.sprite.Sprite):
	"""A sprite that shows all of the active moves of each piece."""
	def __init__(self, game, x, y, player, name):
		self._layer = ACTIVE_MOVE_LAYER
		self.groups = game.all_sprites, game.active_moves
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
		self.image.fill(Colors.RED)
		self.rect = self.image.get_rect()
		self.center = (x, y)
		# adjusting the sprite to grid.
		self.rect.x = x * TILE_SIZE
		self.rect.y = y * TILE_SIZE
		self.player = player
		self.type = name


class Grid:
	"""The main grid that stores the movement of all the pieces."""
	def __init__(self):
		self.move_database = {
			"p": [[0, -1], [0, -2]],
			"b": [[-1, 1], [1, -1], [-1, -1], [1, 1]],
			"n": [[-1, -2], [1, -2], [-2, -1], [2, -1], [-2, 1], [2, 1], [-1, 2], [1, 2]],
			"r": [[1, 0], [-1, 0], [0, -1], [0, 1]],
			"k": [[1, -1], [1, 0], [-1, 0], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 1]],
			"q": [[1, 0], [-1, 0], [0, -1], [0, 1], [-1, 1], [1, -1], [-1, -1], [1, 1]]
		}
		self.indexs = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
					   'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
		self.piece_labels = ['k', 'q', 'r', 'b', 'n', 'p']
		self.board = []
		for i in range(64):
			self.board.append('o')
		for i in range(len(self.indexs)):
			self.board[i] = self.indexs[i]
			self.board[-16 + i] = self.indexs[-i - 1]
		self.board[-5], self.board[-4] = self.board[-4], self.board[-5]

	def draw_grid(self, surf):
		"""displays the grid on screen (or a pygame surface)."""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(surf, Colors.BROWN, pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2))

	def change_movement(self):
		"""flips the movement database so the other player can have the correct movement."""
		for moves in self.move_database:
			for move in moves:
				for p in self.move_database[move]:
					p[0] *= -1
					p[1] *= -1


class Piece(pygame.sprite.Sprite):
	"""The game pieces that shows its moves."""
	def __init__(self, game, x, y, name, has_moved, player, image, color):
		self._layer = PIECE_LAYER
		self.groups = game.all_sprites, game.pieces
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.database = self.game.grid.move_database
		self.board = self.game.grid.board
		self.image = image
		self.image = pygame.transform.scale(self.image, (TILE_SIZE//2, TILE_SIZE//2))
		self.rect = self.image.get_rect()
		self.center = (y, x)
		# adjusting the sprite to grid.
		self.rect.center = (y * TILE_SIZE + self.rect.width, x * TILE_SIZE + self.rect.width)
		# getting the main types of the sprite. (used for pawns, knights and the king).
		self.type = name
		self.moved = has_moved
		self.active = False
		self.player = player
		self.color = color
		# only for kings in castling.
		self.rook = None
		self.side = None

	def set_active(self, value):
		self.active = value

	def show_moves(self, special_case=False):
		"""Shows all the moves that the piece can do relative to all the other pieces.
		Also controlling the movement of the pieces with different cases as well."""
		# if the piece is a pawn, it has special movement.
		if self.type == 'p':
			moves = self.database[self.type]
			for move in moves:
				for i in range(-self.moved+2):
					a = ActiveMove(self.game, ((move[0]*(i+1))+self.center[0]), ((move[1]*(i+1))+self.center[1]), self.player, self.type)
					hits = pygame.sprite.spritecollide(a, self.game.pieces, False)
					if hits:
						a.kill()
				for i in range(2):
					a = ActiveMove(self.game, (((i-1)+i)+self.center[0]), (self.center[1]+move[1]), self.player, self.type)
					attack_hits = pygame.sprite.spritecollide(a, self.game.pieces, False)
					for attack in attack_hits:
						if attack.player == self.player:
							a.kill()
					if not attack_hits:
						a.kill()
				break
		# if the piece is a king or a knight
		elif self.type == 'k' or self.type == 'n':
			moves = self.database[self.type]
			for move in moves:
				a = ActiveMove(self.game, ((move[0])+self.center[0]), ((move[1])+self.center[1]), self.player, self.type)
				hits = pygame.sprite.spritecollide(a, self.game.pieces, False)
				if hits:
					for hit in hits:
						if hit.player == self.player:
							a.kill()
			if self.moved == 0 and self.type == 'k':
				# controls the castling of the king and rook.
				castle = [0, 7]
				for i in range(len(castle)):
					a = ActiveMove(self.game, castle[i], self.center[1], self.player, self.type)
					hits = pygame.sprite.spritecollide(a, self.game.pieces, False)
					if hits:
						self.rook = hits[0]
						self.side = castle[i]
				if not self.side:
					for i in range(4):
						ActiveMove(self.game, (-i+self.center[0]), (self.center[1]), self.player, self.type)
				else:
					for i in range(3):
						ActiveMove(self.game, (i+self.center[0]), (self.center[1]), self.player, self.type)
				pygame.sprite.groupcollide(self.game.pieces, self.game.active_moves, False, True)
			return
		else:
			moves = self.database[self.type]
			for move in moves:
				mult = 0
				while True:
					# creating the active move object.
					a = ActiveMove(self.game, ((move[0]*(mult+1))+self.center[0]), ((move[1]*(mult+1))+self.center[1]), self.player, self.type)
					# if the piece collides with any of the other pieces.
					hits = pygame.sprite.spritecollide(a, self.game.pieces, False)
					for hit in hits:
						if hit.player == self.player:
							a.kill()
					if hits or mult >= 9:
						break
					mult += 1

	def update(self):
		# if the pawn makes it the end of the board.
		if self.type == 'p':
			if self.player:
				if self.center[1] == 0:
					self.type = 'q'
					self.image = self.game.images[self.type + self.color]
			else:
				if self.center[1] == 7:
					self.type = 'q'
					self.image = self.game.images[self.type + self.color]
		if self.active and len(self.game.active_moves) < 100:
			self.show_moves()
		# updates the piece if the user has clicked on it.
		if self.active:
			self.rect.x = self.center[0] * TILE_SIZE
			self.rect.y = self.center[1] * TILE_SIZE
			self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
		else:
			self.rect.center = (self.center[0] * TILE_SIZE + self.rect.width, self.center[1] * TILE_SIZE + self.rect.width)
			self.image = pygame.transform.scale(self.image, (TILE_SIZE // 2, TILE_SIZE // 2))


if __name__ == "__main__":
	print(__file__, "isn't meant to be run")
