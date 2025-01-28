import os
import sys

import wandb
from stable_baselines3 import PPO
from wandb.integration.sb3 import WandbCallback

from snake_env import SnakeEnv

wandb.init(
    project="snake-game-rl",
    sync_tensorboard=True,
)

models_dir = 'models/PPO'
log_dir = 'logs'

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

env = SnakeEnv(show_window=False)
env.reset()

if len(sys.argv) > 1:
    model = PPO.load(
        f'{models_dir}/{sys.argv[1]}', env, verbose=1, tensorboard_log=log_dir)
else:
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)

TIMESTEPS = 10000

start = 1 if len(sys.argv) <= 1 else int(sys.argv[1]) // TIMESTEPS + 1
end = start + 300
restart_timesteps = True

for i in range(start, end):
    model.learn(
        total_timesteps=TIMESTEPS,
        progress_bar=True,
        reset_num_timesteps=restart_timesteps,
        tb_log_name='PPO',
        callback=WandbCallback()
    )
    model.save(f'{models_dir}/{i * TIMESTEPS}')
    restart_timesteps = False

env.close()
