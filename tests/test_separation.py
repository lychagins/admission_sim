import numpy as np
import pytest
from example_usage import create_sample_data
from admission_sim.waiver_probability import WaiverProbabilityEstimator


def test_no_perfect_prediction_on_training_data():
    """Fit the estimator and ensure it does not perfectly predict the training labels.

    This test is specification-independent: it fits the model on the toy data,
    predicts on the same data, and fails if predictions exactly match labels
    (which indicates complete separation or another degenerate case).
    """
    data = create_sample_data()
    estimator = WaiverProbabilityEstimator()

    try:
        estimator.fit(data)
    except RuntimeError as e:
        pytest.fail(f"Model fit failed (possible complete separation): {e}")

    results = estimator.estimate_acceptance_rates(data)
    probs = np.array([r['acceptance_probability'] for r in results])
    preds = (probs >= 0.5).astype(int)
    actual = np.array([1 if d['accepted'] else 0 for d in data])

    assert not np.array_equal(preds, actual), (
        "Model perfectly predicts training labels — dataset is degenerate for MLE."
    )
