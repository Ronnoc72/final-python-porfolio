# --- Connor Paxman ---
# Chess
# P.4/5
# imports
import pygame
from pygame.locals import *
from os import path
import random
from colors import Colors
from settings import *
from sprites import *
import time


class Game:
	"""The main game"""
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		pygame.display.set_caption(TITLE)
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.running = True
		self.player_turn = False

	def new(self):
		"""makes new grid and sprite groups"""
		self.mouse = Mouse((0, 0))
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.active_moves = pygame.sprite.LayeredUpdates()
		self.check_moves = pygame.sprite.Group()
		self.grid = Grid()
		self.pieces = pygame.sprite.LayeredUpdates()
		self.checks = False
		self.checkmate = False
		main_dir = path.dirname(__file__)
		img_dir = path.join(main_dir, "images")
		self.sprite_sheet = Spritesheet(path.join(img_dir, SPRITESHEET))
		self.load_images()
		index = 0
		turn_index = 0
		# creates all the pieces that are placed onto the board.
		for x in range(8):
			for y in range(8):
				if x * y > 20:
					turn_index = 1
					self.player_turn = True
				if self.grid.board[index] != 'o':
					Piece(self, x, y, self.grid.board[index], 0, self.player_turn, self.images[self.grid.board[index]+self.turn[turn_index]], self.turn[turn_index])
				index += 1

	def load_images(self):
		"""loads all the images that are used (from the sprite sheet)"""
		self.images = {}
		self.turn = ['b', 'w']
		for i in range(2):
			for j in range(6):
				img = self.sprite_sheet.get_image(j*175, i*187, 175, 187).convert()
				img.set_colorkey(Colors.WHITE)
				self.images[self.grid.piece_labels[j]+self.turn[i]] = img

	def run(self):
		"""game loop"""
		self.playing = True
		while self.playing:
			self.events()
			self.update()
			self.render()

	def events(self):
		"""event loop that controls the piece movement."""
		for event in pygame.event.get():
			if event.type == QUIT:
				self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.playing = False
					self.running = False
			if event.type == MOUSEBUTTONDOWN:
				# sets the active piece that the current player clicks on.
				hits = pygame.sprite.spritecollide(self.mouse, self.pieces, False)
				if hits and hits[0].player == self.player_turn:
					hits[0].set_active(True)
			if event.type == MOUSEBUTTONUP:
				hits = pygame.sprite.spritecollide(self.mouse, self.active_moves, False)
				if hits:
					for p in self.pieces:
						if p.active:
							previous_move = p
							# controls whether the user takes or moves a piece.
							self.pieces.remove(p)
							name = p.type
							new_rook = None
							old_rook = None
							# if the king is castling.
							if name == 'k':
								if abs(p.center[0]-hits[0].center[0]) > 1:
									if p.rook and not p.rook.moved:
										# determining where the rook is located due to what player is playing.
										if p.player:
											# placing the rook at an exact position, due to castling being very situational.
											if p.side:
												new_rook = Piece(self, 7, 5, 'r', 1, self.player_turn, p.rook.image, p.color)
											else:
												new_rook = Piece(self, 7, 2, 'r', 1, self.player_turn, p.rook.image, p.color)
										else:
											if p.side:
												new_rook = Piece(self, 0, 5, 'r', 1, self.player_turn, p.rook.image, p.color)
											else:
												new_rook = Piece(self, 0, 2, 'r', 1, self.player_turn, p.rook.image, p.color)
										old_rook = p.rook
										p.rook.kill()
							# creating the new piece that will be added on the board.
							new_piece = Piece(self, hits[0].center[1], hits[0].center[0], name, 1, self.player_turn, p.image, p.color)
							p.kill()
							destroyed_piece = None
							for i in self.pieces:
								if i.rect.colliderect(new_piece) and i.player != self.player_turn:
									destroyed_piece = i
									i.kill()
							# controls if the king is in check.
							self.check_for_checks()
							if self.checks:
								if destroyed_piece:
									self.pieces.add(destroyed_piece)
									self.all_sprites.add(destroyed_piece)
								if new_rook and old_rook:
									self.pieces.add(old_rook)
									self.all_sprites.add(old_rook)
									new_rook.kill()
								new_piece.kill()
								self.pieces.add(previous_move)
								self.all_sprites.add(previous_move)
								return
							# flips the grid for the other player and changes the turn of the player.
							self.grid.change_movement()
							self.player_turn = not self.player_turn
				# resets all the pieces on the board
				for p in self.pieces:
					p.set_active(False)
				# resets the available moves when the player takes a piece or moves it.
				for move in self.active_moves:
					move.kill()

	def render(self):
		"""displays all of the sprites on the screen."""
		self.screen.fill(Colors.WHITE)
		self.grid.draw_grid(self.screen)
		self.all_sprites.draw(self.screen)
		pygame.display.update()

	def update(self):
		"""updates the game and all the sprites."""
		if self.checkmate:
			return
		self.mouse.rect.center = pygame.mouse.get_pos()
		self.all_sprites.update()
		self.clock.tick(FPS)

	def check_for_checks(self):
		"""finds the checks to the king with going through all the available moves in every piece.
		if there is a collision with any of those pieces to the king either player one or two is in check."""
		king = None
		for item in self.pieces:
			if item.type == 'k' and item.player == self.player_turn:
				king = item
		for item in self.pieces:
			item.show_moves()
			for sprite in self.active_moves:
				if sprite.rect.colliderect(king.rect) and sprite.type != 'k':
					self.checks = True
					return
			for move in self.active_moves:
				move.kill()
			# resetting the checks if there are no collisions.
			self.checks = False


# creating the main game object
game = Game()
while game.running:
	game.new()
	game.run()

pygame.quit()
