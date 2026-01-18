"""
Tests for the ResamplingSimulator module.
"""

import unittest
from admission_sim.waiver_probability import WaiverProbabilityEstimator
from admission_sim.resampling_simulator import ResamplingSimulator


class TestResamplingSimulator(unittest.TestCase):
    """Test cases for ResamplingSimulator."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = [
            {'priority_score': 95.5, 'waiver': 0.5, 'accepted': 1, 'background_score': 95},
            {'priority_score': 92.3, 'waiver': 0.4, 'accepted': 1, 'background_score': 92},
            {'priority_score': 88.7, 'waiver': 0.3, 'accepted': 1, 'background_score': 88},
            {'priority_score': 85.2, 'waiver': 0.5, 'accepted': 1, 'background_score': 85},
            {'priority_score': 82.1, 'waiver': 0.2, 'accepted': 0, 'background_score': 82},
            {'priority_score': 80.4, 'waiver': 0.6, 'accepted': 1, 'background_score': 80},
            {'priority_score': 78.9, 'waiver': 0.3, 'accepted': 0, 'background_score': 78},
            {'priority_score': 75.6, 'waiver': 0.4, 'accepted': 1, 'background_score': 75},
            {'priority_score': 72.3, 'waiver': 0.1, 'accepted': 0, 'background_score': 72},
            {'priority_score': 70.8, 'waiver': 0.5, 'accepted': 1, 'background_score': 70},
            {'priority_score': 84.0, 'waiver': 0.4, 'accepted': 0, 'background_score': 84},
            {'priority_score': 60.0, 'waiver': 0.1, 'accepted': 1, 'background_score': 60},
        ]
        # Prepare a fitted estimator to pass into the simulator
        self.estimator = WaiverProbabilityEstimator()
        self.estimator.fit(self.sample_data)
        
    def test_initialization(self):
        """Test that simulator initializes correctly."""
        simulator = ResamplingSimulator(self.sample_data, self.estimator)
        self.assertEqual(len(simulator.admissions_data), 12)
        
    def test_initialization_empty_data(self):
        """Test that initialization with empty data raises error."""
        with self.assertRaises(ValueError):
            ResamplingSimulator([], self.estimator)
            
    def test_simulate(self):
        """Test basic simulation."""
        simulator = ResamplingSimulator(self.sample_data, self.estimator)
        
        waiver_allocation = [
            {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
            {'priority_score': 92.3, 'waiver': 0.4, 'background_score': 92},
            {'priority_score': 88.7, 'waiver': 0.3, 'background_score': 88},
        ]
        
        results = simulator.simulate(
            num_offers=3,
            waiver_allocation=waiver_allocation,
            num_simulations=100,
            random_seed=42
        )
        
        # Check that results contain expected keys
        self.assertIn('expected_acceptances', results)
        self.assertIn('std_acceptances', results)
        self.assertIn('acceptance_distribution', results)
        self.assertIn('student_probabilities', results)
        self.assertIn('mean_priority_score', results)
        
    def test_simulate_with_model(self):
        """Test simulation with fitted probability model."""
        estimator = WaiverProbabilityEstimator()
        estimator.fit(self.sample_data)
        
        simulator = ResamplingSimulator(self.sample_data, estimator)
        
        waiver_allocation = [
            {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
            {'priority_score': 92.3, 'waiver': 0.4, 'background_score': 92},
        ]
        
        results = simulator.simulate(
            num_offers=2,
            waiver_allocation=waiver_allocation,
            num_simulations=100,
            random_seed=42
        )
        
        self.assertGreater(results['expected_acceptances'], 0)
        
    def test_simulate_reproducibility(self):
        """Test that simulation with same seed produces same results."""
        simulator = ResamplingSimulator(self.sample_data, self.estimator)
        
        waiver_allocation = [
            {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
        ]
        
        results1 = simulator.simulate(
            num_offers=1,
            waiver_allocation=waiver_allocation,
            num_simulations=100,
            random_seed=42
        )
        
        results2 = simulator.simulate(
            num_offers=1,
            waiver_allocation=waiver_allocation,
            num_simulations=100,
            random_seed=42
        )
        
        self.assertEqual(results1['expected_acceptances'], results2['expected_acceptances'])
        
    
        
    def test_percentiles_in_results(self):
        """Test that simulation results include percentile information."""
        simulator = ResamplingSimulator(self.sample_data, self.estimator)
        
        waiver_allocation = [
            {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
            {'priority_score': 92.3, 'waiver': 0.4, 'background_score': 92},
        ]
        
        results = simulator.simulate(
            num_offers=2,
            waiver_allocation=waiver_allocation,
            num_simulations=100
        )
        
        self.assertIn('percentiles', results)
        self.assertIn('10th', results['percentiles'])
        self.assertIn('50th', results['percentiles'])
        self.assertIn('90th', results['percentiles'])


if __name__ == '__main__':
    unittest.main()
