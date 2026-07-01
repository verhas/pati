# pati - Data Model Code Generator

**Project**: pati - Language-agnostic boilerplate code generator from YAML data models and Jinja2 templates.

**Vision**: Define your data model once in YAML. Generate boilerplate code in any language (Java, Rust, Python, Go, TypeScript, etc.) using Jinja2 templates.

---

## Project Structure

```
pati/
├── README.md                          # Main documentation
├── CLAUDE.md                          # This file (Claude Code instructions)
├── pyproject.toml                     # Python project config (build, deps, metadata)
├── build.sh                           # Build and package script
├── release.sh                         # PyPI release script
├── docs/
│   ├── INSTALLATION.md                # Installation instructions
│   ├── QUICKSTART.md                  # 5-minute quick start
│   ├── YAML_SCHEMA.md                 # YAML configuration schema
│   ├── TEMPLATE_SYNTAX.md             # Jinja2 template reference
│   └── EXAMPLES.md                    # Real-world template examples
├── src/
│   └── pati/
│       ├── __init__.py                # Package init with version
│       ├── cli.py                     # CLI entry point (argparse)
│       ├── generator.py               # Core generation logic
│       ├── config.py                  # YAML config loader
│       └── utils.py                   # Helper functions
├── examples/
│   ├── java-spring/
│   │   ├── schema.yaml
│   │   └── templates/
│   │       ├── entity.java.j2
│   │       ├── dto.java.j2
│   │       ├── repository.java.j2
│   │       └── liquibase.xml.j2
│   ├── rust-sqlx/
│   │   ├── schema.yaml
│   │   └── templates/
│   │       ├── model.rs.j2
│   │       └── migration.sql.j2
│   ├── python-sqlalchemy/
│   │   ├── schema.yaml
│   │   └── templates/
│   │       └── model.py.j2
│   └── go-gorm/
│       ├── schema.yaml
│       └── templates/
│           └── model.go.j2
├── tests/
│   ├── test_generator.py              # Unit tests for generator
│   ├── test_config.py                 # Unit tests for config loader
│   └── test_integration.py            # Integration tests
└── .github/
    └── workflows/
        └── ci.yml                     # CI/CD pipeline
```

---

## Core Implementation

### 1. **src/pati/__init__.py**
```python
__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "Language-agnostic boilerplate generator from YAML data models and Jinja2 templates"
```

### 2. **src/pati/config.py**
Load and parse YAML configuration file. Should:
- Read YAML file using `yaml.safe_load()`
- Validate required keys (`template_dir`, `jobs`)
- Support YAML anchors and aliases (native in PyYAML)
- Return dict structure with merged contexts

### 3. **src/pati/generator.py**
Core generation logic. Should:
- Accept config dict and job definition
- Initialize Jinja2 Environment with template loader
- Load template by name
- Render template with job context
- Create output directories as needed
- Write rendered output to file
- Return success/failure status with logging

### 4. **src/pati/cli.py**
Command-line interface using argparse. Should:
- `pati cuire <config.yaml>` — Process all jobs in config
- `pati mise --template <name>` — Create skeleton config + template dir
- `pati list-templates` — Show available example templates
- `--dry-run` flag — Show what would be generated without writing
- `--output-dir` flag — Override output paths from config
- Proper error handling and user-friendly messages
- Progress indicators (processing job X of Y)

### 5. **src/pati/utils.py**
Helper functions:
- `ensure_directories(path)` — Create dirs recursively
- `safe_write_file(path, content)` — Write with backups
- `get_example_templates_path()` — Locate bundled example templates
- `validate_config(config)` — Basic schema validation

---

## Build and Release Scripts

### build.sh
```bash
#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Building pati...${NC}"

# 1. Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

# 2. Install/upgrade build tools
echo "Installing build dependencies..."
pip install --upgrade pip setuptools wheel build

# 3. Run tests
echo -e "${BLUE}Running tests...${NC}"
pip install -e ".[dev]"
pytest tests/ -v --cov=src/pati --cov-report=term-missing

# 4. Build distribution packages
echo -e "${BLUE}Building distributions...${NC}"
python -m build

# 5. Validate with twine
echo "Validating packages..."
pip install twine
twine check dist/*

echo -e "${GREEN}✓ Build successful!${NC}"
echo "Artifacts: $(ls -lh dist/)"
```

### release.sh
```bash
#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if version argument provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version argument required${NC}"
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.1.0"
    exit 1
fi

VERSION=$1

echo -e "${BLUE}Releasing pati v${VERSION}...${NC}"

# 1. Update version in __init__.py
echo "Updating version in src/pati/__init__.py..."
sed -i "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/g" src/pati/__init__.py

# 2. Build
echo -e "${BLUE}Building package...${NC}"
./build.sh

# 3. Check PyPI credentials
echo -e "${BLUE}Checking PyPI credentials...${NC}"
if [ ! -f ~/.pypirc ]; then
    echo -e "${YELLOW}Warning: ~/.pypirc not found. You'll be prompted for credentials.${NC}"
fi

# 4. Upload to PyPI
echo -e "${BLUE}Uploading to PyPI...${NC}"
twine upload dist/* --verbose

# 5. Create git tag
echo -e "${BLUE}Creating git tag...${NC}"
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
git push origin "v${VERSION}"

echo -e "${GREEN}✓ Release v${VERSION} complete!${NC}"
echo -e "${GREEN}✓ Package available at: https://pypi.org/project/pati/${VERSION}/${NC}"
```

---

## Documentation

### docs/INSTALLATION.md
- System requirements (Python 3.8+)
- pip install pati
- Verify installation: `pati --version`
- For development: `git clone ... && pip install -e .[dev]`
- PyPI link and version badge

### docs/QUICKSTART.md
- 5-minute walkthrough
- Example: Generate Java Spring boilerplate
- Show command: `pati cuire examples/java-spring/schema.yaml`
- Explain output structure
- Show schema.yaml and one simple template
- Point to full examples

### docs/YAML_SCHEMA.md
- Detailed YAML structure documentation
- `template_dir` — path to templates
- `shared` — optional shared data with anchors
- `jobs` — array of generation jobs
- Each job: `template`, `output`, `context` (dict)
- Show YAML anchors/aliases example
- Merge key (`<<:`) explanation

### docs/TEMPLATE_SYNTAX.md
- Jinja2 quick reference
- Variables: `{{ var }}`
- Loops: `{% for item in items %} ... {% endfor %}`
- Conditionals: `{% if condition %} ... {% endif %}`
- Filters: `{{ value | capitalize }}`
- Loop special variable: `loop.index`, `loop.first`, etc.
- Link to official Jinja2 docs

### docs/EXAMPLES.md
- 3-4 complete working examples
- Java entity + DTO + Liquibase changelog
- Rust model + SQL migrations
- Python SQLAlchemy model
- Each: show YAML schema, templates, generated output
- Emphasis on single source of truth

### README.md (Main)
- Project description and use cases
- Feature highlights (language-agnostic, YAML source, Jinja2 templates)
- Quick install: `pip install pati`
- Quick usage: `pati cuire schema.yaml`
- Links to docs: Installation, Quickstart, Examples
- Screenshots/diagrams (optional: show data model → artifacts flow)
- Contributing guidelines
- License (MIT or Apache 2.0)

---

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "patisserie"
dynamic = ["version"]
description = "Language-agnostic boilerplate generator from YAML data models"
readme = "README.md"
requires-python = ">=3.8"
license = "MIT OR Apache-2.0"
license-files = ["LICENSE", "LICENSE-MIT", "LICENSE-APACHE"]
authors = [
    {name = "Peter Verhas", email = "peter.verhas@gmail.com"},
]
keywords = ["code-generation", "boilerplate", "yaml", "jinja2", "templates"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Code Generators",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "pyyaml>=6.0",
    "jinja2>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "flake8>=5.0",
    "twine>=4.0",
    "build>=0.9",
]

[project.urls]
Homepage = "https://github.com/yourusername/pati"
Documentation = "https://github.com/yourusername/pati/tree/main/docs"
Repository = "https://github.com/yourusername/pati.git"
Issues = "https://github.com/yourusername/pati/issues"

[project.scripts]
pati = "pati.cli:main"

[tool.setuptools.dynamic]
version = {attr = "pati.__version__"}

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages]
find = {where = ["src"]}

[tool.setuptools.package-data]
pati = ["examples/**/*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src/pati --cov-report=term-missing"

[tool.black]
line-length = 100
target-version = ['py38']

[tool.flake8]
max-line-length = 100
exclude = [".git", "__pycache__", "build", "dist"]
```

---

## Implementation Priority

1. **Phase 1 - Core**: `config.py`, `generator.py`, `cli.py`, `utils.py`
2. **Phase 2 - Examples**: Create 4 example templates (Java, Rust, Python, Go)
3. **Phase 3 - Testing**: Write `test_*.py` files with good coverage
4. **Phase 4 - Packaging**: `pyproject.toml`, `build.sh`
5. **Phase 5 - Documentation**: All `docs/` and `README.md`
6. **Phase 6 - Release**: `release.sh` and PyPI publication

---

## Testing Strategy

- **Unit tests**: config loading, template rendering, file writes
- **Integration tests**: end-to-end with example schemas
- **CLI tests**: argument parsing, help output, error handling
- Target: >80% code coverage

---

## Next Steps

Start with Phase 1 using Claude Code:
1. Scaffold the directory structure
2. Implement core modules (`config.py`, `generator.py`)
3. Create CLI with argparse
4. Test with one example (Java Spring)
5. Refine and document

Use `vi` for any manual edits to configuration or template files.

---

## Command Reference

```bash
# Build
./build.sh

# Release to PyPI
./release.sh 0.1.0

# Local install (development)
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov

# CLI usage
pati cuire schema.yaml
pati mise --template java-spring
pati list-templates
pati cuire schema.yaml --dry-run
```

---

**Ready to build with Claude Code!**