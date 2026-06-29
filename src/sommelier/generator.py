import logging
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, BaseLoader, TemplateNotFound, TemplateSyntaxError

from .utils import ensure_directories, safe_write_file, TemplateFieldResolver

logger = logging.getLogger(__name__)


class StringLoader(BaseLoader):
    """Jinja2 loader for inline template strings."""

    def get_source(self, environment, template):
        return template, None, lambda: True


class Generator:
    """Template-based code generator."""

    def __init__(self, template_dir: str):
        """Initialize generator with template directory.

        Args:
            template_dir: Path to directory containing Jinja2 templates
        """
        self.template_dir = Path(template_dir)
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {template_dir}")

        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.string_loader = StringLoader()

    def generate(self, job_name: str, job: Dict[str, Any], dry_run: bool = False) -> bool:
        """Generate output from template and job definition.

        Args:
            job_name: Name of the job
            job: Job configuration with 'template', 'output', and 'context'
            dry_run: If True, don't write files

        Returns:
            True if successful, False otherwise
        """
        template_str = job.get('template')
        output_path = job.get('output')
        context = job.get('context', {})

        try:
            # Resolve template variables in context
            resolver = TemplateFieldResolver(self.env, context)
            resolved_context = resolver.resolve_all()
            logger.debug(f"Resolved context: {resolved_context}")
        except (ValueError, KeyError) as e:
            logger.error(f"Error resolving context in job '{job_name}': {e}")
            return False

        try:
            is_inline = '\n' in template_str or '{%' in template_str or '{{' in template_str

            if is_inline:
                logger.info(f"Using inline template for job: {job_name}")
                env = Environment(loader=self.string_loader)
                template = env.from_string(template_str)
            else:
                logger.info(f"Loading template: {template_str}")
                template = self.env.get_template(template_str)
        except TemplateNotFound:
            logger.error(f"Template not found: {template_str}")
            return False
        except TemplateSyntaxError as e:
            logger.error(f"Template syntax error in job '{job_name}': {e}")
            return False

        try:
            logger.debug(f"Rendering template with resolved context")
            rendered = template.render(resolved_context)
        except Exception as e:
            logger.error(f"Error rendering template for job '{job_name}': {e}")
            return False

        if dry_run:
            logger.info(f"[DRY RUN] Would write {len(rendered)} bytes to {output_path}")
            return True

        try:
            ensure_directories(Path(output_path).parent)
            safe_write_file(output_path, rendered)
            logger.info(f"Generated: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing output file {output_path}: {e}")
            return False

    def generate_all(self, config: Dict[str, Any], dry_run: bool = False) -> int:
        """Generate all jobs from configuration.

        Args:
            config: Configuration dictionary with 'jobs' dict
            dry_run: If True, don't write files

        Returns:
            Number of successful generations
        """
        jobs = config.get('jobs', {})
        total = len(jobs)
        successful = 0

        if total == 0:
            logger.info("No jobs to process")
            return 0

        logger.info(f"Processing {total} job(s)")

        for i, (job_name, job) in enumerate(jobs.items(), 1):
            logger.info(f"Processing job {i}/{total}: {job_name}")
            if self.generate(job_name, job, dry_run=dry_run):
                successful += 1

        logger.info(f"Completed: {successful}/{total} successful")
        return successful
