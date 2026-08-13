import yaml
import os

def get_config(env=None):
    env = env or os.getenv("TEST_ENV", "qa")
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", f"{env}.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    config["email"] = os.getenv("TEST_EMAIL", config.get("email"))
    config["password"] = os.getenv("TEST_PASSWORD", config.get("password"))
    return config
