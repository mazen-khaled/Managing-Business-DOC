from .Document import Document
from document_system.validators.InvoiceValidator import InvoiceValidator

# document/document.py
class Invoice(Document):
    def __init__(self, docname: str, created_by: str, data: dict, validator=None):
        super().__init__(docname, created_by, data)
        self.validator = validator or InvoiceValidator()
    
    def validate(self):
        self.validator.validate(self)