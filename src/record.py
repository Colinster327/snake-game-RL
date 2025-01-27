import sys

import imageio
import numpy as np
import pygame
from stable_baselines3 import PPO

from snake_env import SnakeEnv
from snake_game import FPS

models_dir = 'models'

if len(sys.argv) > 1:
    model_path = f'{models_dir}/{sys.argv[1]}'
else:
    model_path = f'{models_dir}/PPO/3000000'

env = SnakeEnv(show_window=True, disable_input=True)
env.reset()

model = PPO.load(model_path, env)

obs, _ = env.reset()
done = False
frames = []

while not done:
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, _ = env.step(action)
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frames.append(frame)
    done = terminated or truncated

imageio.mimsave(f'assets/snake.gif', frames, fps=FPS, loop=0)

env.close()
