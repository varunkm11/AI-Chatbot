import datetime
import json
import os

class TrainingExample:
    def __init__(self, input_text, output_text, category="general", source="manual", created_at=None):
        self.input_text = input_text
        self.output_text = output_text
        self.category = category
        self.source = source
        self.created_at = created_at or datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            'input_text': self.input_text,
            'output_text': self.output_text,
            'category': self.category,
            'source': self.source,
            'created_at': self.created_at
        }

class Document:
    def __init__(self, content, title, category="general"):
        self.content = content
        self.title = title
        self.category = category

    def to_dict(self):
        return {
            'content': self.content,
            'title': self.title,
            'category': self.category
        }

class TrainingDataManager:
    def __init__(self):
        self.examples = []
        self.documents = []
    
    def add_example(self, example):
        self.examples.append(example)
    
    def get_examples(self, category=None):
        if category:
            return [ex for ex in self.examples if ex.category == category]
        return self.examples
    
    def add_document(self, document):
        self.documents.append(document)
    
    def get_documents(self, category=None):
        if category:
            return [doc for doc in self.documents if doc.category == category]
        return self.documents

class SimpleRAGSystem:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def retrieve(self, query, limit=5):
        # Simple keyword-based retrieval
        examples = self.data_manager.get_examples()
        return examples[:limit]  # Return first 'limit' examples
    
    def generate_response(self, query, context_examples):
        # Simple response generation based on examples
        if not context_examples:
            return "I don't have enough information to answer that question."
        
        # Find the most relevant example (simple string matching)
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        for example in context_examples:
            input_lower = example.input_text.lower()
            # Simple scoring based on common words
            common_words = set(query_lower.split()) & set(input_lower.split())
            score = len(common_words)
            
            if score > best_score:
                best_score = score
                best_match = example
        
        if best_match and best_score > 0:
            return best_match.output_text
        
        return "I'm not sure about that. Could you please rephrase your question?"

class FinetuningDataPrep:
    def __init__(self):
        pass
    
    def prepare_for_training(self, examples):
        """Prepare training examples for fine-tuning format"""
        training_data = []
        for example in examples:
            training_data.append({
                "messages": [
                    {"role": "user", "content": example.input_text},
                    {"role": "assistant", "content": example.output_text}
                ]
            })
        return training_data
    
    def export_jsonl(self, examples, filename):
        """Export training data to JSONL format"""
        training_data = self.prepare_for_training(examples)
        with open(filename, 'w', encoding='utf-8') as f:
            for item in training_data:
                f.write(json.dumps(item) + '\n')

class DataImporter:
    def __init__(self):
        pass
    
    def import_from_json(self, file_path):
        """Import training examples from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            examples = []
            for item in data:
                example = TrainingExample(
                    input_text=item.get('input_text', ''),
                    output_text=item.get('output_text', ''),
                    category=item.get('category', 'general'),
                    source=item.get('source', 'import')
                )
                examples.append(example)
            
            return examples
        except Exception as e:
            print(f"Error importing data: {e}")
            return []
    
    def import_from_csv(self, file_path):
        """Import training examples from CSV file"""
        examples = []
        try:
            # Simple CSV parsing without pandas
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # Skip header
                    for line in lines[1:]:
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            example = TrainingExample(
                                input_text=parts[0].strip('"'),
                                output_text=parts[1].strip('"'),
                                category=parts[2].strip('"') if len(parts) > 2 else 'general',
                                source='csv_import'
                            )
                            examples.append(example)
        except Exception as e:
            print(f"Error importing CSV data: {e}")
        
        return examples
