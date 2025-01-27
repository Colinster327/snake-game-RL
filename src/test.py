import sys

from stable_baselines3 import PPO

from snake_env import SnakeEnv

models_dir = 'models/PPO'

if len(sys.argv) > 1:
    model_path = f'{models_dir}/{sys.argv[1]}.zip'
else:
    model_path = f'{models_dir}/3000000.zip'

env = SnakeEnv(show_window=True, disable_input=True)
env.reset()

model = PPO.load(model_path, env)

episodes = 500

for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

env.close()
