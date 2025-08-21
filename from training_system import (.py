from training_system import (
    TrainingExample, 
    Document, 
    TrainingDataManager, 
    SimpleRAGSystem, 
    FinetuningDataPrep, 
    DataImporter
)

class TestTrainingExample(unittest.TestCase):
    def test_training_example_creation_with_defaults(self):
        example = TrainingExample("What is AI?", "AI is artificial intelligence.")
        self.assertEqual(example.input_text, "What is AI?")
        self.assertEqual(example.output_text, "AI is artificial intelligence.")
        self.assertEqual(example.category, "general")
        self.assertEqual(example.source, "manual")
        self.assertIsNotNone(example.created_at)
    
    def test_training_example_with_custom_values(self):
        example = TrainingExample(
            "Test input", 
            "Test output", 
            category="test", 
            source="unittest",
            created_at="2023-01-01T00:00:00"
        )
        self.assertEqual(example.category, "test")
        self.assertEqual(example.source, "unittest")
        self.assertEqual(example.created_at, "2023-01-01T00:00:00")

    def test_training_example_auto_timestamp(self):
        example = TrainingExample("Input", "Output")
        # Should have ISO format timestamp
        self.assertIn("T", example.created_at)
        self.assertTrue(example.created_at.endswith("Z") or "+" in example.created_at or example.created_at.count(":") >= 2)

class TestDocument(unittest.TestCase):
    def test_document_creation_with_defaults(self):
        doc = Document("Test content", "Test title")
        self.assertEqual(doc.content, "Test content")
        self.assertEqual(doc.title, "Test title")
        self.assertEqual(doc.category, "general")
        self.assertEqual(doc.metadata, {})
    
    def test_document_with_metadata(self):
        metadata = {"author": "Test Author", "date": "2023-01-01"}
        doc = Document("Content", "Title", "custom", metadata)
        self.assertEqual(doc.category, "custom")
        self.assertEqual(doc.metadata, metadata)

    def test_document_metadata_initialization(self):
        doc = Document("Content", "Title")
        self.assertIsInstance(doc.metadata, dict)
        self.assertEqual(len(doc.metadata), 0)

class TestTrainingDataManager(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.manager = TrainingDataManager(self.temp_db.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('training_examples', tables)
        self.assertIn('documents', tables)
        self.assertIn('embeddings', tables)
        conn.close()
    
    def test_add_and_get_training_example(self):
        example = TrainingExample("Test input", "Test output", "test_category")
        self.manager.add_training_example(example)
        
        examples = self.manager.get_training_examples()
        self.assertEqual(len(examples), 1)
        retrieved = examples[0]
        self.assertEqual(retrieved.input_text, "Test input")
        self.assertEqual(retrieved.output_text, "Test output")
        self.assertEqual(retrieved.category, "test_category")
    
    def test_get_training_examples_by_category(self):
        example1 = TrainingExample("Input 1", "Output 1", "cat1")
        example2 = TrainingExample("Input 2", "Output 2", "cat2")
        example3 = TrainingExample("Input 3", "Output 3", "cat1")
        
        self.manager.add_training_example(example1)
        self.manager.add_training_example(example2)
        self.manager.add_training_example(example3)
        
        cat1_examples = self.manager.get_training_examples("cat1")
        self.assertEqual(len(cat1_examples), 2)
        
        cat2_examples = self.manager.get_training_examples("cat2")
        self.assertEqual(len(cat2_examples), 1)
        self.assertEqual(cat2_examples[0].category, "cat2")
    
    def test_add_and_get_document(self):
        doc = Document("Test content", "Test title", "test_cat", {"key": "value"})
        self.manager.add_document(doc)
        
        docs = self.manager.get_documents()
        self.assertEqual(len(docs), 1)
        retrieved = docs[0]
        self.assertEqual(retrieved.content, "Test content")
        self.assertEqual(retrieved.title, "Test title")
        self.assertEqual(retrieved.category, "test_cat")
        self.assertEqual(retrieved.metadata, {"key": "value"})
    
    def test_get_documents_by_category(self):
        doc1 = Document("Content 1", "Title 1", "cat1")
        doc2 = Document("Content 2", "Title 2", "cat2")
        doc3 = Document("Content 3", "Title 3", "cat1")
        
        self.manager.add_document(doc1)
        self.manager.add_document(doc2)
        self.manager.add_document(doc3)
        
        cat1_docs = self.manager.get_documents("cat1")
        self.assertEqual(len(cat1_docs), 2)
        
        cat2_docs = self.manager.get_documents("cat2")
        self.assertEqual(len(cat2_docs), 1)
        self.assertEqual(cat2_docs[0].category, "cat2")

    def test_document_metadata_serialization(self):
        complex_metadata = {
            "tags": ["ai", "ml"],
            "rating": 5,
            "nested": {"key": "value"}
        }
        doc = Document("Content", "Title", "test", complex_metadata)
        self.manager.add_document(doc)
        
        retrieved_docs = self.manager.get_documents()
        self.assertEqual(len(retrieved_docs), 1)
        self.assertEqual(retrieved_docs[0].metadata, complex_metadata)

class TestSimpleRAGSystem(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.manager = TrainingDataManager(self.temp_db.name)
        self.rag_system = SimpleRAGSystem(self.manager)
        
        # Add test documents
        docs = [
            Document("Artificial intelligence is the simulation of human intelligence in machines.", "AI Basics"),
            Document("Machine learning is a subset of AI that focuses on algorithms learning from data.", "ML Overview"),
            Document("Python is a programming language widely used in data science and web development.", "Python Info")
        ]
        for doc in docs:
            self.manager.add_document(doc)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_build_knowledge_base_success(self):
        with patch('builtins.print') as mock_print:
            self.rag_system.build_knowledge_base()
            self.assertTrue(self.rag_system.is_trained)
            self.assertEqual(len(self.rag_system.documents), 3)
            self.assertIsNotNone(self.rag_system.document_vectors)
            mock_print.assert_called_with("Knowledge base built with 3 documents")
    
    def test_build_knowledge_base_no_documents(self):
        # Create empty manager
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_db.close()
        empty_manager = TrainingDataManager(temp_db.name)
        empty_rag = SimpleRAGSystem(empty_manager)
        
        with patch('builtins.print') as mock_print:
            empty_rag.build_knowledge_base()
            self.assertFalse(empty_rag.is_trained)
            mock_print.assert_called_with("No documents found. Please add documents to the knowledge base first.")
        
        os.unlink(temp_db.name)
    
    def test_retrieve_relevant_docs_success(self):
        self.rag_system.build_knowledge_base()
        
        relevant_docs = self.rag_system.retrieve_relevant_docs("artificial intelligence", top_k=2)
        self.assertGreater(len(relevant_docs), 0)
        self.assertLessEqual(len(relevant_docs), 2)
        
        # Check that most relevant doc contains "artificial intelligence"
        if relevant_docs:
            self.assertIn("artificial", relevant_docs[0].content.lower())
    
    def test_retrieve_relevant_docs_not_trained(self):