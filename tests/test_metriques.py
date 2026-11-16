"""Tests des métriques NumPy, comparées à scikit-learn."""
import numpy as np
import pytest
from sklearn.metrics import mean_squared_error, r2_score

from exceptions import DonneeInvalideError
from metriques import r2, rmse


@pytest.fixture
def valeurs():
    rng = np.random.default_rng(42)
    y = rng.uniform(40, 90, 200)
    return y, y + rng.normal(0, 3, 200)


def test_rmse_coincide_avec_sklearn(valeurs):
    y, yp = valeurs
    assert rmse(y, yp) == pytest.approx(mean_squared_error(y, yp) ** 0.5)


def test_r2_coincide_avec_sklearn(valeurs):
    y, yp = valeurs
    assert r2(y, yp) == pytest.approx(r2_score(y, yp))


def test_r2_prediction_parfaite():
    assert r2([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)


def test_r2_prediction_de_la_moyenne():
    assert r2([1, 2, 3], [2, 2, 2]) == pytest.approx(0.0)


def test_rmse_tailles_differentes():
    with pytest.raises(DonneeInvalideError):
        rmse([1, 2, 3], [1, 2])


def test_r2_valeurs_constantes():
    with pytest.raises(DonneeInvalideError):
        r2([5, 5, 5], [4, 5, 6])