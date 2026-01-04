# Mermaid Syntax Quick Reference

This document provides essential Mermaid syntax for creating UML diagrams. For complex scenarios, refer to examples in the `examples/` directory.

## Basic Structure

All Mermaid diagrams start with a type declaration:

```mermaid
<diagram-type>
    <diagram-content>
```

## 1. Class Diagram

### Basic Syntax

```mermaid
classDiagram
    class ClassName {
        +public_attribute: type
        -private_attribute: type
        #protected_attribute: type
        +public_method(param: type) return_type
        -private_method()
    }
```

### Relationships

```mermaid
classDiagram
    ClassA <|-- ClassB : Inheritance
    ClassA *-- ClassB : Composition
    ClassA o-- ClassB : Aggregation
    ClassA --> ClassB : Association
    ClassA ..> ClassB : Dependency
    ClassA ..|> ClassB : Realization
```

### Visibility Modifiers

- `+` Public
- `-` Private
- `#` Protected
- `~` Package/Internal

## 2. Sequence Diagram

### Basic Syntax

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    
    A->>B: Synchronous message
    B-->>A: Response
    A-)B: Async message
    B--)A: Async response
```

### Advanced Features

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB
    
    User->>API: Request
    activate API
    API->>DB: Query
    activate DB
    DB-->>API: Data
    deactivate DB
    API-->>User: Response
    deactivate API
    
    Note over User,API: This is a note
    
    alt Success case
        API-->>User: 200 OK
    else Error case
        API-->>User: 500 Error
    end
    
    loop Every 10s
        API->>DB: Heartbeat
    end
```

### Message Types

- `->` Solid line without arrow
- `-->` Dotted line without arrow
- `->>` Solid line with arrow
- `-->>` Dotted line with arrow
- `-x` Solid line with X
- `--x` Dotted line with X
- `-)` Async solid line
- `--)` Async dotted line

## 3. Flowchart

### Basic Syntax

```mermaid
flowchart TD
    A[Rectangle] --> B{Diamond}
    B -->|Yes| C[Process]
    B -->|No| D[End]
```

### Node Shapes

```mermaid
flowchart LR
    A[Rectangle]
    B(Rounded)
    C([Stadium])
    D[[Subroutine]]
    E[(Database)]
    F((Circle))
    G>Flag]
    H{Diamond}
    I{{Hexagon}}
```

### Directions

- `TD` / `TB` - Top to Down/Bottom
- `BT` - Bottom to Top
- `LR` - Left to Right
- `RL` - Right to Left

## 4. State Diagram

### Basic Syntax

```mermaid
stateDiagram-v2
    [*] --> State1
    State1 --> State2 : Event
    State2 --> [*]
    
    State2: This is State2
    State2: It can have
    State2: Multiple lines
```

### Composite States

```mermaid
stateDiagram-v2
    [*] --> Active
    
    state Active {
        [*] --> Processing
        Processing --> Validating
        Validating --> [*]
    }
    
    Active --> Inactive : timeout
    Inactive --> [*]
```

## 5. ER Diagram

### Basic Syntax

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

### Relationship Cardinality

- `||--||` One to one
- `||--o{` One to many
- `}o--o{` Many to many
- `||..|{` Zero or more

### Entity Attributes

```mermaid
erDiagram
    CUSTOMER {
        string name
        string email PK
        int age
    }
    ORDER {
        int id PK
        date order_date
        string status FK
    }
    CUSTOMER ||--o{ ORDER : places
```

## 6. Graph/Architecture Diagram

### Basic Syntax

```mermaid
graph TD
    A[Client] --> B[API Gateway]
    B --> C[Service 1]
    B --> D[Service 2]
    C --> E[(Database)]
    D --> E
```

### Subgraphs

```mermaid
graph TB
    subgraph Frontend
        A[UI]
        B[State Management]
    end
    
    subgraph Backend
        C[API]
        D[Business Logic]
        E[(DB)]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
```

## Styling Tips

### Custom Styles

```mermaid
classDiagram
    class Important
    class Normal
    
    style Important fill:#f9f,stroke:#333,stroke-width:4px
    style Normal fill:#bbf,stroke:#333,stroke-width:2px
```

### CSS Classes

```mermaid
graph LR
    A:::highlight --> B
    B --> C:::highlight
    
    classDef highlight fill:#f96,stroke:#333,stroke-width:4px
```

## Best Practices

1. **Keep It Simple** - One diagram should focus on one aspect
2. **Use Meaningful Names** - Use actual code names, not generic ones
3. **Add Annotations** - Use `Note` blocks to clarify complex parts
4. **Consistent Naming** - Keep naming consistent across diagrams
5. **Test Rendering** - Verify diagrams render correctly on GitHub/GitLab

## Common Pitfalls

- **Syntax Errors** - Missing colons, brackets, or quotes
- **Name Mismatches** - UML names don't match actual code
- **Too Complex** - Too many elements in one diagram
- **Wrong Diagram Type** - Using wrong diagram for the use case

## Testing Your Diagrams

Test your Mermaid code:
- [Mermaid Live Editor](https://mermaid.live/)
- GitHub/GitLab Markdown preview
- VS Code with Mermaid extension

## Further Reading

For complete syntax reference:
- [Mermaid Official Documentation](https://mermaid.js.org/)
- Examples in `examples/` directory

