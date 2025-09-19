import pytest
import numpy as np
from Regressor_factory import RegressorFactory, XGBoostRegressor


# AAA : Arrange, Act, Assert
def test_split():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([1.0, 2.0, 3.0, 4.0])
    reg = XGBoostRegressor()

    x1, x2, y1, y2 = reg._split_data(X, y)
    assert x1.shape == (3, 2)
    assert x2.shape == (1, 2)
    assert y1.shape == (3,)
    assert y2.shape == (1,)


def test_xgb_empty_input(mocker):
    X = np.array([])
    y = np.array([])
    reg = XGBoostRegressor()
    with pytest.raises(ValueError):
        reg.train_and_predict(X, y)


def test_factory():
    reg = RegressorFactory().create_regressor("xgboost")
    assert isinstance(reg, XGBoostRegressor)

    with pytest.raises(ValueError):
        RegressorFactory().create_regressor("invalid")


# Test xgboost
def test_xgb(mocker):
    # Data
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([1.0, 2.0, 3.0, 4.0])

    # Mock model
    mock_model = mocker.Mock()
    mock_model.fit.return_value = None
    mock_model.predict.return_value = np.array([1.0])
    mocker.patch("Regressor_factory.xgb.XGBRegressor", return_value=mock_model)
    mocker.patch("Regressor_factory.mean_squared_error", return_value=0.05)

    # Run
    reg = XGBoostRegressor()
    mse = reg.train_and_predict(X, y)

    # Verify
    assert mse == 0.05
    mock_model.fit.assert_called_once()
    mock_model.predict.assert_called_once()


# test_boosting_regressors.py
