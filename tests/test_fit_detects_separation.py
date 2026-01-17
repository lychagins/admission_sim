import pytest
import numpy as np
import statsmodels.api as sm

from admission_sim.waiver_probability import WaiverProbabilityEstimator


def test_fit_detects_separation(monkeypatch):
    """If the fitted model perfectly predicts training labels, fit() should raise RuntimeError."""
    # Construct a small toy dataset (content doesn't matter because we'll stub the fit)
    data = [
        {'priority_score': 1.0, 'waiver': 0.0, 'accepted': 0, 'background_score': 0},
        {'priority_score': 2.0, 'waiver': 0.0, 'accepted': 0, 'background_score': 0},
        {'priority_score': 10.0, 'waiver': 1.0, 'accepted': 1, 'background_score': 0},
        {'priority_score': 11.0, 'waiver': 1.0, 'accepted': 1, 'background_score': 0},
    ]

    y = np.array([1 if d['accepted'] else 0 for d in data])

    # Dummy fit that returns an object whose predict() returns the true labels
    class DummyResult:
        def predict(self, X):
            return y

    def fake_fit(self, *args, **kwargs):
        return DummyResult()

    # Monkeypatch the Logit.fit method used by the estimator
    monkeypatch.setattr(sm.Logit, 'fit', fake_fit)

    estimator = WaiverProbabilityEstimator()

    with pytest.raises(RuntimeError):
        estimator.fit(data)
