# Sommelier

[![PyPI Version](https://img.shields.io/pypi/v/sommelier.svg)](https://pypi.org/project/sommelier/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE-MIT)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE-APACHE)

**Language-agnostic boilerplate code generator from YAML data models and Jinja2 templates.**

Define your data model once in YAML. Generate boilerplate code in any language (Java, Rust, Python, Go, TypeScript, etc.) using Jinja2 templates.

## Why Sommelier?

- **Single Source of Truth**: Define your data model once, generate code for multiple languages
- **Template-Driven**: Use Jinja2 to create language-specific templates
- **Configuration as Code**: YAML schemas with anchors for DRY configuration
- **Language Agnostic**: Generate Java, Rust, Python, Go, TypeScript, or any text-based format
- **Zero Runtime Dependencies**: Just Python, PyYAML, and Jinja2

## Quick Start

### Installation

```bash
pip install sommelier
```

### 5-Minute Example

1. **Initialize a project:**
   ```bash
   mkdir my-project && cd my-project
   sommelier init
   ```

2. **Edit your data model** (`.sommelier/schema.yaml`):
   ```yaml
   jobs:
     user_entity:
       template: entity.java.j2
       output: generated/User.java
       context:
         package: com.example
         class_name: User
         fields:
           - name: id
             type: Long
           - name: username
             type: String
   ```

3. **Customize a template** (`.sommelier/tmplts/entity.java.j2`):
   ```jinja2
   package {{ package }};
   
   public class {{ class_name }} {
   {% for field in fields %}
       private {{ field.type }} {{ field.name }};
   {% endfor %}
   }
   ```

4. **Generate code:**
   ```bash
   sommelier generate
   ```

5. **Check the output:**
   ```bash
   cat generated/User.java
   ```

## Features

### 📋 YAML Schema Support
- Define jobs with template, output, and context
- YAML anchors (`&name`) and aliases (`*name`) for reusable config
- Merge key (`<<: *alias`) for DRY configuration
- Full PyYAML support for complex structures

### 🎨 Jinja2 Templates
- Variables: `{{ variable }}`
- Loops: `{% for item in items %}`
- Conditionals: `{% if condition %}`
- Filters: `{{ value | filter }}`
- Complete Jinja2 feature set

### 🛠️ CLI Tools
```bash
# Generate all jobs from default schema (.sommelier/schema.yaml)
sommelier generate

# Generate specific job(s) by name
sommelier generate pojo_user

# Generate jobs matching a glob pattern
sommelier generate 'pojo*'

# Generate jobs matching multiple patterns
sommelier generate 'pojo*' dto_user

# Generate from a specific schema
sommelier generate --config path/to/schema.yaml

# Dry run (preview without writing)
sommelier generate --dry-run

# Override output directory
sommelier generate --output-dir /path/to/output

# Initialize new project
sommelier init

# List available example templates
sommelier list
```

### 📦 Built-in Examples
- **Java Spring Boot**: Entities, DTOs, Repositories, Liquibase migrations
- **Rust SQLx**: Models with SQLx derive macros
- **Python SQLAlchemy**: ORM models
- **Go GORM**: Struct definitions with GORM tags

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)** — Setup and troubleshooting
- **[Quick Start Guide](docs/QUICKSTART.md)** — Get running in 5 minutes
- **[YAML Schema Reference](docs/YAML_SCHEMA.md)** — Complete schema documentation
- **[Jinja2 Template Syntax](docs/TEMPLATE_SYNTAX.md)** — Template language reference
- **[Real-World Examples](docs/EXAMPLES.md)** — Complete working examples

## Example Use Cases

### Multi-language ORM Models
```yaml
jobs:
  user_java:
    template: entity.java.j2
    output: src/main/java/User.java
    context: { class_name: User, fields: [...] }
  
  user_python:
    template: model.py.j2
    output: models/user.py
    context: { class_name: User, fields: [...] }
  
  user_rust:
    template: model.rs.j2
    output: src/models/user.rs
    context: { struct_name: User, fields: [...] }
```

### Microservice Scaffolding
Generate controllers, services, and DTOs from a single data model schema.

### API Client/Server Code
Generate OpenAPI specs, request/response models, and route handlers.

### Database Migrations
Generate SQL migrations, Liquibase changesets, or Flyway migrations.

### Configuration Files
Generate Docker Compose, Kubernetes manifests, or Terraform code.

## Architecture

```
schema.yaml          Template files              Generated code
     │               (Jinja2)                         │
     │                   │                            │
     └──────────────────────────────────────────────────→
                    Sommelier
          (config loader + generator)
```

1. Load YAML schema
2. Extract job configuration
3. Initialize Jinja2 environment
4. Render each template with context
5. Write generated files

## Development

### Setup
```bash
git clone https://github.com/yourusername/sommelier.git
cd sommelier
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest tests/ -v --cov
```

### Building
```bash
./build.sh
```

### Releasing
```bash
./release.sh 0.2.0
```

## CLI Reference

```bash
# Generate from default schema
sommelier generate [JOB ...] [OPTIONS]
  JOB                     Job name(s) or glob patterns to run (default: all)
                          Examples: pojo_user  'pojo*'  'pojo*' dto_user
  --config, -c FILE       Path to schema file (default: .sommelier/schema.yaml)
  --dry-run               Show what would be generated without writing
  --output-dir DIR        Override output directory for all jobs

# Initialize new project structure
sommelier init [OPTIONS]
  --output, -o DIR        Output directory (default: current directory)

# List available example templates
sommelier list

# Show version
sommelier --version, -v

# Logging level (global flags, mutually exclusive)
sommelier --verbose COMMAND   # debug output
sommelier --quiet COMMAND     # warnings and errors only
sommelier -q COMMAND
sommelier --silent COMMAND    # errors only
sommelier -s COMMAND

# Show help
sommelier --help
sommelier COMMAND --help
```

## Project Structure

```
sommelier/
├── src/sommelier/           # Main package
│   ├── __init__.py          # Package metadata
│   ├── cli.py               # CLI entry point
│   ├── config.py            # YAML config loader
│   ├── generator.py         # Template generator
│   └── utils.py             # Helper functions
├── examples/                # Example templates
│   ├── java-spring/
│   ├── rust-sqlx/
│   ├── python-sqlalchemy/
│   └── go-gorm/
├── tests/                   # Test suite
├── docs/                    # Documentation
├── setup.py                 # Package metadata
├── pyproject.toml          # Modern Python config
├── build.sh                 # Build script
└── release.sh              # Release script
```

## License

Licensed under either of:

- [MIT License](LICENSE-MIT)
- [Apache License, Version 2.0](LICENSE-APACHE)

at your option.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure tests pass: `pytest tests/ -v --cov`
5. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sommelier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sommelier/discussions)
- **Docs**: [Full Documentation](docs/)

## Roadmap

- [ ] Watch mode for live template development
- [ ] Template inheritance and includes
- [ ] Custom Jinja2 filters and globals
- [ ] Schema validation with JSON Schema
- [ ] Plugin system for extensibility
- [ ] Web UI for template editing
- [ ] Template marketplace

---

**Ready to generate? → [Quick Start Guide](docs/QUICKSTART.md)**
