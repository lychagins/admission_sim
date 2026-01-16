"""
Module for estimating how tuition waivers affect the probability that a student accepts an offer.

This module uses past admissions data to build a statistical model that predicts
the probability of acceptance based on tuition waiver amounts and student characteristics.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings


class WaiverProbabilityEstimator:
    """
    Estimates the probability that a student accepts an offer based on tuition waivers.
    
    Uses logistic regression to model the relationship between tuition waivers,
    student characteristics, and acceptance decisions.
    """
    
    def __init__(self):
        """Initialize the estimator."""
        self.coefficients = None
        self.intercept = None
        self.is_fitted = False
        
    def fit(self, admissions_data: List[Dict]) -> None:
        """
        Fit the model using past admissions data.
        
        Args:
            admissions_data: List of dictionaries containing:
                - 'ranking': int, student ranking (1 is best)
                - 'waiver': float, tuition waiver amount (0-1 representing percentage)
                - 'accepted': bool, whether student accepted the offer
                - 'background_score': float, optional background score
        """
        if not admissions_data:
            raise ValueError("admissions_data cannot be empty")
        
        # Extract features and target
        X = []
        y = []
        
        for record in admissions_data:
            features = [
                1.0,  # intercept term
                record.get('ranking', 0),
                record.get('waiver', 0),
                record.get('background_score', 0),
                record.get('waiver', 0) * record.get('ranking', 0)  # interaction term
            ]
            X.append(features)
            y.append(1 if record.get('accepted', False) else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Simple gradient descent for logistic regression
        self._fit_logistic_regression(X, y)
        self.is_fitted = True
        
    def _fit_logistic_regression(self, X: np.ndarray, y: np.ndarray, 
                                  learning_rate: float = 0.01, 
                                  iterations: int = 1000) -> None:
        """
        Fit logistic regression using gradient descent.
        
        Args:
            X: Feature matrix
            y: Target vector
            learning_rate: Learning rate for gradient descent
            iterations: Number of iterations
        """
        n_samples, n_features = X.shape
        self.coefficients = np.zeros(n_features)
        
        for _ in range(iterations):
            # Sigmoid function
            z = np.dot(X, self.coefficients)
            predictions = 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # clip to prevent overflow
            
            # Gradient
            gradient = np.dot(X.T, (predictions - y)) / n_samples
            
            # Update coefficients
            self.coefficients -= learning_rate * gradient
        
        self.intercept = self.coefficients[0]
        self.coefficients = self.coefficients[1:]
        
    def predict_probability(self, ranking: int, waiver: float, 
                          background_score: float = 0) -> float:
        """
        Predict the probability that a student accepts an offer.
        
        Args:
            ranking: Student ranking (1 is best)
            waiver: Tuition waiver amount (0-1 representing percentage)
            background_score: Optional background score
            
        Returns:
            Probability of acceptance (0-1)
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before making predictions")
        
        # Create feature vector
        features = np.array([
            ranking,
            waiver,
            background_score,
            waiver * ranking
        ])
        
        # Compute probability
        z = self.intercept + np.dot(self.coefficients, features)
        probability = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        
        return float(probability)
    
    def estimate_acceptance_rates(self, students: List[Dict]) -> List[Dict]:
        """
        Estimate acceptance probabilities for multiple students.
        
        Args:
            students: List of dictionaries containing student info:
                - 'ranking': int, student ranking
                - 'waiver': float, tuition waiver amount
                - 'background_score': float, optional
                
        Returns:
            List of dictionaries with original data plus 'acceptance_probability'
        """
        results = []
        for student in students:
            result = student.copy()
            result['acceptance_probability'] = self.predict_probability(
                ranking=student.get('ranking', 0),
                waiver=student.get('waiver', 0),
                background_score=student.get('background_score', 0)
            )
            results.append(result)
        
        return results
