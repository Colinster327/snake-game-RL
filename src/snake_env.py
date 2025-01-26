import gymnasium as gym
import numpy as np
from gymnasium import spaces

from snake_game import (BOARD_TILE_HEIGHT, BOARD_TILE_WIDTH,
                        SNAKE_SECTION_WIDTH, SnakeGame)

SNAKE_LENGTH_GOAL = 30


class SnakeEnv(gym.Env):
    def __init__(self, show_window=False, disable_input=False, seed=None):
        super().__init__()
        self.game = SnakeGame(show_window=show_window,
                              disable_input=disable_input, seed=seed)
        self.action_space = spaces.Discrete(4)
        low = np.array([-1, -1, -1, -1, -1, -1, -
                       1, -1, -1, -1], dtype=np.int32)
        high = np.array([5, 5, 5, 5, 1, 1, 1, 1, 1, 1], dtype=np.int32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int32)

    def step(self, action):
        self.game.set_direction([(1, 0), (0, -1), (-1, 0), (0, 1)][action])
        self.game.update()

        observation = self._get_observation()
        reward = self._get_reward()
        terminated = self.game.game_over
        truncated = self.game.get_snake_length() >= SNAKE_LENGTH_GOAL
        info = self._get_info()

        if self.game.show_window:
            self.render()

        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, **kwargs):
        super().reset(seed=seed)
        self.game.reset(seed=seed)

        observation = self._get_observation()
        info = self._get_info()

        return observation, info

    def render(self):
        if self.game.show_window:
            self.game.draw()

    def _get_info(self):
        return {
            "snake_length": self.game.get_snake_length(),
            "head_position": self.game.snake[0],
            "food_position": self.game.food
        }

    def _get_observation(self):
        head_x, head_y = self.game.snake[0]
        food_x, food_y = self.game.food
        tail_x, tail_y = self.game.snake[-1]
        middle_x, middle_y = self.game.snake[len(self.game.snake) // 2]

        # Calculate danger distances
        danger_up = self._scan_direction(head_x, head_y, 0, -1)
        danger_down = self._scan_direction(head_x, head_y, 0, 1)
        danger_left = self._scan_direction(head_x, head_y, -1, 0)
        danger_right = self._scan_direction(head_x, head_y, 1, 0)

        # Calculate relative positions
        relative_food_x = self._relative_position(food_x, head_x)
        relative_food_y = self._relative_position(food_y, head_y)
        relative_tail_x = self._relative_position(tail_x, head_x)
        relative_tail_y = self._relative_position(tail_y, head_y)
        relative_middle_x = self._relative_position(middle_x, head_x)
        relative_middle_y = self._relative_position(middle_y, head_y)

        return np.array([
            danger_up, danger_down, danger_left, danger_right,
            relative_food_x, relative_food_y,
            relative_tail_x, relative_tail_y,
            relative_middle_x, relative_middle_y
        ], dtype=np.int32)

    def _scan_direction(self, x, y, dx, dy):
        x_tile = (x // SNAKE_SECTION_WIDTH) + dx
        y_tile = (y // SNAKE_SECTION_WIDTH) + dy
        distance = 0

        while True:
            actual_pos = (x_tile * SNAKE_SECTION_WIDTH,
                          y_tile * SNAKE_SECTION_WIDTH)

            if x_tile >= 0 and x_tile < BOARD_TILE_WIDTH and y_tile >= 0 and y_tile < BOARD_TILE_HEIGHT \
                    and actual_pos not in self.game.snake:
                distance += 1
            else:
                break

            x_tile += dx
            y_tile += dy

        return min(distance, 6) - 1

    def _relative_position(self, pos, head_pos):
        if pos < head_pos:
            return -1
        elif pos > head_pos:
            return 1
        else:
            return 0

    def _get_reward(self):
        apple_reward = 0
        euclidean_distance_to_apple = np.linalg.norm(
            np.array(self.game.snake[0]) - np.array(self.game.food))

        if self.game.was_apple_collision:
            apple_reward = 10000

        reward = ((250 - euclidean_distance_to_apple) + apple_reward) / 100

        if self.game.game_over:
            self.reward = -100

        return reward
