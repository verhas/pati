# Quick Start Guide

Get up and running with Sommelier in 5 minutes!

**License**: MIT OR Apache 2.0 at your option — See [LICENSE-MIT](../LICENSE-MIT) or [LICENSE-APACHE](../LICENSE-APACHE).

## 1. Install Sommelier

```bash
pip install sommelier
```

## 2. Initialize a Project

Initialize a new project in current directory:

```bash
sommelier init
```

This creates the `.sommelier/` directory structure:
```
.sommelier/
├── schema.yaml    # Your data model configuration
└── tmplts/        # Template files directory
```

## 3. Explore the Default Schema

Open `.sommelier/schema.yaml`:

```yaml
# Sommelier Configuration
# Jobs are defined as a map, where each key is a job name.
# Each job has:
#   - template: Either a template filename or inline Jinja2 template
#   - output: Path where the generated file will be written
#   - context: Dictionary of variables passed to the template

jobs: {}
  # my_entity:
  #   template: entity.java.j2
  #   output: generated/Entity.java
  #   context:
  #     entity_name: User
```

**Key concepts:**
- `.sommelier/schema.yaml` — Your default schema (no argument needed to use it)
- `.sommelier/tmplts/` — Location of your Jinja2 templates (default)
- `jobs` — Dictionary of generation tasks (key = job name)
  - `template` — Template file name or inline Jinja2 template
  - `output` — Where to write the generated file
  - `context` — Data passed to the template

## 4. Add a Job with Inline Template

Edit `.sommelier/schema.yaml` and add an inline template:

```yaml
jobs:
  hello:
    template: |
      #!/bin/bash
      echo "Hello {{ name }}!"
    output: generated/hello.sh
    context:
      name: World
```

**Template syntax:**
- `{{ variable }}` — Insert variable
- `{% for item in items %}` — Loop over items
- `{% if condition %}` — Conditional

[Full Jinja2 reference →](TEMPLATE_SYNTAX.md)

## 5. Generate Code

Dry run (preview without writing):

```bash
sommelier generate --dry-run
```

Real generation (creates files):

```bash
sommelier generate
```

Check the output:
```bash
cat generated/hello.sh
```

## 6. Use Template Files Instead

Create a template file: `.sommelier/tmplts/entity.java.j2`

```jinja2
package {{ package }}.entity;

@Entity
public class {{ entity_name }} {
{% for field in fields %}
    private {{ field.type }} {{ field.name }};
{% endfor %}
}
```

Update `.sommelier/schema.yaml`:

```yaml
jobs:
  user_entity:
    template: entity.java.j2          # Reference to file in tmplts/
    output: generated/User.java
    context:
      package: com.example
      entity_name: User
      fields:
        - name: id
          type: Long
        - name: username
          type: String
```

Generate:
```bash
sommelier generate
```

## 7. Multiple Jobs

Add more jobs as a map:

```yaml
jobs:
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      entity_name: User

  product_entity:
    template: entity.java.j2
    output: generated/Product.java
    context:
      entity_name: Product

  config_file:
    template: |
      app_name={{ app }}
      version={{ version }}
    output: generated/app.conf
    context:
      app: MyApp
      version: 1.0.0
```

## 8. Reusable Config with YAML Anchors

Use anchors to avoid repetition:

```yaml
shared:
  java_config: &java
    package: com.example
    
  common_fields: &base_fields
    - name: id
      type: Long

jobs:
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      <<: *java
      entity_name: User
      fields:
        <<: *base_fields
        - name: username
          type: String
```

## Next Steps

- [Full YAML schema documentation](YAML_SCHEMA.md)
- [Advanced template syntax](TEMPLATE_SYNTAX.md)
- [Real-world examples](EXAMPLES.md)
- [Template best practices](https://jinja.palletsprojects.com/)

## Common Commands

```bash
# Generate all jobs from default schema (.sommelier/schema.yaml)
sommelier generate

# Generate a single job by name
sommelier generate pojo_user

# Generate jobs matching a glob pattern
sommelier generate 'pojo*'

# Generate jobs matching multiple patterns
sommelier generate 'pojo*' dto_user

# Generate with dry-run
sommelier generate --dry-run

# Generate from a specific schema
sommelier generate --config path/to/schema.yaml

# Override output directory
sommelier generate --output-dir /path/to/output

# List available example templates
sommelier list

# Initialize new project
sommelier init

# Initialize into a specific directory
sommelier init --output my-project

# Show version
sommelier --version

# Logging level (global, mutually exclusive)
sommelier --verbose generate    # debug output
sommelier --quiet generate      # warnings and errors only (-q)
sommelier --silent generate     # errors only (-s)

# Show help
sommelier --help
sommelier generate --help
```

## Tips

✨ **Inline vs File Templates**
- Use inline templates for small, simple templates
- Use file templates when they get large or reusable

✨ **Job Naming**
- Use descriptive job names: `user_entity`, `config_file`, `migration`
- Job names appear in generation progress messages

✨ **Schema Organization**
- Keep related jobs together
- Use anchors for shared configuration
- Add comments to complex contexts

Happy generating!
