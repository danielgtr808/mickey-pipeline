from pathlib import Path
from src.modules.files import find_relative_file
from src.modules.dicts import merge_with_defaults
from typing import Dict, Any, Optional

import yaml



def _load_and_validate_config(relative_path: Path, environment: str) -> Dict[str, Any]:
    config_file = find_relative_file(relative_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    with open(config_file, 'r') as f:
        full_config = yaml.safe_load(f)
    if environment not in full_config:
        raise KeyError(f"Environment '{environment}' not found in config file. Available: {list(full_config.keys())}")
    return full_config[environment]

def config_loader(
    environment: str,
    config_relative_path: Path,
    default_config_relative_path: Optional[Path] = None
) -> Dict[str, Any]:
    env_config = _load_and_validate_config(config_relative_path, environment)
    
    if default_config_relative_path is None:
        return env_config
    
    default_config = _load_and_validate_config(default_config_relative_path, environment)
    
    # Merge: env_config takes precedence over defaults
    return merge_with_defaults(default_config, env_config)
