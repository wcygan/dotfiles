# /schema

Comprehensive database schema and data management command.

## Usage
```
/schema <action> [options]
```

## Actions

### Migration Management
```
/schema migrate <description>
/schema migrate --rollback <migration_id>
```

### CRUD Generation
```
/schema crud --for <model>
/schema crud --for <model> --lang <go|rust|java>
```

### Data Seeding
```
/schema seed --for <model> --count <number>
/schema seed --all --env <development|test>
```

## Description
This command automates database schema management, CRUD boilerplate generation, and test data creation. It supports multiple database migration tools and programming languages.

### Migration Management
Creates versioned database migration files with proper UP/DOWN scripts:

**Supported Migration Tools:**
- **golang-migrate**: Creates `.sql` files with timestamp prefixes
- **Flyway**: Creates `V{version}__{description}.sql` files
- **Diesel (Rust)**: Creates migration files in `migrations/` directory
- **Liquibase**: Creates XML/YAML changelog files

**Generated Migration Structure:**
```sql
-- migrations/000001_add_user_email_verification.up.sql
ALTER TABLE users 
ADD COLUMN email_verification_token VARCHAR(255),
ADD COLUMN email_verified_at TIMESTAMP;

CREATE INDEX idx_users_verification_token 
ON users(email_verification_token);

-- migrations/000001_add_user_email_verification.down.sql
DROP INDEX idx_users_verification_token;
ALTER TABLE users 
DROP COLUMN email_verification_token,
DROP COLUMN email_verified_at;
```

### CRUD Generation
Analyzes model structures and generates complete data access layers:

**Go Example (with sqlx):**
```go
type UserRepository struct {
    db *sqlx.DB
}

func (r *UserRepository) Create(ctx context.Context, user *User) error {
    query := `INSERT INTO users (name, email, created_at) VALUES ($1, $2, $3) RETURNING id`
    return r.db.QueryRowContext(ctx, query, user.Name, user.Email, user.CreatedAt).Scan(&user.ID)
}

func (r *UserRepository) GetByID(ctx context.Context, id int64) (*User, error) {
    // Implementation...
}
```

**Rust Example (with sqlx):**
```rust
impl UserRepository {
    pub async fn create(&self, user: &User) -> Result<User, sqlx::Error> {
        let row = sqlx::query_as!(
            User,
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
            user.name,
            user.email
        )
        .fetch_one(&self.pool)
        .await?;
        Ok(row)
    }
}
```

**Java Example (with Spring Data JPA):**
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end);
    
    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> findByNameContaining(@Param("name") String name);
}
```

### Data Seeding
Generates realistic test data for development and testing:

**Features:**
- **Realistic Data**: Uses libraries like Faker to generate believable data
- **Relationship Handling**: Maintains foreign key constraints
- **Configurable Volume**: Specify exact counts or ranges
- **Environment Safety**: Prevents accidental production seeding

**Generated Seed Script Example:**
```sql
-- seeds/users_seed.sql
INSERT INTO users (name, email, created_at) VALUES
('Alice Johnson', 'alice.johnson@example.com', '2024-01-15 10:30:00'),
('Bob Smith', 'bob.smith@example.com', '2024-01-16 14:22:00'),
('Carol Davis', 'carol.davis@example.com', '2024-01-17 09:15:00');

-- Maintains relationships
INSERT INTO posts (user_id, title, content) VALUES
(1, 'Getting Started with Go', 'Here are some tips...'),
(1, 'Database Best Practices', 'When working with databases...'),
(2, 'Rust Performance Tips', 'Optimizing Rust code...');
```

## Framework Integration

### Database Tools Detected:
- **Go**: `golang-migrate`, `goose`, `atlas`, `ent`
- **Rust**: `diesel`, `sqlx`, `sea-orm`
- **Java**: `Flyway`, `Liquibase`, `JPA/Hibernate`
- **Node/Deno**: `Prisma`, `TypeORM`, `Drizzle`

### ORM Pattern Recognition:
Automatically detects and follows existing patterns:
- Repository pattern (Go, Java)
- Active Record pattern (Ruby, some JS ORMs)
- Query Builder pattern (Rust sqlx)
- Data Mapper pattern (TypeORM)

## Examples

### Create a migration:
```
/schema migrate "add-user-email-verification-token"
```

### Generate CRUD for Go model:
```
/schema crud --for User --lang go
```

### Seed development data:
```
/schema seed --for User --count 50
/schema seed --all --env development
```

### Rollback migration:
```
/schema migrate --rollback 20240315143022
```

## Configuration
Respects existing database configuration files:
- `database.yml` (Rails-style)
- `dbconfig.yml` (golang-migrate)
- `application.properties` (Spring)
- `diesel.toml` (Diesel)

## Safety Features
- **Environment Checks**: Prevents destructive operations in production
- **Backup Recommendations**: Suggests backup commands before migrations
- **Dry Run Mode**: Preview changes without executing
- **Transaction Wrapping**: Wraps migrations in transactions when supported

## Integration with Other Commands
- Use with `/containerize` to include migration steps in Docker builds
- Combine with `/ci-gen` to add database testing to CI pipelines
- Use with `/deploy` to automate migrations during deployments