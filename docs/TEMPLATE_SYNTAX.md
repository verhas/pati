# Jinja2 Template Syntax Reference

Sommelier uses Jinja2 for template rendering. This guide covers the essentials.

**Note:** Templates can be either:
- **File-based**: Reference a template file in `.sommelier/tmplts/`
- **Inline**: Define template content directly in `.sommelier/schema.yaml`

For complete documentation, see the [official Jinja2 docs](https://jinja.palletsprojects.com/).

## File-based vs Inline Templates

### File Template
```yaml
jobs:
  my_entity:
    template: entity.java.j2          # Reference file in tmplts/
    output: generated/Entity.java
    context:
      name: User
```

### Inline Template
```yaml
jobs:
  my_entity:
    template: |                       # Multiline template string
      public class {{ name }} {
        // Generated
      }
    output: generated/Entity.java
    context:
      name: User
```

## Variables

Insert variable values with double curly braces:

```jinja2
{{ variable_name }}
{{ context.nested.value }}
{{ user['email'] }}
```

### Examples

Template:
```jinja2
Hello {{ name }}!
```

Context:
```yaml
context:
  name: Alice
```

Output:
```
Hello Alice!
```

---

## Filters

Transform variables with filters using the pipe syntax:

```jinja2
{{ value | filter_name }}
{{ value | filter1 | filter2 }}
```

### Common Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `upper` | Uppercase | `{{ name \| upper }}` → `ALICE` |
| `lower` | Lowercase | `{{ name \| lower }}` → `alice` |
| `capitalize` | Capitalize first letter | `{{ name \| capitalize }}` → `Alice` |
| `title` | Title case | `{{ "hello world" \| title }}` → `Hello World` |
| `length` | String/list length | `{{ items \| length }}` → `3` |
| `default` | Default value | `{{ value \| default("N/A") }}` |
| `join` | Join list items | `{{ items \| join(", ") }}` |
| `sort` | Sort list | `{{ items \| sort }}` |
| `reverse` | Reverse list | `{{ items \| reverse }}` |
| `first` | First item | `{{ items \| first }}` |
| `last` | Last item | `{{ items \| last }}` |
| `replace` | String replace | `{{ text \| replace("old", "new") }}` |

### Examples

```jinja2
{% for field in fields %}
    private {{ field.type }} {{ field.name | lower }};
{% endfor %}

{{ description | default("No description") }}

{{ tags | join(", ") }}
```

---

## Control Structures

### If/Else Conditionals

```jinja2
{% if condition %}
    content
{% elif other_condition %}
    other content
{% else %}
    default content
{% endif %}
```

### Examples

```jinja2
{% if field.nullable %}
    @Column(nullable = true)
{% else %}
    @Column(nullable = false)
{% endif %}

{% if field.primary_key %}
    @Id
{% endif %}
```

### For Loops

```jinja2
{% for item in items %}
    {{ item }}
{% endfor %}
```

### Loop Variables

Inside loops, access loop metadata:

```jinja2
{% for item in items %}
    {% if loop.first %}
        First item: {{ item }}
    {% endif %}
    
    Item #{{ loop.index }} (1-indexed)
    Item #{{ loop.index0 }} (0-indexed)
    
    {% if loop.last %}
        Last item: {{ item }}
    {% endif %}
{% endfor %}
```

### Loop Metadata

| Variable | Description |
|----------|-------------|
| `loop.index` | Current iteration (1-indexed) |
| `loop.index0` | Current iteration (0-indexed) |
| `loop.first` | True if first iteration |
| `loop.last` | True if last iteration |
| `loop.length` | Total number of items |
| `loop.revindex` | Remaining iterations (reverse) |
| `loop.revindex0` | Remaining iterations (reverse, 0-indexed) |

### Examples

```jinja2
{% for field in fields %}
    private {{ field.type }} {{ field.name }};
    {% if not loop.last %},{% endif %}
{% endfor %}
```

---

## Complex Example

### Template (entity.java.j2)

```jinja2
package {{ package }}.entity;

import javax.persistence.*;

@Entity
@Table(name = "{{ table_name }}")
public class {{ class_name }} {

{% for field in fields %}
    {% if field.primary_key %}
    @Id
    @GeneratedValue
    {% endif %}
    {% if field.unique %}
    @Column(unique = true, nullable = false)
    {% elif field.nullable %}
    @Column(nullable = true)
    {% else %}
    @Column(nullable = false)
    {% endif %}
    private {{ field.type }} {{ field.name }};

{% endfor %}
    // Constructors
    public {{ class_name }}() {
    }

    public {{ class_name }}(
{% for field in fields %}
            {{ field.type }} {{ field.name }}{{ "," if not loop.last else "" }}
{% endfor %}
    ) {
{% for field in fields %}
        this.{{ field.name }} = {{ field.name }};
{% endfor %}
    }

    // Getters and Setters
{% for field in fields %}
    public {{ field.type }} get{{ field.name | capitalize }}() {
        return {{ field.name }};
    }

    public void set{{ field.name | capitalize }}({{ field.type }} {{ field.name }}) {
        this.{{ field.name }} = {{ field.name }};
    }

{% endfor %}
}
```

### Context

```yaml
context:
  package: com.example.app
  class_name: User
  table_name: users
  fields:
    - name: id
      type: Long
      primary_key: true
    - name: username
      type: String
      unique: true
    - name: email
      type: String
      nullable: false
    - name: status
      type: String
      nullable: true
```

### Output

```java
package com.example.app.entity;

import javax.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue
    @Column(nullable = false)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String email;

    @Column(nullable = true)
    private String status;

    // ... rest of class
}
```

---

## Comments

```jinja2
{# This is a comment and won't appear in output #}
```

---

## Whitespace Control

By default, Jinja2 preserves whitespace. Control it with `-`:

```jinja2
{%- for item in items %}
    {{ item }}
{%- endfor %}
```

The `-` removes whitespace before/after the tag.

---

## Best Practices

1. **Use filters for transformations**
   ```jinja2
   {{ field_name | lower }}  # Good
   {{ field_name }}          # Less ideal if you need lowercase
   ```

2. **Check for existence with default**
   ```jinja2
   {{ description | default("No description available") }}
   ```

3. **Keep templates readable**
   ```jinja2
   {# Good: clear intent #}
   {% if field.is_required %}
       @NotNull
   {% endif %}
   
   {# Less clear #}
   {% if field.is_required %}@NotNull{% endif %}
   ```

4. **Use loop.last to avoid trailing commas**
   ```jinja2
   {% for item in items %}
       {{ item }}{{ "," if not loop.last else "" }}
   {% endfor %}
   ```

5. **Document complex logic**
   ```jinja2
   {# Generate getter method for {{ field.name }} #}
   public {{ field.type }} get{{ field.name | capitalize }}() {
       return {{ field.name }};
   }
   ```

---

## Common Patterns

### Conditional Decorators

```jinja2
{% if field.primary_key %}@Id{% endif %}
{% if field.unique %}@Unique{% endif %}
{% if field.nullable %}@Nullable{% endif %}
private {{ field.type }} {{ field.name }};
```

### Comma-Separated Lists

```jinja2
{{ fields | map(attribute='name') | join(', ') }}
```

### Multiple Lines with Indentation

```jinja2
public void methodName(
{%- for param in parameters %}
    {{ param.type }} {{ param.name }}{{ "," if not loop.last else "" }}
{%- endfor %}
) {
    // method body
}
```

### Conditional Sections

```jinja2
{% if include_javadoc %}
/**
 * Entity for {{ class_name }}
 */
{% endif %}
public class {{ class_name }} {
    // ...
}
```
