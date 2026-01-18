# Quick Start Guide

This guide will help you get started with the Admission Simulation Tool.

## Installation

```bash
# Clone the repository
git clone https://github.com/lychagins/admission_sim.git
cd admission_sim

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Prepare Your Data

The tool expects historical admissions data in the following format:

```python
admissions_data = [
    {
        'priority_score': 1,              # Student priority score (1 is best)
        'waiver': 0.5,            # Tuition waiver (0-1, where 0.5 = 50%)
        'accepted': 1,         # Whether student accepted
        'background_score': 95,   # Optional: background/qualification score
        'student_id': 'S001'      # Optional: student identifier
    },
    # ... more records
]
```

### 2. Estimate Acceptance Probabilities

```python
from admission_sim import WaiverProbabilityEstimator

# Create and train the estimator
estimator = WaiverProbabilityEstimator()
estimator.fit(admissions_data)

# Predict for a new student
probability = estimator.predict_probability(
    priority_score=3,
    waiver=0.5,
    background_score=90
)
print(f"Acceptance probability: {probability:.2%}")
```

### 3. Simulate Student Body Composition

```python
from admission_sim import ResamplingSimulator

# Create simulator
simulator = ResamplingSimulator(admissions_data, estimator)

# Define your waiver allocation strategy
waiver_allocation = [
    {'priority_score': 1, 'waiver': 0.5, 'background_score': 95},
    {'priority_score': 2, 'waiver': 0.4, 'background_score': 92},
    {'priority_score': 3, 'waiver': 0.3, 'background_score': 88},
    # ... more students
]

# Run simulation
results = simulator.simulate(
    num_offers=10,
    waiver_allocation=waiver_allocation,
    num_simulations=1000
)

print(f"Expected acceptances: {results['expected_acceptances']:.2f}")
print(f"Standard deviation: {results['std_acceptances']:.2f}")
print(f"Mean priority score: {results['mean_priority_score']:.2f}")
```

## Working with CSV Files

The package no longer provides CSV helpers. Use `pandas` or your own
I/O utilities to load and save admissions data.

```python
import pandas as pd

# Load data from CSV (returns a DataFrame)
df = pd.read_csv('admissions_history.csv')

# Convert to list-of-dicts if needed by the estimator/simulator
admissions_data = df.to_dict(orient='records')

# Use the data...
estimator = WaiverProbabilityEstimator()
estimator.fit(admissions_data)

# Save results
updated_df = pd.DataFrame(admissions_data)
updated_df.to_csv('admissions_updated.csv', index=False)
```

## Running Examples

Run the comprehensive examples to see all features:

```bash
python example_usage.py
```

This will demonstrate:
- Fitting the probability estimator
- Predicting acceptance probabilities
- Simulating student body composition

Note: The package no longer includes a built-in waiver allocation optimizer. If you
need to search for optimal allocations, call the estimator and simulator from your
own optimization routine (e.g., `scipy.optimize`, a simple grid search, or an
evolutionary search).

## Running Tests

```bash
python -m unittest discover tests -v
```

## Common Use Cases

### Case 1: Predict Enrollment for Next Year

```python
import pandas as pd

# 1. Load historical data
df = pd.read_csv('past_admissions.csv')
admissions_data = df.to_dict(orient='records')

# 2. Train estimator
estimator = WaiverProbabilityEstimator()
estimator.fit(admissions_data)

# 3. Create simulator
simulator = ResamplingSimulator(admissions_data, estimator)

# 4. Define your planned waiver allocation
planned_allocation = [...]  # Your allocation strategy

# 5. Simulate
results = simulator.simulate(
    num_offers=len(planned_allocation),
    waiver_allocation=planned_allocation,
    num_simulations=1000
)

# 6. Analyze results
print(f"Expected enrollment: {results['expected_acceptances']:.1f}")
print(f"90th percentile: {results['percentiles']['90th']:.0f}")
print(f"10th percentile: {results['percentiles']['10th']:.0f}")
```

### Case 2: Compare Different Strategies

```python
strategies = [
    # Strategy 1: Equal waivers
    [{'priority_score': 100 - i*5, 'waiver': 0.3} for i in range(10)],
    
    # Strategy 2: Higher waivers for top students
    [{'priority_score': 100 - i*5, 'waiver': 0.5 if i < 5 else 0.2} for i in range(10)],
]

for i, strategy in enumerate(strategies):
    results = simulator.simulate(10, strategy, 1000)
    print(f"Strategy {i+1}: {results['expected_acceptances']:.2f} acceptances")
```

## Tips

1. **More data is better**: The models work best with at least 50+ historical records
2. **Use random_seed for reproducibility**: Set `random_seed=42` when testing
3. **Run more simulations for precision**: Use 1000+ simulations for production decisions
4. **Check percentiles**: Use the 10th and 90th percentiles to understand risk
5. **Validate assumptions**: Compare predictions with actual outcomes to improve the model

## Getting Help

- Check the comprehensive README.md for detailed documentation
- Run example_usage.py to see working examples
- Look at the test files in tests/ for more usage patterns
