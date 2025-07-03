# Scaffold Java Quarkus with Spring Compatibility

## Description

Creates a new Java project using Quarkus framework with Spring Boot compatibility layer, providing supersonic startup times with familiar Spring APIs.

## Usage

```
/scaffold-java-quarkus [project-name]
```

## What it does

1. Creates a new directory with the specified project name
2. Sets up Maven pom.xml with Quarkus BOM and Spring Web compatibility
3. Creates a Spring-style REST controller using familiar annotations
4. Configures standard Maven directory structure
5. Runs `mvn clean install` to verify setup and download dependencies

## Example

```
/scaffold-java-quarkus quarkus-spring-app
```

This creates a production-ready Quarkus application with:

- Spring Web compatibility for familiar @RestController syntax
- Maven build configuration with Quarkus plugins
- Java 21 target with proper encoding settings
- REST endpoint at `/greeting`
- Quarkus development mode capabilities
- Fast startup and low memory footprint
