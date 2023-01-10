import pygame
from pygame.locals import *
import time
import random

size=40
background_color=(110, 110, 5)


class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen=parent_screen
        self.x=size*3
        self.y=size*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*size
        self.y = random.randint(0,14)*size


class Snake:
    def __init__(self,parent_screen,lenght):
        self.length=lenght
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*lenght
        self.y = [size]*lenght
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction='right'

    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= 40

        if self.direction == 'right':
            self.x[0] += 40
        
        if self.direction == 'up':
            self.y[0] -= 40
        
        if self.direction == 'down':
            self.y[0] += 40

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
#####
        with open ("highscore.txt","r") as f:
            self.highscore = f.read()

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+size:
            if y1>=y2 and y1<y2+size:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources\\bg_music_1.mp3")
        pygame.mixer.music.play()
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources\\{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    
    def render_background(self):
        bg = pygame.image.load("resources\\background.jpg")
        self.surface.blit(bg,(0,0))
    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()


        for i in range(2,self.snake.length):
           if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
               self.play_sound("crash")
               raise "Collision Occured"


        if not (0<=self.snake.x[0]<=1000 and 0<=self.snake.y[0]<=600):
            self.play_sound("crash")
            raise "Collision Occured"
            
    def show_game_over(self):
        
        self.render_background()

        



        font = pygame.font.SysFont('arial',30)
        self.score=self.snake.length
        line1 =  font.render(f"Game is Over! Your score is {self.snake.length}",True,(225,225,225))
        self.surface.blit(line1,(200,300))
        line2 =  font.render(f"To play again press ENTER.To exit press ESC ",True,(225,225,225))
        self.surface.blit(line2,(200,350))
#####
        if self.score>int(self.highscore):
            self.highscore = self.score
        with open ("highscore.txt","w") as f:
            f.write(str(self.highscore))

        pygame.display.flip()
        pygame.mixer.music.pause()

        
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score=font.render(f"Score: {self.snake.length}",True,(225,225,225))

        font2 = pygame.font.SysFont('arial',30)
        hs=font2.render(f"High Score: {self.highscore}",True,(225,225,225))


        self.surface.blit(score,(800,10))
        self.surface.blit(hs,(800,40))


        

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple=Apple(self.surface)


    def run(self):
        running = True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False 
                    if not pause:
                        if event.key == K_a:
                            self.snake.move_left()
    
                        if event.key == K_d:
                            self.snake.move_right()
    
                        if event.key == K_w:
                            self.snake.move_up()
    
                        if event.key == K_s:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
            time.sleep(0.15)

if __name__ == '__main__':
    game = Game()
    game.run()

