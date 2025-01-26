from collections import deque

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from snake_game import (BOARD_HEIGHT, BOARD_TILE_HEIGHT, BOARD_TILE_WIDTH,
                        BOARD_WIDTH, SnakeGame)

SNAKE_LENGTH_GOAL = 30


class SnakeEnv(gym.Env):
    def __init__(self, show_window=False, disable_input=False):
        super().__init__()
        self.game = SnakeGame(show_window=show_window,
                              disable_input=disable_input)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.MultiDiscrete(
            [SNAKE_LENGTH_GOAL] + [BOARD_WIDTH, BOARD_HEIGHT] * (SNAKE_LENGTH_GOAL + 1))

    def step(self, action):
        self.game.set_direction([(1, 0), (0, -1), (-1, 0), (0, 1)][action])
        self.game.update()

        reward = 0
        if self.game.was_apple_collision:
            reward = 50
        elif self.game.was_wall_collision or self.game.was_body_collision:
            reward = -100

        head = self.game.snake[0]
        body = self.game.snake
        food_x, food_y = self.game.food
        length = self.game.get_snake_length()
        terminated = self.game.game_over
        observation = [length, food_x, food_y]

        for i in range(SNAKE_LENGTH_GOAL):
            observation.extend(body[i] if i < length else (0, 0))

        observation = np.array(observation, dtype=np.int32).flatten()

        info = {
            "snake_length": length,
            "head_position": head,
            "food_position": self.game.food
        }

        return observation, reward, terminated, False, info

    def reset(self, seed=None, **kwargs):
        super().reset(seed=seed)
        self.game.reset(seed=seed)

        head = self.game.snake[0]
        body = self.game.snake
        food_x, food_y = self.game.food
        length = self.game.get_snake_length()
        observation = [length, food_x, food_y]

        for i in range(SNAKE_LENGTH_GOAL):
            observation.extend(body[i] if i < length else (0, 0))

        observation = np.array(observation, dtype=np.int32).flatten()

        info = {
            "snake_length": length,
            "head_position": head,
            "food_position": self.game.food
        }

        return observation, info

    def render(self):
        if self.game.show_window:
            self.game.draw()
