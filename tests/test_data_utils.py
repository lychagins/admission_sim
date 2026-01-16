"""
Tests for the data utilities module.
"""

import unittest
import tempfile
import os
from admission_sim.data_utils import load_admissions_data, save_admissions_data, create_sample_csv


class TestDataUtils(unittest.TestCase):
    """Test cases for data utilities."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = [
            {'priority_score': 95.5, 'waiver': 0.5, 'accepted': True, 'background_score': 95, 'student_id': 'S001'},
            {'priority_score': 92.3, 'waiver': 0.4, 'accepted': True, 'background_score': 92, 'student_id': 'S002'},
            {'priority_score': 88.7, 'waiver': 0.3, 'accepted': False, 'background_score': 88, 'student_id': 'S003'},
        ]
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_save_and_load_data(self):
        """Test saving and loading admissions data."""
        filepath = os.path.join(self.temp_dir, 'test_data.csv')
        
        # Save data
        save_admissions_data(self.sample_data, filepath)
        
        # Check file exists
        self.assertTrue(os.path.exists(filepath))
        
        # Load data back
        loaded_data = load_admissions_data(filepath)
        
        # Verify loaded data matches original
        self.assertEqual(len(loaded_data), len(self.sample_data))
        self.assertEqual(loaded_data[0]['priority_score'], 95.5)
        self.assertEqual(loaded_data[0]['waiver'], 0.5)
        self.assertTrue(loaded_data[0]['accepted'])
        self.assertEqual(loaded_data[0]['student_id'], 'S001')
        
    def test_save_empty_data(self):
        """Test that saving empty data raises error."""
        filepath = os.path.join(self.temp_dir, 'test_empty.csv')
        
        with self.assertRaises(ValueError):
            save_admissions_data([], filepath)
            
    def test_create_sample_csv(self):
        """Test creating sample CSV."""
        filepath = os.path.join(self.temp_dir, 'sample.csv')
        
        create_sample_csv(filepath)
        
        # Check file exists
        self.assertTrue(os.path.exists(filepath))
        
        # Load and verify
        data = load_admissions_data(filepath)
        self.assertGreater(len(data), 0)
        self.assertIn('priority_score', data[0])
        self.assertIn('waiver', data[0])
        self.assertIn('accepted', data[0])
        
    def test_data_types(self):
        """Test that loaded data has correct types."""
        filepath = os.path.join(self.temp_dir, 'test_types.csv')
        
        save_admissions_data(self.sample_data, filepath)
        loaded_data = load_admissions_data(filepath)
        
        # Check types
        self.assertIsInstance(loaded_data[0]['priority_score'], float)
        self.assertIsInstance(loaded_data[0]['waiver'], float)
        self.assertIsInstance(loaded_data[0]['accepted'], bool)
        self.assertIsInstance(loaded_data[0]['background_score'], float)
        self.assertIsInstance(loaded_data[0]['student_id'], str)


if __name__ == '__main__':
    unittest.main()
