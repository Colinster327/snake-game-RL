import os

from stable_baselines3 import PPO
from wandb.integration.sb3 import WandbCallback

import wandb
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

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_dir)

TIMESTEPS = 100000
for i in range(1, 31):
    model.learn(
        total_timesteps=TIMESTEPS,
        progress_bar=True,
        reset_num_timesteps=False,
        tb_log_name='PPO',
        callback=WandbCallback()
    )
    model.save(f'{models_dir}/{i * TIMESTEPS}')

env.close()
