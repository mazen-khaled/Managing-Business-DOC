from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, docname: str, created_by: str, data: dict):
        self.docname = docname
        self.created_by = created_by
        self.data = data
        self.status = "Draft"
    
    def submit(self):
        self.validate()
        self.status = "Submitted"
    
    @abstractmethod
    def validate(self):
        pass