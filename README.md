# Admission Simulation Tool

A simple tool for evaluating admission strategies in a small program. This tool helps admission committees make data-driven decisions about tuition waiver allocations to optimize student enrollment.

## Features

The tool provides two main modules:

1. **Waiver Probability Estimator**: Estimates how tuition waivers affect the probability that a student accepts an offer
   - Uses logistic regression to model acceptance probability
   - Considers student priority score, waiver amount, and background scores
   - Provides individual acceptance probability predictions

2. **Resampling Simulator**: Simulates enrollment outcomes given a waiver allocation
    - Takes the number and size of tuition waivers as user input
    - Requires a fitted `WaiverProbabilityEstimator` (or compatible model) to supply
      per-student acceptance probabilities via `predict_probability(...)`
    - Uses Monte Carlo simulation that queries the supplied model for each student
    - Predicts expected enrollment and student body composition

Both modules use past admissions data including:
- Background information and priority scores of students with offers
- Tuition waivers allocated
- Acceptance decisions

## Installation

```bash
# Clone the repository
git clone https://github.com/lychagins/admission_sim.git
cd admission_sim

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from admission_sim import WaiverProbabilityEstimator, ResamplingSimulator

# Sample historical data
admissions_data = [
    {'priority_score': 1, 'waiver': 0.5, 'accepted': True, 'background_score': 95},
    {'priority_score': 2, 'waiver': 0.4, 'accepted': True, 'background_score': 92},
    # ... more data
]

# 1. Estimate acceptance probabilities
estimator = WaiverProbabilityEstimator()
estimator.fit(admissions_data)

probability = estimator.predict_probability(priority_score=3, waiver=0.5, background_score=90)
print(f"Acceptance probability: {probability:.2%}")

# 2. Simulate student body composition
simulator = ResamplingSimulator(admissions_data, estimator)

waiver_allocation = [
    {'priority_score': 1, 'waiver': 0.5, 'background_score': 95},
    {'priority_score': 2, 'waiver': 0.4, 'background_score': 92},
    # ... more students
]

results = simulator.simulate(
    num_offers=10,
    waiver_allocation=waiver_allocation,
    num_simulations=1000
)

print(f"Expected acceptances: {results['expected_acceptances']:.2f}")
print(f"Mean priority score: {results['mean_priority_score']:.2f}")
```

## Examples

Run the comprehensive examples:

```bash
python example_usage.py
```

This will demonstrate:
- How to fit the probability estimator
- How to predict acceptance probabilities
- How to simulate student body composition

## Data Format

The tool expects admissions data as a list of dictionaries with the following fields:

- `priority_score`: float - Student priority score (higher is better)
- `waiver`: float - Tuition waiver as a proportion (0-1, where 0.5 = 50%)
- `accepted`: bool or int - Whether the student accepted the offer (True/1 = accepted)
- `background_score`: float - Optional background/qualification score
- `student_id`: str/int - Optional student identifier

Example:
```python
{
    'priority_score': 95.0,
    'waiver': 0.5,
    'accepted': True,
    'background_score': 95,
    'student_id': 'S001'
}
```

## Modules

### WaiverProbabilityEstimator

Estimates acceptance probability using logistic regression.

**Key Methods:**
- `fit(admissions_data)`: Train the model on historical data
- `predict_probability(priority score, waiver, background_score)`: Predict acceptance probability
- `estimate_acceptance_rates(students)`: Predict for multiple students

### ResamplingSimulator

Simulates student body composition using Monte Carlo sampling. The simulator
requires a fitted `WaiverProbabilityEstimator` (or compatible model) that implements
`predict_probability(priority_score, waiver, background_score)` and exposes an
`is_fitted` attribute set to `True` after `fit()`.

**Key Methods:**
- `simulate(num_offers, waiver_allocation, num_simulations)`: Run simulation

## Use Cases

1. **Predict Enrollment**: Estimate how many students will accept offers given a waiver strategy
2. **Optimize Resources**: Find the best way to allocate limited waiver budget (note: the
    package does not include a built-in optimizer; implement optimization externally
    by calling the simulator and estimator)
3. **Risk Analysis**: Understand the variability in enrollment outcomes
4. **Strategic Planning**: Test different scenarios before making actual offers

## License

MIT License - see LICENSE file for details
