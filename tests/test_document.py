import unittest
from datetime import datetime
from document_system.document import Document
from document_system.exceptions import ValidationError

class TestDocument(unittest.TestCase):
    def setUp(self):
        self.doc_data = {'field1': 'value1'}
        self.doc = Document('TEST-001', 'admin', self.doc_data)
    
    def test_initialization(self):
        self.assertEqual(self.doc.docname, 'TEST-001')
        self.assertEqual(self.doc.created_by, 'admin')
        self.assertEqual(self.doc.data, self.doc_data)
        self.assertEqual(self.doc.status, 'Draft')

if __name__ == '__main__':
    unittest.main()