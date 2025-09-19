import numpy as np
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression
import xgboost as xgb
from catboost import CatBoostRegressor
import lightgbm as lgb
from typing import Tuple, Optional


TEST_SIZE = 0.2
RANDOM_SEED = 42


class BoostingRegressor(ABC):
    def __init__(self) -> None:
        self._model = None

    @staticmethod
    def _split_data(
        X: np.ndarray, y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED)

    @abstractmethod
    def train_and_predict(self, X: np.ndarray, y: np.ndarray) -> float:
        pass


class XGBoostRegressor(BoostingRegressor):
    def __init__(self) -> None:
        super().__init__()
        self._model = xgb.XGBRegressor(random_state=RANDOM_SEED)

    def train_and_predict(self, X: np.ndarray, y: np.ndarray) -> float:
        X_train, X_test, y_train, y_test = self._split_data(X, y)
        self._model.fit(X_train, y_train)
        predictions = self._model.predict(X_test)
        return mean_squared_error(y_test, predictions)


class LightGBMRegressor(BoostingRegressor):
    def __init__(self) -> None:
        super().__init__()
        self._model = lgb.LGBMRegressor(random_state=RANDOM_SEED)

    def train_and_predict(self, X: np.ndarray, y: np.ndarray) -> float:
        X_train, X_test, y_train, y_test = self._split_data(X, y)
        self._model.fit(X_train, y_train)
        predictions = self._model.predict(X_test)
        return mean_squared_error(y_test, predictions)


class CatBoostReg(BoostingRegressor):
    def __init__(self) -> None:
        super().__init__()
        self._model = CatBoostRegressor(verbose=False)

    def train_and_predict(self, X: np.ndarray, y: np.ndarray) -> float:
        X_train, X_test, y_train, y_test = self._split_data(X, y)
        self._model.fit(X_train, y_train)
        predictions = self._model.predict(X_test)
        return mean_squared_error(y_test, predictions)


class RegressorFactory:
    _regressors = {
        "xgboost": XGBoostRegressor,
        "catboost": CatBoostReg,
        "lightgbm": LightGBMRegressor,
    }

    @staticmethod
    def create_regressor(regressor_type: str) -> BoostingRegressor:
        regressor_class = RegressorFactory._regressors.get(regressor_type.lower())
        if regressor_class is None:
            raise ValueError(f"Invalid regressor type: {regressor_type}")
        return regressor_class()


if __name__ == "__main__":
    X, y = make_regression(n_samples=100, n_features=4, random_state=RANDOM_SEED)

    for reg_type in ["xgboost", "catboost", "lightgbm", "invalid_type"]:
        try:
            regressor = RegressorFactory.create_regressor(reg_type)
            mse = regressor.train_and_predict(X, y)
            print(f"{reg_type.capitalize()} MSE: {mse}")
        except ValueError as e:
            print(f"{reg_type.capitalize()} ERROR: {e}")
