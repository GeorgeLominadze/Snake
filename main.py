import pygame
from pygame.locals import *
import time
import random
import sys

from pygame import mixer


SIZE = 40
BACKGROUND_COLOR = (29, 245, 255)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
MAX_BLOCKS = (WINDOW_WIDTH // SIZE) * (WINDOW_HEIGHT // SIZE)


pygame.mixer.init()
bg = pygame.mixer.music.load('bg_music_1.mp3')
pygame.mixer.music.play(-1)
music = pygame.mixer.Sound('ding.mp3')
crash = pygame.mixer.Sound('crash.mp3')


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(
            r"C:\Users\leon\Desktop\Snake\apple.jpg").convert()

        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):

        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self, snake):
        # Snake positions to prevent overlapping
        snake_positions = list(zip(snake.x, snake.y))
        while True:

            self.x = random.randint(0, 24)*SIZE
            self.y = random.randint(0, 19)*SIZE
            if (self.x, self.y) not in snake_positions:
                break


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            r"C:\Users\leon\Desktop\Snake\block.jpg").convert()

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        game.score += 1

    def draw(self):
        self.parent_screen.fill((BACKGROUND_COLOR))
        for i in range(self.length):

            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
            self.draw()

        if self.direction == 'down':
            self.y[0] += SIZE
            self.draw()

        if self.direction == 'left':
            self.x[0] -= SIZE
            self.draw()

        if self.direction == 'right':
            self.x[0] += SIZE
            self.draw()

    def check_collision_with_self(self):
        if (self.x[0], self.y[0]) in zip(self.x[1:], self.y[1:]):
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.score = 0

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((29, 245, 255))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2=None, y2=None):
        if x2 is None and y2 is None:
            if x1 < 0 or x1 >= WINDOW_WIDTH or y1 < 0 or y1 >= WINDOW_HEIGHT:
                return True
        else:
            if x1 >= x2 and x1 < x2 + SIZE:
                if y1 >= y2 and y1 < y2+SIZE:
                    return True
        return False

    def play(self):

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.snake.check_collision_with_self():
            pygame.mixer.music.pause()  # Pause the background music
            crash.play()  # Play the crash sound effect
            pygame.time.delay(1000)  # Delay for 1 second
            pygame.mixer.music.unpause()
            raise Exception('Game Over')

        # collision with an apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            pygame.mixer.music.pause()
            music.play()
            # pygame.time.delay(200)
            pygame.mixer.music.unpause()

            self.snake.increase_length()
            self.apple.move(self.snake)

            if self.score >= MAX_BLOCKS:

                self.show_game_over('You Win')  # Display winning message
                pause = True
                self.reset()

        # Collision with walls
        if self.is_collision(self.snake.x[0], self.snake.y[0]):
            pygame.mixer.music.pause()  # Pause the background music
            crash.play()  # Play the crash sound effect
            pygame.time.delay(1000)  # Delay for 1 second
            pygame.mixer.music.unpause()
            raise Exception('Game Over')

        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):

                raise 'Game Over'

    def display_score(self):
        font = pygame.font.SysFont('sans-serif', 30)
        score = font.render(
            f'Score:{self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('sans-serif', 30)

        message1 = font.render(
            f'Game over!Your score is:{self.snake.length}', True, (255, 255, 255))
        self.surface.blit(message1, (400, 400))
        message2 = font.render(
            f'To play again press Enter! To exit press Escape!', True, (255, 255, 255))

        if self.score >= MAX_BLOCKS:
            message3 = font.render(
                f'Congratulations!', True, (255, 255, 255))
            self.surface.blit(message3, (400, 480))

        self.surface.blit(message1, (400, 400))
        self.surface.blit(message2, (400, 440))

        pygame.display.flip()
        pygame.mixer.quit()
        time.sleep(2)

    def reset(self):
        self.snake = Snake(self.surface, 1)

        self.apple = Apple(self.surface)
        self.score = 0

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause == False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == pygame.QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == '__main__':
    game = Game()
    game.run()
