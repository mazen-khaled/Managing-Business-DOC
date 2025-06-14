from .DocumentValidator import DocumentValidator
from datetime import datetime
from document_system.exceptions.exceptions import (
    ValidationError, MissingFieldError,
    ItemValidationError, AmountExceededError
)

class InvoiceValidator(DocumentValidator):
    required_fields = ['customer', 'items', 'posting_date']
    item_fields = ['description', 'qty', 'rate']
    max_amount = 10000
    
    def validate(self, invoice):
        self._validate_required_fields(invoice)
        self._validate_items(invoice)
        self._validate_amount(invoice)
    
    def _validate_required_fields(self, invoice):
        for field in self.required_fields:
            if field not in invoice.data:
                raise MissingFieldError(f"Missing required field: {field}")
            
        if not isinstance(invoice.data['posting_date'], str):
            raise ItemValidationError("posting_date must be a string in YYYY-MM-DD format")
                
        try:
            datetime.strptime(invoice.data['posting_date'], '%Y-%m-%d')
        except ValueError:
            raise ValidationError("posting_date must be in YYYY-MM-DD format")
    
    def _validate_items(self, invoice):
        if not isinstance(invoice.data['items'], list):
            raise ValidationError("items must be a list")
            
        for i, item in enumerate(invoice.data['items']):
            if not isinstance(item, dict):
                raise ItemValidationError(f"Item {i} must be a dictionary")
                
            for field in self.item_fields:
                if field not in item:
                    raise ItemValidationError(
                        f"Item {i} missing required field: {field}"
                    )
                    
            try:
                float(item['qty'])
                float(item['rate'])
            except (ValueError, TypeError):
                raise ItemValidationError(
                    f"Item {i} qty and rate must be numeric"
                )
    
    def _validate_amount(self, invoice):
        total = 0.0
        for item in invoice.data['items']:
            total += float(item['qty']) * float(item['rate'])
            
        if total > self.max_amount:
            raise AmountExceededError(
                f"Total amount ${total:,.2f} exceeds maximum of ${self.max_amount:,.2f}"
            )