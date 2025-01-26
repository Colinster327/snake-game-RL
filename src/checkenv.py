from gymnasium.utils.env_checker import check_env

from snake_env import SnakeEnv

if __name__ == "__main__":
    check_env(SnakeEnv(), skip_render_check=True, skip_close_check=True)
