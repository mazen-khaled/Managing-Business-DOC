# Document System

Python package for managing business documents with validation.

## Features
- **Document Base Class**  
  Provides core functionality for all business documents
- **Invoice Subclass**  
  Specialized document type with validation rules for invoices
- **Validation**  
  - Required field checks  
  - Item validation  
  - Amount limit enforcement ($10,000 max)  
  - Date format validation (YYYY-MM-DD)
- **Custom Exceptions**  
  Detailed error classes for different validation failures
- **Unit Tests**  
  Complete test coverage for all functionality

# V2: SOLID Principles Refactoring for Document System

## 1. Single Responsibility Principle (SRP) Changes
- Created separate validator classes to handle validation logic
- Updated `Document` and `Invoice` classes to separate their concerns
  - `Document` now focuses solely on document properties and core functionality
  - `Invoice` handles invoice-specific behavior separately

## 2. Open/Closed Principle (OCP) Changes
- Created abstract base validator: `DocumentValidator`
  - System is open for extension (new validators can be added)
  - Closed for modification (existing validator interface remains stable)
- New validators can be added without changing existing validation code

## 3. Liskov Substitution Principle (LSP) Changes
- Ensured all validator subclasses properly implement `validate()` method
  - All subclasses must implement `validate()` from `Document` class
  - Validator subclasses can be used interchangeably without breaking functionality
- Maintained consistent behavior across all validator implementations.

## 4. Dependency Inversion Principle (DIP) Changes
- High-level `Invoice` class now depends on `Validator` abstraction
  - Constructor pattern: `Invoice(docname, created_by, data, validator=None)` .
  - Can pass specific Validator Function or not.
- Removed direct dependencies on concrete validator implementations
- Validation logic can be easily swapped or mocked for testing

# Run Tests

```bash
python -m unittest discover -s .\tests\
