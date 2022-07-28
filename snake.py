import keyboard
import pygame
import time

class Game:
    def __init__(self):
        self.points = 0 

class Snake:
    def __init__(self):
        self.length = 1
        self.position = [300, 300]
        self.direction = 0
        self.isAlive = True

def current_milli_time():
    return round(time.time() * 1000)

def main():
    pygame.init()
    screen = pygame.display.set_mode(size=(600,600))
    snake = Snake()
    game = Game()
    

    current_tick = current_milli_time() 
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if keyboard.is_pressed('right'):
            snake.direction = 0
        elif keyboard.is_pressed('left'):
            snake.direction = 1
        elif keyboard.is_pressed('up'):
            snake.direction = 2
        elif keyboard.is_pressed('down'):
            snake.direction = 3

        if current_milli_time() - current_tick > 75:
            current_tick = current_milli_time()
            if snake.direction == 0:
                 snake.position[0] += 15
            elif snake.direction == 1:
                 snake.position[0] -= 15
            elif snake.direction == 2:
                 snake.position[1] -= 15
            elif snake.direction == 3:
                 snake.position[1] += 15
        
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(snake.position[0], snake.position[1], 15, 15))
        pygame.display.flip()
             


if __name__=="__main__":
    main()
