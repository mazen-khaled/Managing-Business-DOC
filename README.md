# Document System

Python package for managing business documents with validation and Follows Soild Principles.

## Features

- **Document Base Class**  
  Core functionality for all business documents including:
  - Document identification (name, creator)
  - Status tracking (Draft → Submitted)
  - Basic validation requirements

- **Specialized Document Types**  
  - `Invoice`: Handles financial transactions with:
    - Customer information
    - Line items with quantities and rates
    - Posting date requirements

- **Validation Framework**  
  Comprehensive validation including:
  - **Field Validation**:
    - Required field checks (`customer`, `items`, `posting_date`)
    - Date format validation (YYYY-MM-DD)
  - **Business Rules**:
    - Item structure validation (description, qty, rate)
    - Amount limit enforcement (configurable $10,000 default max)
    - Numeric value validation for financial fields

- **Error Handling**  
  Hierarchical custom exceptions:
  - `ValidationError` (base)
    - `MissingFieldError`
    - `ItemValidationError`
    - `AmountExceededError`

- **Extensibility**  
  Designed for adding new document types:
  - Purchase orders
  - Receipts
  - Contracts

- **Testing**  
  100% test coverage including:
  - Happy path validation
  - Edge cases
  - Error conditions

## SOLID Principles Implementation

### 1. Single Responsibility Principle (SRP)

**Implementation**:
- `Document`: Manages core document properties and lifecycle
- `Invoice`: Handles invoice-specific data structure
- `InvoiceValidator`: Contains all validation logic
- Separate exception classes for different error types

**Benefits**:
- Changes to validation don't affect document core
- Clear separation between business logic and validation
- Easier maintenance and testing

### 2. Open/Closed Principle (OCP)

**Implementation**:
- Abstract `DocumentValidator` base class
- Closed core system with:

```python
class DocumentValidator(ABC):
    @abstractmethod
    def validate(self, document):
        ...
```

Open for extension through:
- New validator implementations
- New document subclasses

```python
class CustomInvoiceValidator(InvoiceValidator):
    def __init__(self, max_amount=15000):
        self.max_amount = max_amount
```

### 3. Liskov Substitution Principle (LSP)
**Implementation**:
- All validators implement same interface:
```python
def validate(self, document):
    # Must implement full validation
```
- Invoice can substitute Document:

```python
def process_document(doc: Document):
    # Works with any Document subclass
```

## Guarantees:

- Validator subclasses don't weaken preconditions
- Document subclasses don't strengthen postconditions
- No surprise behaviors in inheritance

## 4. Interface Segregation Principle (ISP)

### Implementation:

**Minimal validator interface:**

```python
class DocumentValidator(ABC):
    @abstractmethod
    def validate(self, document):
        ...
```
- Clients only depend on needed methods
- No "fat interfaces" forcing unused method implementation

**Benefits:**
- No need to implement irrelevant methods
- Clear contract between components
- Easier mocking for testing

## 5. Dependency Inversion Principle (DIP)
**Implementation:**

High-level Invoice depends on DocumentValidator abstraction

Constructor injection pattern:
```python
def __init__(self, docname: str, created_by: str, 
             data: dict, validator=None):
    self.validator = validator or InvoiceValidator()

```

**Benefits:**
- Easy validator swapping for different scenarios
- Simplified unit testing with mock validators
- Runtime validator configuration

## **Usage Examples**
**Basic Usage:**
```python
from document_system import Invoice

data = {
    "customer": "Acme Corp",
    "posting_date": "2024-01-15",
    "items": [
        {"description": "Web Design", "qty": 10, "rate": 75}
    ]
}

invoice = Invoice("INV-2024-001", "sales1", data)
invoice.validate()
invoice.submit()
```
**Custom Validation:**
```python
from document_system import Invoice, CustomInvoiceValidator

validator = CustomInvoiceValidator(max_amount=20000)
invoice = Invoice("INV-2024-002", "sales1", data, validator)
```

## Run All Tests
```bash
python -m unittest discover -s tests
```


**Architecture Diagram**
```text
Document (ABC)
    ↑
Invoice ───┐
           │
           ↓
InvoiceValidator → DocumentValidator (ABC)
           |
           ├── Validates: Required Fields
           ├── Validates: Item Structure
           └── Validates: Business Rules
```
