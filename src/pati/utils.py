import os
from pathlib import Path
from shutil import copy2
import logging
from typing import Dict, Any
from jinja2 import Environment, Undefined

logger = logging.getLogger(__name__)


def is_templated(value: Any) -> bool:
    return isinstance(value, str) and ('{{' in value or '{%' in value)

def purge(resolved, unresolved):
    for key in resolved.keys():
        unresolved.pop(key, None)

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
        unresolved = dict(self.context) # Start with original values
        resolved = {}
        for key, value in unresolved.items():
            if is_templated(value):
               continue
            resolved[key] = value

        purge(resolved, unresolved)

        max_iterations = 100
        iteration = 0

        while iteration < max_iterations and len(unresolved) > 0 :

            for key, value in unresolved.items():
                try:
                    new_value = self._resolve_value(value, resolved)
                    resolved[key] = new_value
                except Exception as e:
                    continue

            purge(resolved, unresolved)
            iteration += 1
        if len(unresolved) > 0:
            raise ValueError(f"Context resolution did not converge after {max_iterations} iterations.\nPossible circular dependency or unresolvable values: {unresolved}.")
        return resolved

    def _resolve_value(self, value: Any, context: Dict[str, Any]) -> Any:
        """Resolve a single value using the provided context.

        Args:
            value: Value to resolve
            context: Current resolved context

        Returns:
            Resolved value, or the original value if there is nothing to be resolved or
            the referenced {{ value }} to be used is not available yet
        """
        if is_templated(value):
            template = self.env.from_string(value)
            return template.render(context)
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
    """Write content to file with backup of an existing file if content changed.

    If the file already exists with identical content, skip writing and backup.

    Args:
        path: File path to write to
        content: Content to write
    """
    p = Path(path)
    ensure_directories(str(p.parent))

    # If the file exists, check if the content is identical
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
    """Get the root directory of the pati package.

    Returns:
        Path to package root
    """
    return Path(__file__).parent.parent.parent
