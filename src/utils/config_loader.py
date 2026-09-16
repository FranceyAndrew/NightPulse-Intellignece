import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"

def load_yaml(name: str):
    """
    Load a YAML file from the config directory.

    Parameters:
    -----------------
        name (str): The name of the YAML file to load (without the .yaml extension).
    
    Returns:
    -----------------
        dict: The contents of the YAML file as a dictionary.
    """
    
    file_path = CONFIG_DIR / f"{name}.yaml"
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)