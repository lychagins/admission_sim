"""
Example usage of the admission simulation tool.

This script demonstrates how to use both modules:
1. WaiverProbabilityEstimator - for estimating acceptance probabilities
2. ResamplingSimulator - for simulating student body composition
"""

from admission_sim import WaiverProbabilityEstimator, ResamplingSimulator


def create_sample_data():
    """Create sample admissions data for demonstration."""
    # Sample historical admissions data
    # In practice, this would be loaded from a CSV or database
    admissions_data = [
        {'ranking': 1, 'waiver': 0.5, 'accepted': True, 'background_score': 95, 'student_id': 'S001'},
        {'ranking': 2, 'waiver': 0.4, 'accepted': True, 'background_score': 92, 'student_id': 'S002'},
        {'ranking': 3, 'waiver': 0.3, 'accepted': True, 'background_score': 88, 'student_id': 'S003'},
        {'ranking': 4, 'waiver': 0.5, 'accepted': True, 'background_score': 85, 'student_id': 'S004'},
        {'ranking': 5, 'waiver': 0.2, 'accepted': False, 'background_score': 82, 'student_id': 'S005'},
        {'ranking': 6, 'waiver': 0.6, 'accepted': True, 'background_score': 80, 'student_id': 'S006'},
        {'ranking': 7, 'waiver': 0.3, 'accepted': False, 'background_score': 78, 'student_id': 'S007'},
        {'ranking': 8, 'waiver': 0.4, 'accepted': True, 'background_score': 75, 'student_id': 'S008'},
        {'ranking': 9, 'waiver': 0.1, 'accepted': False, 'background_score': 72, 'student_id': 'S009'},
        {'ranking': 10, 'waiver': 0.5, 'accepted': True, 'background_score': 70, 'student_id': 'S010'},
        {'ranking': 11, 'waiver': 0.2, 'accepted': False, 'background_score': 68, 'student_id': 'S011'},
        {'ranking': 12, 'waiver': 0.7, 'accepted': True, 'background_score': 65, 'student_id': 'S012'},
        {'ranking': 13, 'waiver': 0.3, 'accepted': False, 'background_score': 63, 'student_id': 'S013'},
        {'ranking': 14, 'waiver': 0.4, 'accepted': True, 'background_score': 60, 'student_id': 'S014'},
        {'ranking': 15, 'waiver': 0.1, 'accepted': False, 'background_score': 58, 'student_id': 'S015'},
    ]
    return admissions_data


def example_waiver_probability():
    """Demonstrate the waiver probability estimator."""
    print("=" * 60)
    print("EXAMPLE 1: Waiver Probability Estimation")
    print("=" * 60)
    
    # Create and fit the model
    estimator = WaiverProbabilityEstimator()
    admissions_data = create_sample_data()
    
    print("\nFitting model with historical admissions data...")
    estimator.fit(admissions_data)
    print("Model fitted successfully!")
    
    # Predict for new students
    print("\nPredicting acceptance probabilities for new students:")
    print("-" * 60)
    
    new_students = [
        {'ranking': 3, 'waiver': 0.5, 'background_score': 90},
        {'ranking': 7, 'waiver': 0.3, 'background_score': 75},
        {'ranking': 10, 'waiver': 0.6, 'background_score': 70},
    ]
    
    results = estimator.estimate_acceptance_rates(new_students)
    
    for student in results:
        print(f"Ranking: {student['ranking']}, Waiver: {student['waiver']*100:.0f}%, "
              f"Background Score: {student['background_score']}")
        print(f"  → Acceptance Probability: {student['acceptance_probability']:.2%}")
    
    return estimator


def example_resampling_simulation(estimator):
    """Demonstrate the resampling simulator."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Resampling Simulation")
    print("=" * 60)
    
    # Create simulator
    admissions_data = create_sample_data()
    simulator = ResamplingSimulator(admissions_data, estimator)
    
    # Define waiver allocation strategy
    print("\nSimulating admissions with the following waiver allocation:")
    print("-" * 60)
    
    waiver_allocation = [
        {'ranking': 1, 'waiver': 0.5, 'background_score': 95},
        {'ranking': 2, 'waiver': 0.5, 'background_score': 92},
        {'ranking': 3, 'waiver': 0.4, 'background_score': 88},
        {'ranking': 4, 'waiver': 0.4, 'background_score': 85},
        {'ranking': 5, 'waiver': 0.3, 'background_score': 82},
        {'ranking': 6, 'waiver': 0.3, 'background_score': 80},
        {'ranking': 7, 'waiver': 0.2, 'background_score': 78},
        {'ranking': 8, 'waiver': 0.2, 'background_score': 75},
        {'ranking': 9, 'waiver': 0.1, 'background_score': 72},
        {'ranking': 10, 'waiver': 0.1, 'background_score': 70},
    ]
    
    for student in waiver_allocation:
        print(f"Rank {student['ranking']}: {student['waiver']*100:.0f}% waiver")
    
    # Run simulation
    print("\nRunning 1000 simulations...")
    results = simulator.simulate(
        num_offers=10,
        waiver_allocation=waiver_allocation,
        num_simulations=1000,
        random_seed=42
    )
    
    # Display results
    print("\nSimulation Results:")
    print("-" * 60)
    print(f"Expected acceptances: {results['expected_acceptances']:.2f} ± {results['std_acceptances']:.2f}")
    print(f"Mean ranking of accepted students: {results['mean_ranking']:.2f}")
    print(f"Mean background score: {results['composition_stats']['mean_background_score']:.2f}")
    
    print("\nAcceptance Distribution:")
    for count in sorted(results['acceptance_distribution'].keys()):
        freq = results['acceptance_distribution'][count]
        bar = '█' * int(freq / 20)
        print(f"  {count} acceptances: {freq:4d} times {bar}")
    
    print("\nPercentiles:")
    for percentile, value in results['percentiles'].items():
        print(f"  {percentile}: {value:.1f}")


def example_optimization():
    """Demonstrate waiver allocation optimization."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Waiver Allocation Optimization")
    print("=" * 60)
    
    admissions_data = create_sample_data()
    
    # Create estimator and fit
    estimator = WaiverProbabilityEstimator()
    estimator.fit(admissions_data)
    
    # Create simulator
    simulator = ResamplingSimulator(admissions_data, estimator)
    
    # Optimize allocation
    print("\nFinding optimal waiver allocation:")
    print("  - Making 15 offers")
    print("  - Total waiver budget: 5.0 (500%)")
    print("  - Target acceptances: 10 students")
    print("\nOptimizing...")
    
    optimization_result = simulator.optimize_waiver_allocation(
        num_offers=15,
        total_waiver_budget=5.0,
        target_acceptances=10,
        num_simulations=1000
    )
    
    print("\nOptimized Allocation:")
    print("-" * 60)
    for student in optimization_result['allocation'][:5]:  # Show first 5
        print(f"Rank {student['ranking']}: {student['waiver']*100:.1f}% waiver")
    print("  ...")
    
    results = optimization_result['simulation_results']
    print(f"\nExpected acceptances: {results['expected_acceptances']:.2f}")
    print(f"Meets target: {optimization_result['meets_target']}")


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
    
    # Example 3: Optimization
    example_optimization()
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
