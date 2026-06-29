# YAML Schema Documentation

Complete reference for Sommelier's YAML configuration format.

## Project Structure

The default Sommelier project uses this structure:

```
my-project/
└── .sommelier/
    ├── schema.yaml       # Your configuration file
    └── tmplts/           # Template files directory
```

The default schema location is `.sommelier/schema.yaml` and default template directory is `.sommelier/tmplts/`.

## Top-level Keys

### `template_dir` (optional)
Path to the directory containing your Jinja2 templates.

**Default:** `.sommelier/tmplts/` (relative to schema.yaml)

**Example:**
```yaml
template_dir: templates    # Relative to schema.yaml location
```

**Note:** Usually not needed, as `.sommelier/tmplts/` is the default.

### `shared` (optional)
Shared data that can be reused across jobs using YAML anchors and aliases.

**Example:**
```yaml
shared:
  base_package: &pkg com.example
  database: &db
    host: localhost
    port: 5432
```

### `jobs` (required)
Dictionary/map of generation jobs. Each key is a job name.

**Format:**
```yaml
jobs:
  job_name:
    template: ...
    output: ...
    context: ...
```

---

## Job Configuration

Each job in the `jobs` dictionary must have:

### `template` (required)
Either:
1. **Template filename** — Name of file in `tmplts/` directory
2. **Inline template** — Multiline Jinja2 template string

**Type:** string

**Examples:**

Template file reference:
```yaml
template: entity.java.j2
```

Inline template:
```yaml
template: |
  class {{ name }} {
    // Auto-generated
  }
```

### `output` (required)
Path where the generated file will be written.

**Type:** string

**Example:**
```yaml
output: src/main/java/com/example/User.java
```

### `context` (required)
Dictionary of variables passed to the template.

**Type:** object

**Example:**
```yaml
context:
  package: com.example
  class_name: User
  fields:
    - name: id
      type: Long
    - name: name
      type: String
```

---

## Template Detection

Sommelier automatically detects whether a template is a filename or inline content:

- **Inline template** — If contains `{{`, `{%`, or newlines
- **Template filename** — Simple string without template syntax

Examples:
```yaml
jobs:
  # Treated as inline template (contains {{)
  greeting:
    template: "echo {{ message }}"
    output: output.txt

  # Treated as template filename
  entity:
    template: entity.java.j2
    output: output.java

  # Clearly inline (multiline)
  config:
    template: |
      [app]
      name={{ app_name }}
    output: config.ini
```

---

## YAML Anchors and Aliases

Use YAML anchors (`&name`) and aliases (`*name`) to define reusable blocks:

### Basic Usage

```yaml
shared:
  java_config: &java
    package: com.example.app
    author: John Doe

jobs:
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      <<: *java              # Merge java_config into context
      class_name: User
```

The `<<` merge key (`<<: *java`) includes all keys from `java_config` into `context`.

### Complex Example

```yaml
shared:
  base_package: &pkg com.example
  common_fields: &fields
    - name: id
      type: Long
      primary_key: true
    - name: created_at
      type: DateTime

jobs:
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      package: *pkg
      class_name: User
      fields:
        - name: username
          type: String
        - <<: *fields         # Merge common fields
```

---

## Context Variables

The `context` passed to a template can contain:

### Scalars
```yaml
context:
  app_name: MyApp
  version: 1.0
  debug: true
```

### Lists
```yaml
context:
  fields:
    - name: id
      type: Long
    - name: name
      type: String
```

### Nested Objects
```yaml
context:
  database:
    host: localhost
    port: 5432
    credentials:
      user: admin
      password: secret
```

---

## Complete Example

```yaml
# Sommelier YAML Schema - .sommelier/schema.yaml

# Shared configuration for reuse
shared:
  java_config: &java
    package: com.example.app
    java_version: 11
    
  common_fields: &base_fields
    - name: id
      type: Long
      annotation: "@Id @GeneratedValue"
    - name: created_at
      type: LocalDateTime
      annotation: "@CreationTimestamp"

# Generation jobs (as dictionary with job names)
jobs:
  # Generate User entity from file template
  user_entity:
    template: entity.java.j2
    output: src/main/java/com/example/app/entity/User.java
    context:
      <<: *java
      class_name: User
      table_name: users
      fields:
        <<: *base_fields
        - name: username
          type: String
          annotation: "@Column(unique=true, nullable=false)"

  # Generate Product entity
  product_entity:
    template: entity.java.j2
    output: src/main/java/com/example/app/entity/Product.java
    context:
      <<: *java
      class_name: Product
      table_name: products
      fields:
        <<: *base_fields
        - name: sku
          type: String

  # Generate config with inline template
  app_config:
    template: |
      # Configuration for {{ app_name }}
      spring.application.name={{ app_name }}
      spring.jpa.hibernate.ddl-auto=update
      server.port={{ port }}
    output: src/main/resources/application.properties
    context:
      app_name: MyApp
      port: 8080

  # Generate repository
  user_repository:
    template: repository.java.j2
    output: src/main/java/com/example/app/repository/UserRepository.java
    context:
      <<: *java
      entity_name: User
      id_type: Long
```

---

## Best Practices

1. **Use job names that describe the purpose**
   ```yaml
   jobs:
     user_entity:       # Good: clear purpose
     config_file:       # Good: clear purpose
     my_job_1:          # Bad: not descriptive
   ```

2. **Use anchors for DRY configuration**
   ```yaml
   shared:
     base_package: &pkg com.example
   
   jobs:
     my_job:
       context:
         package: *pkg  # Reuse instead of repeating
   ```

3. **Organize jobs by type**
   ```yaml
   jobs:
     # Entities
     user_entity:
       ...
     product_entity:
       ...
     
     # Repositories
     user_repository:
       ...
     
     # Configuration
     app_config:
       ...
   ```

4. **Use inline templates for small content**
   ```yaml
   # Good: small inline template
   greeting:
     template: "echo {{ message }}"
     
   # Better: large template in file
   entity:
     template: entity.java.j2
   ```

5. **Use consistent context structure**
   ```yaml
   # Good: parallel structure for multiple entities
   jobs:
     user:
       context:
         class_name: User
         table_name: users
     
     product:
       context:
         class_name: Product
         table_name: products
   ```

---

## Common Errors

### Missing required key
```
Error: Job 'my_job' missing 'template' key
```
Ensure each job has `template`, `output`, and `context`.

### Invalid YAML syntax
```
YAML Error: mapping values are not allowed
```
Check for:
- Tabs (use spaces only)
- Proper indentation
- Quotes around strings with special characters

### Template not found
```
ERROR: Template not found: entity.java.j2
```
Verify:
1. File exists in `.sommelier/tmplts/`
2. Filename matches exactly (case-sensitive)
3. No custom `template_dir` is hiding the file

### Jobs must be dict, not list
```
Error: 'jobs' must be a dict/map
```
Use dict format:
```yaml
jobs:
  job_name:
    template: ...
    output: ...
    context: ...
```

Not array format:
```yaml
jobs:
  - template: ...
    output: ...
    context: ...
```
