# Admission Simulation Tool

A simple tool for evaluating admission strategies in a small program. This tool helps admission committees make data-driven decisions about tuition waiver allocations to optimize student enrollment.

## Features

The tool provides two main modules:

1. **Waiver Probability Estimator**: Estimates how tuition waivers affect the probability that a student accepts an offer
   - Uses logistic regression to model acceptance probability
   - Considers student ranking, waiver amount, and background scores
   - Provides individual acceptance probability predictions

2. **Resampling Simulator**: Uses resampling of past admission data to predict the composition of student body
   - Takes the number and size of tuition waivers as user input
   - Uses Monte Carlo simulation with bootstrap resampling
   - Predicts expected enrollment and student body composition
   - Provides optimization suggestions for waiver allocation

Both modules use past admissions data including:
- Background information and ranking of students with offers
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
    {'ranking': 1, 'waiver': 0.5, 'accepted': True, 'background_score': 95},
    {'ranking': 2, 'waiver': 0.4, 'accepted': True, 'background_score': 92},
    # ... more data
]

# 1. Estimate acceptance probabilities
estimator = WaiverProbabilityEstimator()
estimator.fit(admissions_data)

probability = estimator.predict_probability(ranking=3, waiver=0.5, background_score=90)
print(f"Acceptance probability: {probability:.2%}")

# 2. Simulate student body composition
simulator = ResamplingSimulator(admissions_data, estimator)

waiver_allocation = [
    {'ranking': 1, 'waiver': 0.5, 'background_score': 95},
    {'ranking': 2, 'waiver': 0.4, 'background_score': 92},
    # ... more students
]

results = simulator.simulate(
    num_offers=10,
    waiver_allocation=waiver_allocation,
    num_simulations=1000
)

print(f"Expected acceptances: {results['expected_acceptances']:.2f}")
print(f"Mean ranking: {results['mean_ranking']:.2f}")
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
- How to optimize waiver allocation

## Data Format

The tool expects admissions data as a list of dictionaries with the following fields:

- `ranking`: int - Student ranking (1 is best)
- `waiver`: float - Tuition waiver as a percentage (0-1, where 0.5 = 50%)
- `accepted`: bool - Whether the student accepted the offer
- `background_score`: float - Optional background/qualification score
- `student_id`: str/int - Optional student identifier

Example:
```python
{
    'ranking': 1,
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
- `predict_probability(ranking, waiver, background_score)`: Predict acceptance probability
- `estimate_acceptance_rates(students)`: Predict for multiple students

### ResamplingSimulator

Simulates student body composition using Monte Carlo simulation.

**Key Methods:**
- `simulate(num_offers, waiver_allocation, num_simulations)`: Run simulation
- `optimize_waiver_allocation(num_offers, total_waiver_budget, target_acceptances)`: Find optimal allocation

## Use Cases

1. **Predict Enrollment**: Estimate how many students will accept offers given a waiver strategy
2. **Optimize Resources**: Find the best way to allocate limited waiver budget
3. **Risk Analysis**: Understand the variability in enrollment outcomes
4. **Strategic Planning**: Test different scenarios before making actual offers

## License

MIT License - see LICENSE file for details
