import datetime

class TrainingExample:
    def __init__(self, input_text, output_text, category="general", source="manual", created_at=None):
        self.input_text = input_text
        self.output_text = output_text
        self.category = category
        self.source = source
        self.created_at = created_at or datetime.datetime.utcnow().isoformat()

class Document:
    def __init__(self, content, title):
        self.content = content
        self.title = title

class TrainingDataManager:
    def __init__(self):
        self.examples = []
    def add_example(self, example):
        self.examples.append(example)
    def get_examples(self):
        return self.examples

class SimpleRAGSystem:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    def retrieve(self, query):
        # Dummy retrieval logic
        return self.data_manager.get_examples()

class FinetuningDataPrep:
    def __init__(self):
        pass
    def prepare(self, examples):
        # Dummy preparation logic
        return examples

class DataImporter:
    def __init__(self):
        pass
    def import_data(self, path):
        # Dummy import logic
        return []
