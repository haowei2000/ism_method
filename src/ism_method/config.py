from pathlib import Path

import yaml


def load_yaml_config(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
def get_config():
    return load_yaml_config(Path(__file__).parent/"config.yaml")