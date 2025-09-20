import pytest
import numpy as np
from Regressor_factory import (
    RegressorFactory,
    XGBoostRegressor,
    TEST_SIZE,
    RANDOM_SEED,
)


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


@pytest.fixture
def dummy_data():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([1.0, 2.0, 3.0, 4.0])
    return X, y


@pytest.fixture
def mock_split(mocker):
    return mocker.patch(
        "Regressor_factory.train_test_split",
        return_value=(
            np.array([[1, 2], [3, 4]]),  # X_train
            np.array([[5, 6], [7, 8]]),  # X_test
            np.array([1.0, 2.0]),  # y_train
            np.array([3.0, 4.0]),  # y_test
        ),
    )


@pytest.fixture
def mock_xgboost(mocker):
    mock_model = mocker.Mock()
    mock_model.fit.return_value = None
    mock_model.predict.return_value = np.array([1.0, 2.0])
    mocker.patch("Regressor_factory.xgb.XGBRegressor", return_value=mock_model)
    return mock_model


@pytest.fixture
def mock_mse(mocker):
    mock_model = mocker.Mock()
    mock_model.mean_squared_error.return_value = 0.05
    mocker.patch("Regressor_factory.mean_squared_error", return_value=mock_model)
    return mock_model


def test_xgboost_regressor_split_data(dummy_data, mock_split):
    regressor = XGBoostRegressor()
    X, y = dummy_data
    X_train, X_test, y_train, y_test = regressor._split_data(X, y)

    mock_split.assert_called_once_with(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )
    assert X_train.shape == (2, 2)
    assert X_test.shape == (2, 2)
    assert y_train.shape == (2,)
    assert y_test.shape == (2,)


def test_xgboost_regressor_predicts_with_low_mse(
    dummy_data, mock_split, mock_xgboost, mock_mse
):
    regressor = RegressorFactory.create_regressor("xgboost")
    assert isinstance(regressor, XGBoostRegressor)


def test_regressor_factory_handles_invalid_type():
    with pytest.raises(ValueError):
        RegressorFactory().create_regressor("invalid")
