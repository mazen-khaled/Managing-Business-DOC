from datetime import datetime
from .exceptions import (ValidationError, MissingFieldError, 
                        ItemValidationError, AmountExceededError)

class Document:
    
    def __init__(self, docname: str, created_by: str, data: dict):
        self.docname = docname
        self.created_by = created_by
        self.data = data
        self.status = "Draft"


class Invoice(Document):
    required_fields = ['customer', 'items', 'posting_date']
    item_fields = ['description', 'qty', 'rate']
    max_amount = 10000
    
    def validate(self):
        self._validate_required_fields()
        self._validate_items()
        self._validate_amount()
    
    def _validate_required_fields(self):
        for field in self.required_fields:
            if field not in self.data:
                raise MissingFieldError(f"Missing required field: {field}")
                
        # Validate posting_date is a valid date if provided
        if isinstance(self.data['posting_date'], str):
            try:
                datetime.strptime(self.data['posting_date'], '%Y-%m-%d')
            except ValueError:
                raise ValidationError("posting_date must be in YYYY-MM-DD format")
    
    def _validate_items(self):
        if not isinstance(self.data['items'], list):
            raise ValidationError("items must be a list")
            
        for i, item in enumerate(self.data['items']):
            if not isinstance(item, dict):
                raise ItemValidationError(f"Item {i} must be a dictionary")
                
            for field in self.item_fields:
                if field not in item:
                    raise ItemValidationError(
                        f"Item {i} missing required field: {field}"
                    )
                    
            # Validate numeric fields
            try:
                float(item['qty'])
                float(item['rate'])
            except (ValueError, TypeError):
                raise ItemValidationError(
                    f"Item {i} qty and rate must be numeric"
                )
    
    def _validate_amount(self):
        total = 0.0
        for item in self.data['items']:
            total += float(item['qty']) * float(item['rate'])
            
        if total > self.max_amount:
            raise AmountExceededError(
                f"Total amount ${total:,.2f} exceeds maximum of ${self.max_amount:,.2f}"
            )
    
    def submit(self):
        self.validate()
        self.status = "Submitted"