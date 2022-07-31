import sys
import pygame
import time

class Game:
    def __init__(self):
        self.points = 0 

class Snake:
	def __init__(self, size):
		self.length = 1
		self.position = [300, 300]
		self.size = size
		self.direction = 0
		self.isAlive = True
		self.rect = pygame.Rect(self.position[0], self.position[1], size, size)
		self.velocity = [1, 0]

	def update_velocity(self):
		print(self.position)	
		if (int(self.position[0]) % int(self.size)) + (int(self.position[1]) % int(self.size)) == 0:
			if self.direction == 0:
				self.velocity = [1, 0]
			elif self.direction == 1:
				self.velocity = [-1, 0]
			elif self.direction == 2:
				self.velocity = [0, -1]
			elif self.direction == 3:
				self.velocity = [0, 1]

	def move(self, time_difference):
		time_difference = int(time_difference)
		self.position[0] += time_difference * self.velocity[0]
		self.position[1] += time_difference * self.velocity[1]
		self.rect.move_ip(time_difference * self.velocity[0], time_difference * self.velocity[1])

	def update_direction(self, direction):
		if self.direction + direction == 1 or self.direction + direction == 5:
			return
	
		self.direction = direction 

def current_milli_time():
	return round(time.time() * 1000)

def main():
	pygame.init()
	screen = pygame.display.set_mode(size=(600,600))
	snake = Snake(size=30)
	game = Game
	update_rate = 3 

	last_tick = current_milli_time() 
	direction = 0	
	while 1:
		current_tick = current_milli_time()
		pressed_keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		if pressed_keys[pygame.K_RIGHT]:
			direction = 0	
		elif pressed_keys[pygame.K_LEFT]:
       			direction = 1 
		elif pressed_keys[pygame.K_UP]:
       			direction = 2 
		elif pressed_keys[pygame.K_DOWN]:
			direction = 3
		
		snake.update_direction(direction)	
		snake.update_velocity()
		if current_tick - last_tick > update_rate:
			snake.move((current_tick - last_tick) / update_rate)
			last_tick = current_milli_time()
		
		screen.fill((0,0,0))
		pygame.draw.rect(screen, (255, 255, 255), snake.rect)
		pygame.display.flip()
             


if __name__=="__main__":
	main()
