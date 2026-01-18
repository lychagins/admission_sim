"""
Module for using resampling of past admission data to predict the composition of student body.

This module takes the number and size of tuition waivers as user input and uses
bootstrap resampling to predict the likely composition of the admitted student body.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import Counter
import warnings


# Constants for optimization algorithm
WAIVER_OPTIMIZATION_BASE_MULTIPLIER = 1.0
WAIVER_OPTIMIZATION_RANGE_DIVISOR = 2.0
TARGET_ACCEPTANCE_TOLERANCE = 2.0


class ResamplingSimulator:
    """
    Simulates student body composition using resampling of past admission data.
    
    Uses bootstrap resampling and Monte Carlo simulation to predict which students
    will accept offers given a specific waiver allocation strategy.
    """
    
    def __init__(self, admissions_data: List[Dict], 
                 waiver_probability_model: object):
        """
        Initialize the simulator with historical data.
        
        Args:
            admissions_data: List of dictionaries containing past admissions:
                - 'priority_score': float, student priority score (higher is better)
                - 'waiver': float, tuition waiver percentage
                - 'accepted': int, acceptance decision (1=yes, 0=no)
                - 'background_score': float, optional
                - 'student_id': str/int, student identifier
            waiver_probability_model: Optional fitted WaiverProbabilityEstimator
        """
        if not admissions_data:
            raise ValueError("admissions_data cannot be empty")
            
        self.admissions_data = admissions_data
        # Require a waiver probability model to be supplied and fitted.
        if waiver_probability_model is None or not getattr(waiver_probability_model, 'is_fitted', False):
            raise ValueError("waiver_probability_model must be provided and must be fitted")
        self.waiver_probability_model = waiver_probability_model
        
    def simulate(self, num_offers: int, waiver_allocation: List[Dict],
                 num_simulations: int = 1000, random_seed: Optional[int] = None) -> Dict:
        """
        Simulate student body composition based on waiver allocation.
        
        Args:
            num_offers: Total number of offers to make
            waiver_allocation: List of waiver assignments:
                - 'priority_score': float, student priority score
                - 'waiver': float, waiver percentage (0-1)
                - 'background_score': float, optional
            num_simulations: Number of Monte Carlo simulations to run
            random_seed: Optional seed for reproducibility
            
        Returns:
            Dictionary containing simulation results:
                - 'expected_acceptances': Expected number of students accepting
                - 'acceptance_distribution': Distribution of acceptance counts
                - 'student_probabilities': Probability each student accepts
                - 'mean_priority_score': Expected mean priority score of accepted students
                - 'composition_stats': Statistics about student body composition
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Get acceptance probabilities for each student
        student_probabilities = self._calculate_acceptance_probabilities(waiver_allocation)
        
        # Run Monte Carlo simulations
        simulation_results = []
        accepted_students_per_sim = []
        
        for _ in range(num_simulations):
            accepted = []
            for i, student in enumerate(waiver_allocation):
                if np.random.random() < student_probabilities[i]:
                    accepted.append(student.copy())
                    
            simulation_results.append(len(accepted))
            accepted_students_per_sim.append(accepted)
        
        # Calculate statistics
        acceptance_counts = Counter(simulation_results)
        expected_acceptances = np.mean(simulation_results)
        std_acceptances = np.std(simulation_results)
        
        # Calculate mean priority score of accepted students
        all_priority_scores = []
        for accepted_list in accepted_students_per_sim:
            if accepted_list:
                priority_scores = [s.get('priority_score', 0) for s in accepted_list]
                all_priority_scores.extend(priority_scores)
        
        mean_priority_score = np.mean(all_priority_scores) if all_priority_scores else 0
        
        # Calculate composition statistics
        background_scores = []
        for accepted_list in accepted_students_per_sim:
            for student in accepted_list:
                if 'background_score' in student:
                    background_scores.append(student['background_score'])
        
        return {
            'expected_acceptances': expected_acceptances,
            'std_acceptances': std_acceptances,
            'acceptance_distribution': dict(acceptance_counts),
            'student_probabilities': student_probabilities,
            'mean_priority_score': mean_priority_score,
            'composition_stats': {
                'mean_background_score': np.mean(background_scores) if background_scores else 0,
                'std_background_score': np.std(background_scores) if background_scores else 0
            },
            'percentiles': {
                '10th': np.percentile(simulation_results, 10),
                '25th': np.percentile(simulation_results, 25),
                '50th': np.percentile(simulation_results, 50),
                '75th': np.percentile(simulation_results, 75),
                '90th': np.percentile(simulation_results, 90)
            }
        }
    
    def _calculate_acceptance_probabilities(self, waiver_allocation: List[Dict]) -> List[float]:
        """
        Calculate acceptance probability for each student in the allocation.
        
        Args:
            waiver_allocation: List of student waiver assignments
            
        Returns:
            List of acceptance probabilities
        """
        # Assume a fitted `waiver_probability_model` was provided in `__init__`.
        probabilities = []
        for student in waiver_allocation:
            prob = self.waiver_probability_model.predict_probability(
                priority_score=student.get('priority_score', 0),
                waiver=student.get('waiver', 0),
                background_score=student.get('background_score', 0)
            )
            probabilities.append(prob)

        return probabilities
    
    
