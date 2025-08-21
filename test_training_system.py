"""
Comprehensive Test Suite for AI Chatbot Training System
Tests all components of the training system including data management, RAG, and imports
"""

import unittest
import tempfile
import os
import json
import csv
import sqlite3
from unittest.mock import patch, MagicMock
import sys
import shutil

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from training_system import (
        TrainingDataManager, 
        SimpleRAGSystem, 
        FinetuningDataPrep, 
        DataImporter,
        TrainingExample,
        Document
    )
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure training_system.py is in the same directory")
    sys.exit(1)

class TestTrainingSystem(unittest.TestCase):
    """Test suite for the AI Chatbot Training System"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test databases and files
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, "test_training.db")
        
        # Initialize test components
        self.training_manager = TrainingDataManager(self.test_db_path)
        self.rag_system = SimpleRAGSystem(self.training_manager)
        self.data_prep = FinetuningDataPrep(self.training_manager)
        self.importer = DataImporter(self.training_manager)
        
        print(f"\n🧪 Running test: {self._testMethodName}")
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary directory and all its contents
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_training_example_creation(self):
        """Test TrainingExample dataclass creation"""
        example = TrainingExample(
            input_text="What is AI?",
            output_text="AI is artificial intelligence",
            category="technology"
        )
        
        self.assertEqual(example.input_text, "What is AI?")
        self.assertEqual(example.output_text, "AI is artificial intelligence")
        self.assertEqual(example.category, "technology")
        self.assertEqual(example.source, "manual")
        self.assertIsNotNone(example.created_at)
        print("✅ TrainingExample creation test passed")
    
    def test_document_creation(self):
        """Test Document dataclass creation"""
        doc = Document(
            content="This is test content",
            title="Test Document",
            category="test"
        )
        
        self.assertEqual(doc.content, "This is test content")
        self.assertEqual(doc.title, "Test Document")
        self.assertEqual(doc.category, "test")
        self.assertEqual(doc.metadata, {})
        print("✅ Document creation test passed")
    
    def test_database_initialization(self):
        """Test database creation and table setup"""
        # Check if database file exists
        self.assertTrue(os.path.exists(self.test_db_path))
        
        # Check if tables are created
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Check training_examples table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='training_examples'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check documents table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check embeddings table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
        print("✅ Database initialization test passed")
    
    def test_add_training_example(self):
        """Test adding training examples to database"""
        example = TrainingExample(
            input_text="Test question",
            output_text="Test answer",
            category="test",
            source="unittest"
        )
        
        # Add example
        self.training_manager.add_training_example(example)
        
        # Retrieve and verify
        examples = self.training_manager.get_training_examples()
        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0].input_text, "Test question")
        self.assertEqual(examples[0].output_text, "Test answer")
        print("✅ Add training example test passed")
    
    def test_add_document(self):
        """Test adding documents to database"""
        doc = Document(
            content="Test document content",
            title="Test Doc",
            category="test_docs",
            metadata={"source": "unittest"}
        )
        
        # Add document
        self.training_manager.add_document(doc)
        
        # Retrieve and verify
        documents = self.training_manager.get_documents()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].title, "Test Doc")
        self.assertEqual(documents[0].content, "Test document content")
        print("✅ Add document test passed")
    
    def test_category_filtering(self):
        """Test filtering by category"""
        # Add examples with different categories
        example1 = TrainingExample("Q1", "A1", "cat1", "test")
        example2 = TrainingExample("Q2", "A2", "cat2", "test")
        example3 = TrainingExample("Q3", "A3", "cat1", "test")
        
        self.training_manager.add_training_example(example1)
        self.training_manager.add_training_example(example2)
        self.training_manager.add_training_example(example3)
        
        # Test category filtering
        cat1_examples = self.training_manager.get_training_examples("cat1")
        cat2_examples = self.training_manager.get_training_examples("cat2")
        all_examples = self.training_manager.get_training_examples()
        
        self.assertEqual(len(cat1_examples), 2)
        self.assertEqual(len(cat2_examples), 1)
        self.assertEqual(len(all_examples), 3)
        print("✅ Category filtering test passed")
    
    def test_rag_system_build(self):
        """Test RAG system knowledge base building"""
        # Add some test documents
        docs = [
            Document("Machine learning is a subset of AI", "ML Doc", "tech"),
            Document("Python is a programming language", "Python Doc", "programming"),
            Document("Data science involves statistics", "DS Doc", "data")
        ]
        
        for doc in docs:
            self.training_manager.add_document(doc)
        
        # Build knowledge base
        try:
            self.rag_system.build_knowledge_base()
            self.assertTrue(self.rag_system.is_trained)
            print("✅ RAG system build test passed")
        except Exception as e:
            self.fail(f"RAG system build failed: {e}")
    
    def test_rag_document_retrieval(self):
        """Test RAG document retrieval"""
        # Add test documents
        docs = [
            Document("Artificial intelligence is the future of technology", "AI Doc", "tech"),
            Document("Machine learning algorithms learn from data", "ML Doc", "tech"),
            Document("Cooking pasta requires boiling water", "Cooking Doc", "food")
        ]
        
        for doc in docs:
            self.training_manager.add_document(doc)
        
        # Build knowledge base and test retrieval
        self.rag_system.build_knowledge_base()
        
        # Test relevant document retrieval
        relevant_docs = self.rag_system.retrieve_relevant_docs("What is artificial intelligence?", top_k=2)
        
        # Should find tech-related documents
        self.assertGreater(len(relevant_docs), 0)
        print(f"✅ RAG retrieval test passed - Found {len(relevant_docs)} relevant documents")
    
    def test_rag_context_generation(self):
        """Test RAG context prompt generation"""
        # Add a relevant document
        doc = Document(
            "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by humans.",
            "AI Definition",
            "tech"
        )
        self.training_manager.add_document(doc)
        
        # Build knowledge base
        self.rag_system.build_knowledge_base()
        
        # Test context generation
        query = "What is AI?"
        enhanced_prompt = self.rag_system.generate_context_prompt(query)
        
        # Enhanced prompt should contain relevant information
        self.assertIn("intelligence", enhanced_prompt.lower())
        self.assertNotEqual(enhanced_prompt, query)  # Should be enhanced
        print("✅ RAG context generation test passed")
    
    def test_csv_export(self):
        """Test CSV export functionality"""
        # Add test data
        examples = [
            TrainingExample("Q1", "A1", "test", "unittest"),
            TrainingExample("Q2", "A2", "test", "unittest")
        ]
        
        for example in examples:
            self.training_manager.add_training_example(example)
        
        # Export to CSV
        csv_path = os.path.join(self.test_dir, "test_export.csv")
        self.data_prep.export_csv(csv_path)
        
        # Verify CSV file was created and contains data
        self.assertTrue(os.path.exists(csv_path))
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['input'], 'Q1')
        
        print("✅ CSV export test passed")
    
    def test_jsonl_export(self):
        """Test JSONL export functionality"""
        # Add test data
        example = TrainingExample("Test input", "Test output", "test", "unittest")
        self.training_manager.add_training_example(example)
        
        # Export to JSONL
        jsonl_path = os.path.join(self.test_dir, "test_export.jsonl")
        self.data_prep.export_jsonl(jsonl_path, format_type="openai")
        
        # Verify JSONL file
        self.assertTrue(os.path.exists(jsonl_path))
        
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            data = json.loads(line)
            self.assertIn('messages', data)
            self.assertEqual(len(data['messages']), 2)
        
        print("✅ JSONL export test passed")
    
    def test_csv_import(self):
        """Test CSV import functionality"""
        # Create test CSV file
        csv_path = os.path.join(self.test_dir, "test_import.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['input', 'output', 'category'])
            writer.writerow(['What is Python?', 'Python is a programming language', 'programming'])
            writer.writerow(['How to code?', 'Start with basics', 'programming'])
        
        # Import CSV
        self.importer.import_from_csv(csv_path, 'input', 'output', 'category')
        
        # Verify import
        examples = self.training_manager.get_training_examples()
        self.assertEqual(len(examples), 2)
        self.assertEqual(examples[0].input_text, 'What is Python?')
        print("✅ CSV import test passed")
    
    def test_json_import(self):
        """Test JSON import functionality"""
        # Create test JSON file
        json_path = os.path.join(self.test_dir, "test_import.json")
        test_data = [
            {
                "input": "What is machine learning?",
                "output": "ML is a subset of AI",
                "category": "ai"
            }
        ]
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Import JSON
        self.importer.import_from_json(json_path)
        
        # Verify import
        examples = self.training_manager.get_training_examples()
        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0].category, 'ai')
        print("✅ JSON import test passed")
    
    def test_text_file_import(self):
        """Test text file import functionality"""
        # Create test text file
        text_path = os.path.join(self.test_dir, "test_doc.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write("This is a test document for knowledge base.")
        
        # Import text file
        self.importer.import_from_text_file(text_path, "Test Document", "test_docs")
        
        # Verify import
        documents = self.training_manager.get_documents()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].title, "Test Document")
        print("✅ Text file import test passed")
    
    @patch('requests.get')
    def test_web_scraping(self, mock_get):
        """Test web scraping functionality"""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test web content</body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Test web scraping
        self.importer.scrape_website_content("https://example.com", "Test Page", "web")
        
        # Verify document was added
        documents = self.training_manager.get_documents()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].title, "Test Page")
        print("✅ Web scraping test passed")
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        print("\n🔄 Running end-to-end workflow test...")
        
        # Step 1: Add training data
        examples = [
            TrainingExample("What is AI?", "Artificial Intelligence", "ai", "test"),
            TrainingExample("Define ML", "Machine Learning", "ai", "test")
        ]
        
        documents = [
            Document("AI is the future of technology", "AI Overview", "ai_docs"),
            Document("ML algorithms learn from data", "ML Guide", "ai_docs")
        ]
        
        for example in examples:
            self.training_manager.add_training_example(example)
        
        for doc in documents:
            self.training_manager.add_document(doc)
        
        # Step 2: Build RAG system
        self.rag_system.build_knowledge_base()
        self.assertTrue(self.rag_system.is_trained)
        
        # Step 3: Test RAG enhancement
        enhanced_prompt = self.rag_system.generate_context_prompt("Tell me about AI")
        self.assertIn("AI", enhanced_prompt)
        
        # Step 4: Export data
        csv_path = os.path.join(self.test_dir, "workflow_test.csv")
        self.data_prep.export_csv(csv_path)
        self.assertTrue(os.path.exists(csv_path))
        
        # Step 5: Verify data integrity
        retrieved_examples = self.training_manager.get_training_examples()
        retrieved_docs = self.training_manager.get_documents()
        
        self.assertEqual(len(retrieved_examples), 2)
        self.assertEqual(len(retrieved_docs), 2)
        
        print("✅ End-to-end workflow test passed")

def run_comprehensive_tests():
    """Run all tests with detailed reporting"""
    print("🧪 AI Chatbot Training System - Comprehensive Test Suite")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTrainingSystem)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n🎉 ALL TESTS PASSED! Your training system is working perfectly.")
        print(f"✅ The AI chatbot training system is ready for production use.")
    else:
        print(f"\n⚠️  Some tests failed. Please review the issues above.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
