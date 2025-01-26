import os
import random
from typing import Tuple

import pygame

SNAKE_SECTION_WIDTH = 50
BOARD_TILE_WIDTH = BOARD_TILE_HEIGHT = 15

BOARD_WIDTH = BOARD_TILE_WIDTH * SNAKE_SECTION_WIDTH
BOARD_HEIGHT = BOARD_TILE_HEIGHT * SNAKE_SECTION_WIDTH

FPS = 8


class SnakeGame:
    def __init__(self, show_window=True, disable_input=False):
        pygame.init()

        if not show_window:
            os.environ['SDL_VIDEODRIVER'] = 'dummy'

        self.screen: pygame.Surface | None = None
        self.clock = pygame.time.Clock()
        self.snake = [(100, 100), (50, 100), (0, 100)]
        self.food = self.get_next_apple()
        self.direction = (1, 0)
        self.game_over = False
        self.show_window = show_window
        self.disable_input = disable_input or not show_window
        self.quit = False

        if show_window:
            self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
            pygame.display.set_caption("Snake Game")

    def set_direction(self, direction: Tuple[int, int]):
        predicted_head_pos = (
            self.snake[0][0] + direction[0] * SNAKE_SECTION_WIDTH,
            self.snake[0][1] + direction[1] * SNAKE_SECTION_WIDTH,
        )

        if predicted_head_pos != self.snake[1] and direction != (0, 0) and direction != (1, 1):
            self.direction = direction

    def get_snake_length(self):
        return len(self.snake)

    def get_next_apple(self):
        pos = (random.randint(0, BOARD_TILE_WIDTH - 1) * SNAKE_SECTION_WIDTH,
               random.randint(0, BOARD_TILE_HEIGHT - 1) * SNAKE_SECTION_WIDTH)

        if pos in self.snake:
            return self.get_next_apple()
        return pos

    def reset_apple(self):
        self.food = self.get_next_apple()

    def reset_snake(self):
        self.snake = [(100, 100), (50, 100), (0, 100)]
        self.direction = (1, 0)

    def apple_collision(self):
        return self.snake[0] == self.food

    def body_collision(self):
        return self.snake[0] in self.snake[1:]

    def wall_collision(self):
        return (
            self.snake[0][0] in (-SNAKE_SECTION_WIDTH, BOARD_WIDTH)
            or self.snake[0][1] in (-SNAKE_SECTION_WIDTH, BOARD_HEIGHT)
        )

    def get_next_head_pos(self):
        return (
            self.snake[0][0] + self.direction[0] * SNAKE_SECTION_WIDTH,
            self.snake[0][1] + self.direction[1] * SNAKE_SECTION_WIDTH,
        )

    def advance_snake(self):
        self.snake.insert(0, self.get_next_head_pos())

    def update(self):
        if self.show_window:
            self.clock.tick(FPS)
        else:
            self.clock.tick(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN and not self.disable_input:
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.set_direction((1, 0))
                elif event.key == pygame.K_RETURN:
                    self.reset()

        if self.game_over:
            return

        self.advance_snake()

        if self.wall_collision() or self.body_collision():
            self.game_over = True

        if self.apple_collision():
            self.reset_apple()
        else:
            self.snake.pop()

    def draw(self):
        if not self.show_window:
            return

        if self.game_over:
            self.screen.fill((255, 0, 0))

            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_x = self.screen.get_width() / 2 - text_rect.width / 2
            text_y = self.screen.get_height() / 2 - text_rect.height / 2

            self.screen.blit(text, [text_x, text_y])

        else:
            self.screen.fill((0, 0, 0))

            for pos in self.snake:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 pygame.Rect(pos[0], pos[1], SNAKE_SECTION_WIDTH, SNAKE_SECTION_WIDTH))

            pygame.draw.rect(self.screen, (255, 0, 0),
                             pygame.Rect(self.food[0], self.food[1], SNAKE_SECTION_WIDTH, SNAKE_SECTION_WIDTH))

        pygame.display.flip()

    def reset(self):
        self.game_over = False
        self.reset_snake()
        self.reset_apple()
