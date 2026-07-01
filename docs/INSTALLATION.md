# Installation Guide

## License

pati is dual-licensed under the **MIT License** and the **Apache License 2.0**. You may choose either license at your option.

- [MIT License](../LICENSE-MIT)
- [Apache License 2.0](../LICENSE-APACHE)

## System Requirements

- Python 3.8 or later
- pip (Python package manager)

## Quick Install

Install pati from PyPI:

```bash
pip install patisserie
```

## Verify Installation

Check that pati is installed correctly:

```bash
pati --version
```

You should see output like: `pati 0.1.0`

Also verify the CLI works:

```bash
pati --help
```

## First Run

After installation:

### 1. Initialize a new project

```bash
mkdir my-project
cd my-project
pati init
```

This creates:
```
my-project/
└── .pati/
    ├── schema.yaml    # Your configuration
    └── tmplts/        # Template files directory
```

### 2. Edit your schema

Open `.pati/schema.yaml` and add a job:

```yaml
jobs:
  greeting:
    template: |
      #!/bin/bash
      echo "Hello {{ name }}!"
    output: generated/hello.sh
    context:
      name: World
```

### 3. Generate code

```bash
pati generate
```

### 4. Check the output

```bash
cat generated/hello.sh
```

## List Available Templates

View built-in example templates:

```bash
pati list
```

Output:
```
Available templates:
  - go-gorm
  - java-spring
  - python-sqlalchemy
  - rust-sqlx
```

## Development Setup

If you want to contribute or modify pati, clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/pati.git
cd pati
pip install -e ".[dev]"
```

The `[dev]` extra installs additional tools for testing and code formatting:
- pytest (testing framework)
- pytest-cov (coverage reporting)
- black (code formatter)
- flake8 (linter)
- twine (PyPI upload tool)

### Run tests

```bash
pytest tests/ -v --cov
```

### Build and release

```bash
./build.sh              # Build package
./release.sh 0.2.0      # Release to PyPI (requires credentials)
```

## Virtual Environment Setup

Recommended for development or isolated usage:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install pati
pip install patisserie

# Or for development
git clone https://github.com/yourusername/pati.git
cd pati
pip install -e ".[dev]"
```

To deactivate:
```bash
deactivate
```

## Troubleshooting

### Command not found

If `pati` command is not found after installation, you may need to add Python's bin directory to your PATH:

- **Linux/macOS**: `~/.local/bin` or `/usr/local/bin`
- **Windows**: `%APPDATA%\Python\Scripts`

Verify Python installation location:
```bash
python3 -m site
```

### Permission denied (macOS/Linux)

If you get permission errors when installing to system Python, use a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install patisserie
```

### Default schema not found

If `pati generate` fails with "Config file not found: .pati/schema.yaml", make sure:

1. You've run `pati init` in the current directory
2. You're in the correct directory containing `.pati/`
3. The file `.pati/schema.yaml` exists

### Template not found

If you get "Template not found: mytemplate.j2", check:

1. Template file exists in `.pati/tmplts/`
2. Filename matches exactly (case-sensitive)
3. Filename doesn't have typos

### YAML parsing errors

If you see "YAML Error: mapping values are not allowed":

1. Check that you're using spaces (not tabs) for indentation
2. Ensure proper YAML structure (colons need spaces after them)
3. Quote strings with special characters: `"value: with: colons"`

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade pati
```

## Uninstalling

To remove pati:

```bash
pip uninstall pati
```

If you used a virtual environment, also remove it:
```bash
rm -rf venv
```

## Project Structure

pati uses a standardized project structure:

```
my-project/
├── .pati/
│   ├── schema.yaml              # Schema file (always read by default)
│   └── tmplts/                  # Template files directory (default)
└── generated/                   # Generated files (created by pati)
    ├── file1.java
    ├── file2.sh
    └── config.properties
```

You can customize the template directory in `.pati/schema.yaml`:

```yaml
template_dir: my_templates        # Override default tmplts/
```

## Next Steps

- [Quick Start Guide](QUICKSTART.md)
- [YAML Schema Reference](YAML_SCHEMA.md)
- [Template Syntax](TEMPLATE_SYNTAX.md)
- [Examples](EXAMPLES.md)
