import os
from pathlib import Path
from shutil import copy2
import logging
from typing import Dict, Any
from jinja2 import Environment

logger = logging.getLogger(__name__)


class TemplateFieldResolver:
    """Resolve template syntax in context field values using fixed-point iteration."""

    def __init__(self, env: Environment, context: Dict[str, Any]):
        """Initialize resolver with Jinja2 environment and context.

        Args:
            env: Jinja2 Environment
            context: Dictionary of context values
        """
        self.env = env
        self.context = context

    def resolve_all(self) -> Dict[str, Any]:
        """Resolve all context fields using fixed-point iteration.

        Iteratively renders all template strings until they stop changing.
        This handles nested dependencies correctly.

        Returns:
            Dictionary with all resolved values
        """
        resolved = dict(self.context)  # Start with original values
        max_iterations = 100
        iteration = 0

        while iteration < max_iterations:
            changed = False
            new_resolved = {}

            for key, value in resolved.items():
                new_value = self._resolve_value(value, resolved)
                if new_value != value:
                    changed = True
                new_resolved[key] = new_value

            resolved = new_resolved
            iteration += 1

            if not changed:
                logger.debug(f"Resolved all fields in {iteration} iteration(s)")
                return resolved

        raise ValueError("Context resolution did not converge after 100 iterations. Possible circular dependency.")

    def _resolve_value(self, value: Any, context: Dict[str, Any]) -> Any:
        """Resolve a single value using the provided context.

        Args:
            value: Value to resolve
            context: Current resolved context

        Returns:
            Resolved value
        """
        if isinstance(value, str) and ('{{' in value or '{%' in value):
            try:
                template = self.env.from_string(value)
                return template.render(context)
            except Exception as e:
                logger.debug(f"Error rendering template '{value}': {e}")
                return value
        elif isinstance(value, list):
            return [self._resolve_value(item, context) for item in value]
        elif isinstance(value, dict):
            return {k: self._resolve_value(v, context) for k, v in value.items()}
        else:
            return value

def ensure_directories(path: str) -> Path:
    """Create directories recursively if they don't exist.

    Args:
        path: Directory path to create

    Returns:
        Path object for the created directory
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {p}")
    return p


def safe_write_file(path: str, content: str) -> None:
    """Write content to file with backup of existing file if content changed.

    If the file already exists with identical content, skip write and backup.

    Args:
        path: File path to write to
        content: Content to write
    """
    p = Path(path)
    ensure_directories(p.parent)

    # If file exists, check if content is identical
    if p.exists():
        try:
            existing_content = p.read_text()
            if existing_content == content:
                logger.debug(f"File unchanged, skipping write: {p}")
                return
        except Exception as e:
            logger.debug(f"Could not read existing file {p}: {e}")

        # Content differs, create backup
        backup_path = Path(str(p) + '.bak')
        copy2(p, backup_path)
        logger.info(f"Backed up existing file to {backup_path}")

    with open(p, 'w') as f:
        f.write(content)
    logger.debug(f"Wrote file: {p}")


def get_example_templates_path() -> Path:
    """Get path to bundled example templates.

    Returns:
        Path to examples directory
    """
    return Path(__file__).parent.parent.parent / "examples"


def get_package_root() -> Path:
    """Get the root directory of the sommelier package.

    Returns:
        Path to package root
    """
    return Path(__file__).parent.parent.parent
