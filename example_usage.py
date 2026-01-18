"""
Example usage of the admission simulation tool.

This script demonstrates how to use the estimator and simulator:
- `WaiverProbabilityEstimator` for estimating acceptance probabilities
- `ResamplingSimulator` for simulating student body composition

Note: The package does not include a built-in waiver-allocation optimizer. The
`ResamplingSimulator` requires a fitted estimator (or compatible model) passed
into its constructor and uses Monte Carlo sampling to simulate outcomes.
"""

from admission_sim import WaiverProbabilityEstimator, ResamplingSimulator


def create_sample_data():
    """Create sample admissions data for demonstration."""
    # Sample historical admissions data
    admissions_data = [
        {'priority_score': 95.5, 'waiver': 0.5, 'accepted': 1, 'background_score': 95, 'student_id': 'S001'},
        {'priority_score': 92.3, 'waiver': 0.4, 'accepted': 1, 'background_score': 92, 'student_id': 'S002'},
        {'priority_score': 88.7, 'waiver': 0.3, 'accepted': 1, 'background_score': 88, 'student_id': 'S003'},
        {'priority_score': 85.2, 'waiver': 0.5, 'accepted': 1, 'background_score': 85, 'student_id': 'S004'},
        {'priority_score': 82.1, 'waiver': 0.2, 'accepted': 0, 'background_score': 82, 'student_id': 'S005'},
        {'priority_score': 80.4, 'waiver': 0.6, 'accepted': 1, 'background_score': 80, 'student_id': 'S006'},
        {'priority_score': 78.9, 'waiver': 0.3, 'accepted': 0, 'background_score': 78, 'student_id': 'S007'},
        {'priority_score': 75.6, 'waiver': 0.4, 'accepted': 1, 'background_score': 75, 'student_id': 'S008'},
        {'priority_score': 72.3, 'waiver': 0.1, 'accepted': 0, 'background_score': 72, 'student_id': 'S009'},
        {'priority_score': 70.8, 'waiver': 0.5, 'accepted': 1, 'background_score': 70, 'student_id': 'S010'},
        {'priority_score': 68.5, 'waiver': 0.2, 'accepted': 0, 'background_score': 68, 'student_id': 'S011'},
        {'priority_score': 65.9, 'waiver': 0.7, 'accepted': 1, 'background_score': 65, 'student_id': 'S012'},
        {'priority_score': 63.2, 'waiver': 0.3, 'accepted': 0, 'background_score': 63, 'student_id': 'S013'},
        {'priority_score': 60.7, 'waiver': 0.4, 'accepted': 1, 'background_score': 60, 'student_id': 'S014'},
        {'priority_score': 58.1, 'waiver': 0.1, 'accepted': 0, 'background_score': 58, 'student_id': 'S015'},
        {'priority_score': 84.0, 'waiver': 0.4, 'accepted': 0, 'background_score': 84, 'student_id': 'S016'},
        {'priority_score': 60.0, 'waiver': 0.1, 'accepted': 1, 'background_score': 60, 'student_id': 'S017'},
    ]
    return admissions_data


def example_waiver_probability():
    """Demonstrate the waiver probability estimator."""
    print("=" * 60)
    print("EXAMPLE 1: Waiver Probability Estimation")
    print("=" * 60)
    
    estimator = WaiverProbabilityEstimator()
    admissions_data = create_sample_data()
    
    print("\nFitting model with historical admissions data...")
    estimator.fit(admissions_data)
    print("Model fitted successfully!")
    return estimator


def example_resampling_simulation(estimator):
    """Demonstrate the resampling simulator."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Resampling Simulation")
    print("=" * 60)
    
    admissions_data = create_sample_data()
    simulator = ResamplingSimulator(admissions_data, estimator)
    
    print("\nSimulating admissions with the following waiver allocation:")
    print("-" * 60)
    
    waiver_allocation = [
        {'priority_score': 95.5, 'waiver': 0.5, 'background_score': 95},
        {'priority_score': 92.3, 'waiver': 0.5, 'background_score': 92},
        {'priority_score': 88.7, 'waiver': 0.4, 'background_score': 88},
        {'priority_score': 85.2, 'waiver': 0.4, 'background_score': 85},
        {'priority_score': 82.1, 'waiver': 0.3, 'background_score': 82},
        {'priority_score': 80.4, 'waiver': 0.3, 'background_score': 80},
        {'priority_score': 78.9, 'waiver': 0.2, 'background_score': 78},
        {'priority_score': 75.6, 'waiver': 0.2, 'background_score': 75},
        {'priority_score': 72.3, 'waiver': 0.1, 'background_score': 72},
        {'priority_score': 70.8, 'waiver': 0.1, 'background_score': 70},
    ]
    
    for student in waiver_allocation:
        print(f"Priority Score {student['priority_score']:.1f}: {student['waiver']*100:.0f}% waiver")
    
    print("\nRunning 1000 simulations...")
    results = simulator.simulate(
        num_offers=10,
        waiver_allocation=waiver_allocation,
        num_simulations=1000,
        random_seed=42
    )
    
    print("\nSimulation Results:")
    print("-" * 60)
    print(f"Expected acceptances: {results['expected_acceptances']:.2f} ± {results['std_acceptances']:.2f}")
    print(f"Mean priority score of accepted students: {results['mean_priority_score']:.2f}")
    print(f"Mean background score: {results['composition_stats']['mean_background_score']:.2f}")
    
    print("\nAcceptance Distribution:")
    for count in sorted(results['acceptance_distribution'].keys()):
        freq = results['acceptance_distribution'][count]
        bar = '█' * int(freq / 20)
        print(f"  {count} acceptances: {freq:4d} times {bar}")
    
    print("\nPercentiles:")
    for percentile, value in results['percentiles'].items():
        print(f"  {percentile}: {value:.1f}")




def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "ADMISSION SIMULATION TOOL EXAMPLES" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Example 1: Waiver Probability
    estimator = example_waiver_probability()
    
    # Example 2: Resampling Simulation
    example_resampling_simulation(estimator)
    
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
