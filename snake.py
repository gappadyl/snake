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
	
	def move(self, time_difference):
		time_difference = int(time_difference)
		head_position = self.position	
		self.position[0] += time_difference * self.velocity[0]
		self.position[1] += time_difference * self.velocity[1]
	
		num_segments = len(self.body)
		for i in range(num_segments - 1, 0, -1):	
			if int(self.body[i - 1].left / 30) == int(self.body[i].left / 30) and math.ceil(self.body[i - 1].left / 30) == math.ceil(self.body[i].left / 30):
				if self.body[i - 1].top > self.body[i].top:	
					self.body[i].move_ip(0, time_difference * 1)
				elif self.body[i - 1].top < self.body[i].top: 
					self.body[i].move_ip(0, time_difference * -1)	
			else:
				if self.body[i - 1].left > self.body[i].left:
					self.body[i].move_ip(time_difference * 1, 0)
				elif self.body[i - 1].left < self.body[i].left: 
					self.body[i].move_ip(time_difference * -1, 0)	
		
		self.body[0].move_ip(time_difference * self.velocity[0], time_difference * self.velocity[1])
	
	def update_direction(self, direction):
		if self.direction + direction == 1 or self.direction + direction == 5:
			return
	
		self.direction = direction

def current_milli_time():
	return round(time.time() * 1000)

def main():
	pygame.init()
	screen = pygame.display.set_mode(size=(600,600))
	game_bounds = pygame.Rect(0, 0, 600, 600)	
	snake = Snake()
	game = Game()
	update_rate = 3 

	last_tick = current_milli_time() 
	direction_queue = []	
	while 1:
		current_tick = current_milli_time()
		pressed_keys = pygame.key.get_pressed()

		if snake.body[0].colliderect(game.apple_rect):
			game.points += 1	
			game.reset_apple()
		
		if not game_bounds.contains(snake.body[0]):
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
			
			snake.move((current_tick - last_tick) / update_rate)
			last_tick = current_milli_time()
		screen.fill((0,0,0))
		for segment in snake.body:	
			pygame.draw.rect(screen, (255, 255, 255), segment)
		pygame.draw.rect(screen, (255, 0, 0), game.apple_rect)	
		pygame.display.flip()
             


if __name__=="__main__":
	main()
