import math
import random
import sys
import pygame
import time

class Game:
	def __init__(self):
		self.points = 0
		self.apple = self.apple_position = [30 * random.randint(0, 19), 30 * random.randint(0, 19)] 
		self.apple_rect = pygame.Rect(self.apple_position[0], self.apple_position[1], 30, 30)

	def reset_apple(self):
		self.apple_position = [30 * random.randint(0, 19), 30 * random.randint(0, 19)] 
		self.apple_rect.update(self.apple_position[0], self.apple_position[1], 30, 30)

class Snake:
	def __init__(self):
		self.length = 1
		self.size = 30
		self.direction = 0
		self.body = [pygame.Rect(300, 300, self.size, self.size)]
		self.velocity = [1, 0]

	def update_velocity(self):
		if (int(self.body[0].left) % int(self.size)) + (int(self.body[0].top) % int(self.size)) == 0:
			if self.direction == 0:
				self.velocity = [1, 0]
			elif self.direction == 1:
				self.velocity = [-1, 0]
			elif self.direction == 2:
				self.velocity = [0, -1]
			elif self.direction == 3:
				self.velocity = [0, 1]
			
			return True
		
		return False
	
	def move(self):
		num_segments = len(self.body)
		for i in range(num_segments - 1, 0, -1):	
			if self.body[i].left % self.size == 0 and self.body[i].top % self.size != 0:
				if self.body[i - 1].top > self.body[i].top:	
					self.body[i].move_ip(0, 1)
				elif self.body[i - 1].top < self.body[i].top: 
					self.body[i].move_ip(0, -1)	
			elif self.body[i].left % self.size != 0 and self.body[i].top % self.size == 0:
				if self.body[i - 1].left > self.body[i].left:
					self.body[i].move_ip(1, 0)
				elif self.body[i - 1].left < self.body[i].left: 
					self.body[i].move_ip(-1, 0)
			else:
				if self.body[i - 1].left > self.body[i].left:
					self.body[i].move_ip(1, 0)
				elif self.body[i - 1].left < self.body[i].left: 
					self.body[i].move_ip(-1, 0)
				elif self.body[i - 1].top > self.body[i].top:	
					self.body[i].move_ip(0, 1)
				elif self.body[i - 1].top < self.body[i].top: 
					self.body[i].move_ip(0, -1)	
		
		self.body[0].move_ip(self.velocity[0], self.velocity[1])
	
	def update_direction(self, direction):
		if self.direction + direction == 1 or self.direction + direction == 5:
			return
	
		self.direction = direction

	def check_body_collision(self):
		num_segments = len(self.body)
		for i in range(2, num_segments):
			if self.body[i].colliderect(self.body[0]):
				return True	
		return False

	def append_segment(self):		
		num_segments = len(self.body)
		tail = pygame.Rect.copy(self.body[num_segments - 1])	
		if num_segments < 2:	
			tail.move_ip(self.size * -self.velocity[0], self.size * -self.velocity[1])
		else:
			if self.body[num_segments - 1].left % self.size == 0 and self.body[num_segments - 1].top % self.size != 0:
				if self.body[num_segments - 2].top > self.body[num_segments - 1].top:	
					tail.move_ip(0, -self.size)
				elif self.body[num_segments - 2].top < self.body[num_segments - 1].top: 
					tail.move_ip(0, self.size)	
			elif self.body[num_segments - 1].left % self.size != 0 and self.body[num_segments - 1].top % self.size == 0:
				if self.body[num_segments - 2].left > self.body[num_segments - 1].left:
					tail.move_ip(-self.size, 0)
				elif self.body[num_segments - 2].left < self.body[num_segments - 1].left: 
					tail.move_ip(self.size, 0)
			else:
				if self.body[num_segments - 2].left > self.body[num_segments - 1].left:
					tail.move_ip(-self.size, 0)
				elif self.body[num_segments - 2].left < self.body[num_segments - 1].left: 
					tail.move_ip(self.size, 0)
				elif self.body[num_segments - 2].top > self.body[num_segments - 1].top:	
					tail.move_ip(0, -self.size)
				elif self.body[num_segments - 2].top < self.body[num_segments - 1].top: 
					tail.move_ip(0, self.size)	
					
		self.body.append(tail)	

def current_milli_time():
	return round(time.time() * 1000)

def main():
	pygame.init()
	screen = pygame.display.set_mode(size=(600,600))
	game_bounds = pygame.Rect(0, 0, 600, 600)	
	snake = Snake()
	game = Game()
	update_rate = 2 

	last_tick = current_milli_time() 
	direction_queue = []	
	while 1:
		current_tick = current_milli_time()
		pressed_keys = pygame.key.get_pressed()

		if snake.body[0].colliderect(game.apple_rect):
			game.points += 1
			game.reset_apple()
			valid_pos = False	
			while not valid_pos:	
				valid_pos = True	
				for r in snake.body:
					if r.colliderect(game.apple_rect):
						game.reset_apple()
						valid_pos = False
			snake.append_segment()
		
		if not game_bounds.contains(snake.body[0]) or snake.check_body_collision():
			snake = Snake()
			game = Game()
			last_tick = current_milli_time()
			direction_queue = []	
			continue
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN and len(direction_queue) < 2:
				if event.key == pygame.K_RIGHT:
					direction_queue.append(0)	
				elif event.key == pygame.K_LEFT:
       					direction_queue.append(1) 
				elif event.key == pygame.K_UP:
       					direction_queue.append(2) 
				elif event.key == pygame.K_DOWN:
					direction_queue.append(3)
				
		if current_tick - last_tick > update_rate:
			if len(direction_queue) > 0:
				snake.update_direction(direction_queue[0])
			
			if snake.update_velocity() and len(direction_queue) > 0:
				direction_queue.pop(0)
			
			snake.move()
			last_tick = current_milli_time()
		screen.fill((0,0,0))
		for segment in snake.body:	
			pygame.draw.rect(screen, (255, 255, 255), segment)
		pygame.draw.rect(screen, (255, 0, 0), game.apple_rect)	
		pygame.display.flip()
             


if __name__=="__main__":
	main()
