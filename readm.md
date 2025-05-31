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
```bash
python -m unittest discover
