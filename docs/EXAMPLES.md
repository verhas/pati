# Real-World Examples

Complete working examples showing Sommelier in action.

## Example 1: Java Spring Boot Entity

Generate a JPA entity with associated DTO and repository.

### Schema (.sommelier/schema.yaml)

```yaml
shared: &java
  package: com.example.app

jobs:
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      <<: *java
      class_name: User
      table_name: users
      fields:
        - name: id
          type: Long
          annotation: "@Id @GeneratedValue"
        - name: username
          type: String
          annotation: "@Column(nullable = false, unique = true)"
        - name: email
          type: String
          annotation: "@Column(nullable = false)"

  user_dto:
    template: dto.java.j2
    output: generated/UserDTO.java
    context:
      <<: *java
      class_name: UserDTO
      fields:
        - name: id
          type: Long
        - name: username
          type: String
        - name: email
          type: String

  user_repository:
    template: repository.java.j2
    output: generated/UserRepository.java
    context:
      <<: *java
      entity_name: User
      entity_type: User
      id_type: Long
```

### Template (.sommelier/tmplts/entity.java.j2)

```jinja2
package {{ package }}.entity;

import javax.persistence.*;

@Entity
@Table(name = "{{ table_name }}")
public class {{ class_name }} {

{% for field in fields %}
    {{ field.annotation }}
    private {{ field.type }} {{ field.name }};

{% endfor %}
    public {{ class_name }}() {
    }

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

### Usage

```bash
# Generate
sommelier generate

# Or with dry-run
sommelier generate --dry-run
```

### Generated Output (generated/User.java)

```java
package com.example.app.entity;

import javax.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id @GeneratedValue
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String email;

    public User() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

}
```

---

## Example 2: Inline Templates for Configuration

Generate configuration files with inline templates.

### Schema (.sommelier/schema.yaml)

```yaml
jobs:
  app_properties:
    template: |
      # Application Configuration
      spring.application.name={{ app_name }}
      spring.profiles.active={{ env }}
      server.port={{ port }}
      spring.datasource.url=jdbc:postgresql://{{ db_host }}:{{ db_port }}/{{ db_name }}
      spring.datasource.username={{ db_user }}
      spring.jpa.hibernate.ddl-auto=update
    output: generated/application.properties
    context:
      app_name: MyApp
      env: development
      port: 8080
      db_host: localhost
      db_port: 5432
      db_name: myapp_db
      db_user: postgres

  docker_compose:
    template: |
      version: '3.8'
      services:
        postgres:
          image: postgres:{{ postgres_version }}
          environment:
            POSTGRES_DB: {{ db_name }}
            POSTGRES_USER: {{ db_user }}
            POSTGRES_PASSWORD: {{ db_password }}
          ports:
            - "{{ db_port }}:5432"
    output: generated/docker-compose.yml
    context:
      postgres_version: '14'
      db_name: myapp_db
      db_user: postgres
      db_password: mysecret
      db_port: 5432

  bash_script:
    template: |
      #!/bin/bash
      # Setup script for {{ app_name }}
      echo "Setting up {{ app_name }}..."
      echo "Environment: {{ env }}"
      echo "Database: {{ db_name }}"
    output: generated/setup.sh
    context:
      app_name: MyApp
      env: development
      db_name: myapp_db
```

### Usage

```bash
sommelier generate
```

### Generated Files

**generated/application.properties**
```properties
# Application Configuration
spring.application.name=MyApp
spring.profiles.active=development
server.port=8080
...
```

**generated/docker-compose.yml**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: myapp_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mysecret
    ports:
      - "5432:5432"
```

---

## Example 3: Mixed File and Inline Templates

Combine file templates with inline templates in one schema.

### Schema (.sommelier/schema.yaml)

```yaml
shared:
  model_config: &model
    package: com.example
    lang: java

jobs:
  # Use file template
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      <<: *model
      class_name: User
      fields:
        - name: id
          type: Long
        - name: username
          type: String

  # Use inline template
  readme:
    template: |
      # {{ project_name }} - API Documentation

      ## Models
      {% for model in models %}
      - `{{ model }}`
      {% endfor %}

      ## Quick Start
      ```bash
      mvn spring-boot:run
      ```

      Generated by Sommelier
    output: generated/README.md
    context:
      project_name: MyAPI
      models:
        - User
        - Product
        - Order

  # Another file template
  migration:
    template: migration.sql.j2
    output: generated/001_create_users.sql
    context:
      table_name: users
      columns:
        - name: id
          type: BIGINT PRIMARY KEY AUTO_INCREMENT
        - name: username
          type: VARCHAR(255) NOT NULL UNIQUE
```

---

## Example 4: Complex Job Organization

Organize multiple related jobs with shared configuration.

### Schema (.sommelier/schema.yaml)

```yaml
shared:
  java_base: &java
    package: com.example.app
    java_version: 11

  common_fields: &common
    - name: id
      type: Long
      annotation: "@Id @GeneratedValue"
    - name: created_at
      type: LocalDateTime
      annotation: "@CreationTimestamp"
    - name: updated_at
      type: LocalDateTime
      annotation: "@UpdateTimestamp"

jobs:
  # Generate entities
  user_entity:
    template: entity.java.j2
    output: generated/User.java
    context:
      <<: *java
      class_name: User
      table_name: users
      fields:
        <<: *common
        - name: username
          type: String

  product_entity:
    template: entity.java.j2
    output: generated/Product.java
    context:
      <<: *java
      class_name: Product
      table_name: products
      fields:
        <<: *common
        - name: sku
          type: String

  # Generate repositories
  user_repository:
    template: repository.java.j2
    output: generated/UserRepository.java
    context:
      <<: *java
      entity_name: User

  product_repository:
    template: repository.java.j2
    output: generated/ProductRepository.java
    context:
      <<: *java
      entity_name: Product

  # Generate documentation
  entities_doc:
    template: |
      # Entity Definitions

      ## User
      - id (Long, primary key)
      - username (String)
      - created_at (LocalDateTime)
      - updated_at (LocalDateTime)

      ## Product
      - id (Long, primary key)
      - sku (String)
      - created_at (LocalDateTime)
      - updated_at (LocalDateTime)

      Generated by Sommelier
    output: generated/ENTITIES.md
    context: {}
```

---

## Tips and Tricks

### 1. Use Descriptive Job Names

```yaml
jobs:
  user_entity:        # Good
  product_dto:        # Good
  j1:                 # Bad: not descriptive
```

### 2. Mix File and Inline Templates

- **File templates**: Large, reusable across projects
- **Inline templates**: Small, configuration-specific

```yaml
jobs:
  entity:
    template: entity.java.j2          # File template
  
  config:
    template: |
      app={{ name }}
```

### 3. Organize by Type

Group related jobs together in your schema:

```yaml
jobs:
  # Entities
  user_entity:
  product_entity:

  # Repositories
  user_repository:
  product_repository:

  # Configuration
  app_config:
  docker_config:
```

### 4. Use Anchors for DRY Configuration

```yaml
shared:
  common: &common
    author: John Doe
    license: MIT

jobs:
  file1:
    context:
      <<: *common
      extra: value
```

### 5. Generate Multiple Variants

```yaml
jobs:
  dev_config:
    template: |
      ENV=development
      DEBUG=true
    output: generated/dev.env
    context: {}

  prod_config:
    template: |
      ENV=production
      DEBUG=false
    output: generated/prod.env
    context: {}
```

### 6. Version Control Your Schema

```bash
git add .sommelier/schema.yaml
git add .sommelier/tmplts/
```

Track changes to your data model and templates over time.

### 7. Use Environment Variables in Inline Templates

```yaml
context:
  db_host: "{{ lookup('env', 'DB_HOST') | default('localhost') }}"
```

Note: This requires Jinja2 environment setup. By default, use simple context values.
