"""
Admission Simulation Tool

A tool for evaluating admission strategies in a small program.
Includes modules for:
- Estimating how tuition waivers affect acceptance probability
- Resampling past admission data to predict student body composition
"""

from .waiver_probability import WaiverProbabilityEstimator
from .resampling_simulator import ResamplingSimulator

__version__ = "0.1.0"
__all__ = ["WaiverProbabilityEstimator", "ResamplingSimulator"]
