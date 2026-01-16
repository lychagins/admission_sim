"""
Module for estimating how tuition waivers affect the probability that a student accepts an offer.

This module uses past admissions data to build a statistical model that predicts
the probability of acceptance based on tuition waiver amounts and student characteristics.
"""

import numpy as np
import statsmodels.api as sm
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
        self.model = None
        self.is_fitted = False
        
    def fit(self, admissions_data: List[Dict]) -> None:
        """
        Fit the model using past admissions data.
        
        Args:
            admissions_data: List of dictionaries containing:
                - 'priority_score': float, student priority score (higher is better)
                - 'waiver': float, tuition waiver amount (0-1 representing percentage)
                - 'accepted': int, whether student accepted the offer (1=yes, 0=no)
                - 'background_score': float, optional background score
        """
        if not admissions_data:
            raise ValueError("admissions_data cannot be empty")
        
        # Extract features and target
        X = []
        y = []
        
        for record in admissions_data:
            features = [
                record.get('priority_score', 0),
                record.get('waiver', 0),
                record.get('background_score', 0),
                record.get('waiver', 0) * record.get('priority_score', 0)  # interaction term
            ]
            X.append(features)
            y.append(1 if record.get('accepted', False) else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Add constant term for intercept
        X_with_const = sm.add_constant(X)
        
        # Fit logistic regression using statsmodels
        # Suppress convergence warnings for small datasets
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=Warning)
            self.model = sm.Logit(y, X_with_const).fit(disp=False)
        self.is_fitted = True
        
    def predict_probability(self, priority_score: float, waiver: float, 
                          background_score: float = 0) -> float:
        """
        Predict the probability that a student accepts an offer.
        
        Args:
            priority_score: Student priority score (higher is better)
            waiver: Tuition waiver amount (0-1 representing percentage)
            background_score: Optional background score
            
        Returns:
            Probability of acceptance (0-1)
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before making predictions")
        
        # Create feature vector (as 2D array for compatibility with statsmodels)
        features = np.array([[
            priority_score,
            waiver,
            background_score,
            waiver * priority_score
        ]])
        
        # Add constant term for intercept
        features_with_const = sm.add_constant(features, has_constant='add')
        
        # Predict probability using the fitted model
        probability = self.model.predict(features_with_const)[0]
        
        return float(probability)
    
    def estimate_acceptance_rates(self, students: List[Dict]) -> List[Dict]:
        """
        Estimate acceptance probabilities for multiple students.
        
        Args:
            students: List of dictionaries containing student info:
                - 'priority_score': float, student priority score
                - 'waiver': float, tuition waiver amount
                - 'background_score': float, optional
                
        Returns:
            List of dictionaries with original data plus 'acceptance_probability'
        """
        results = []
        for student in students:
            result = student.copy()
            result['acceptance_probability'] = self.predict_probability(
                priority_score=student.get('priority_score', 0),
                waiver=student.get('waiver', 0),
                background_score=student.get('background_score', 0)
            )
            results.append(result)
        
        return results
