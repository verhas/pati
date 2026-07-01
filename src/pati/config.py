import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load and parse YAML configuration file.

    Args:
        config_path: Path to YAML configuration file.

    Returns:
        Dictionary with parsed config

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    if config_path is None:
        config_path = Path.cwd() / ".pati" / "schema.yaml"
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    if not config:
        config = {}

    validate_config(config)
    return config


def validate_config(config: Dict[str, Any]) -> None:
    """Validate required keys in config.

    Args:
        config: Configuration dictionary

    Raises:
        ValueError: If required keys are missing
    """
    if 'jobs' not in config:
        return

    if not isinstance(config['jobs'], dict):
        raise ValueError("'jobs' must be a dict/map")

    for job_name, job in config['jobs'].items():
        if 'output' not in job:
            raise ValueError(f"Job '{job_name}' missing 'output' key")
        if 'context' not in job:
            raise ValueError(f"Job '{job_name}' missing 'context' key")
        if 'template' not in job:
            raise ValueError(f"Job '{job_name}' missing 'template' key")
