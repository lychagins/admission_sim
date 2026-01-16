"""
Tests for the WaiverProbabilityEstimator module.
"""

import unittest
from admission_sim.waiver_probability import WaiverProbabilityEstimator


class TestWaiverProbabilityEstimator(unittest.TestCase):
    """Test cases for WaiverProbabilityEstimator."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = [
            {'priority_score': 95.5, 'waiver': 0.5, 'accepted': True, 'background_score': 95},
            {'priority_score': 92.3, 'waiver': 0.4, 'accepted': True, 'background_score': 92},
            {'priority_score': 88.7, 'waiver': 0.3, 'accepted': True, 'background_score': 88},
            {'priority_score': 85.2, 'waiver': 0.5, 'accepted': True, 'background_score': 85},
            {'priority_score': 82.1, 'waiver': 0.2, 'accepted': False, 'background_score': 82},
            {'priority_score': 80.4, 'waiver': 0.6, 'accepted': True, 'background_score': 80},
            {'priority_score': 78.9, 'waiver': 0.3, 'accepted': False, 'background_score': 78},
            {'priority_score': 75.6, 'waiver': 0.4, 'accepted': True, 'background_score': 75},
            {'priority_score': 72.3, 'waiver': 0.1, 'accepted': False, 'background_score': 72},
            {'priority_score': 70.8, 'waiver': 0.5, 'accepted': True, 'background_score': 70},
        ]
        
    def test_initialization(self):
        """Test that estimator initializes correctly."""
        estimator = WaiverProbabilityEstimator()
        self.assertIsNone(estimator.coefficients)
        self.assertIsNone(estimator.intercept)
        self.assertFalse(estimator.is_fitted)
        
    def test_fit(self):
        """Test that model can be fitted."""
        estimator = WaiverProbabilityEstimator()
        estimator.fit(self.sample_data)
        
        self.assertTrue(estimator.is_fitted)
        self.assertIsNotNone(estimator.coefficients)
        self.assertIsNotNone(estimator.intercept)
        
    def test_fit_empty_data(self):
        """Test that fitting with empty data raises error."""
        estimator = WaiverProbabilityEstimator()
        with self.assertRaises(ValueError):
            estimator.fit([])
            
    def test_predict_probability(self):
        """Test probability prediction."""
        estimator = WaiverProbabilityEstimator()
        estimator.fit(self.sample_data)
        
        prob = estimator.predict_probability(priority_score=3, waiver=0.5, background_score=90)
        
        # Check that probability is between 0 and 1
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
        
    def test_predict_without_fit(self):
        """Test that predicting without fitting raises error."""
        estimator = WaiverProbabilityEstimator()
        
        with self.assertRaises(RuntimeError):
            estimator.predict_probability(priority_score=1, waiver=0.5)
            
    def test_estimate_acceptance_rates(self):
        """Test estimating rates for multiple students."""
        estimator = WaiverProbabilityEstimator()
        estimator.fit(self.sample_data)
        
        students = [
            {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
            {'priority_score': 82.1, 'waiver': 0.3, 'background_score': 80},
        ]
        
        results = estimator.estimate_acceptance_rates(students)
        
        self.assertEqual(len(results), 2)
        self.assertIn('acceptance_probability', results[0])
        self.assertIn('acceptance_probability', results[1])
        
    def test_probability_range(self):
        """Test that probabilities are always in valid range."""
        estimator = WaiverProbabilityEstimator()
        estimator.fit(self.sample_data)
        
        # Test various scenarios
        test_cases = [
            (95.5, 0.0, 0),
            (95.5, 1.0, 100),
            (70.8, 0.5, 50),
            (82.1, 0.3, 75),
        ]
        
        for priority_score, waiver, background in test_cases:
            prob = estimator.predict_probability(priority_score, waiver, background)
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)


if __name__ == '__main__':
    unittest.main()
