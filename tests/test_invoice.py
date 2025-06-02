import unittest
from datetime import datetime
from document_system import Invoice
from document_system import (MissingFieldError, ItemValidationError, 
                         AmountExceededError, ValidationError)

class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            'customer': 'Mazen Khaled',
            'posting_date': '2024-05-02',
            'items': [
                {'description': 'Item 1', 'qty': 2, 'rate': 100},
                {'description': 'Item 2', 'qty': 1, 'rate': 200}
            ]
        }
    
    def test_valid_invoice(self):
        invoice = Invoice('INV-001', 'admin', self.valid_data)
        invoice.validate()  # Should not raise
        invoice.submit()
        self.assertEqual(invoice.status, 'Submitted')
    
    def test_missing_required_field(self):
        for field in ['customer', 'items', 'posting_date']:
            data = self.valid_data.copy()
            data.pop(field)
            invoice = Invoice('INV-001', 'admin', data)
            with self.assertRaises(MissingFieldError):
                invoice.validate()
    
    def test_invalid_items(self):
        # Test non-list items
        data = self.valid_data.copy()
        data['items'] = 'not a list'
        invoice = Invoice('INV-001', 'admin', data)
        with self.assertRaises(ValidationError):
            invoice.validate()
        
        # Test missing item fields
        for field in ['description', 'qty', 'rate']:
            data = self.valid_data.copy()
            data['items'][0].pop(field)
            invoice = Invoice('INV-001', 'admin', data)
            with self.assertRaises(ItemValidationError):
                invoice.validate()
    
    def test_amount_exceeded(self):
        data = self.valid_data.copy()
        data['items'].append({'description': 'Expensive', 'qty': 100, 'rate': 200})
        invoice = Invoice('INV-001', 'admin', data)
        with self.assertRaises(AmountExceededError):
            invoice.validate()
    
    def test_invalid_posting_date(self):
        data = self.valid_data.copy()
        data['posting_date'] = 'not-a-date'
        invoice = Invoice('INV-001', 'admin', data)
        with self.assertRaises(ValidationError):
            invoice.validate()

if __name__ == '__main__':
    unittest.main()