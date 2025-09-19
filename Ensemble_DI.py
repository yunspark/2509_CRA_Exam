import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from sklearn.linear_model import Ridge, ElasticNet, LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from sklearn.datasets import make_regression

from tabpfn import TabPFNRegressor


class BaseModel(ABC):
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        pass


class RidgeModel(BaseModel):
    def __init__(self):
        self.model = Ridge()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)


class XGBoostModel(BaseModel):
    def __init__(self):
        self.model = xgb.XGBRegressor()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)


class TabPFNModel(BaseModel):
    def __init__(self):
        self.model = TabPFNRegressor()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)


class EnsembleStrategy(ABC):
    @abstractmethod
    def combine_predictions(
        self, meta_train: np.ndarray, y_train: np.ndarray, meta_test: np.ndarray
    ) -> np.ndarray:
        pass


class SimpleStrategy(EnsembleStrategy):
    def combine_predictions(
        self, meta_train: np.ndarray, y_train: np.ndarray, meta_test: np.ndarray
    ) -> np.ndarray:
        return np.mean(meta_test, axis=1)  # simple average


class LinearStrategy(EnsembleStrategy):
    def combine_predictions(
        self, meta_train: np.ndarray, y_train: np.ndarray, meta_test: np.ndarray
    ) -> np.ndarray:
        meta_model = ElasticNet(alpha=1.0)
        meta_model.fit(meta_train, y_train)
        return meta_model.predict(meta_test)


class NoneLinearStrategy(EnsembleStrategy):
    def combine_predictions(
        self, meta_train: np.ndarray, y_train: np.ndarray, meta_test: np.ndarray
    ) -> np.ndarray:
        meta_model = SVR(kernel="rbf", C=1.0)
        meta_model.fit(meta_train, y_train)
        return meta_model.predict(meta_test)


class EnsembleEvaluator:  # DI applied
    def __init__(self, base_models: List[BaseModel], strategy: EnsembleStrategy):
        self.base_models = base_models
        self.strategy = strategy

    def train_base_models(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        for model in self.base_models:
            model.fit(X_train, y_train)

    def predict_base_models(self, X_test: np.ndarray) -> np.ndarray:
        predictions = [model.predict(X_test) for model in self.base_models]
        return np.column_stack(predictions)

    def evaluate(self, data: np.ndarray, target: np.ndarray) -> float:
        X_train, X_test, y_train, y_test = train_test_split(
            data, target, test_size=0.2, random_state=42
        )
        self.train_base_models(X_train, y_train)
        meta_train = self.predict_base_models(X_train)
        meta_test = self.predict_base_models(X_test)

        ensemble_pred = self.strategy.combine_predictions(
            meta_train, y_train, meta_test
        )
        return mean_squared_error(y_test, ensemble_pred)


if __name__ == "__main__":
    X, y = make_regression(n_samples=100, n_features=4, random_state=42)
    base_models = [RidgeModel(), XGBoostModel(), TabPFNModel()]

    simple_eval = EnsembleEvaluator(base_models, SimpleStrategy())
    print(simple_eval.evaluate(X, y))

    linear_strategy = EnsembleEvaluator(base_models, LinearStrategy())
    print(linear_strategy.evaluate(X, y))

    nonlinear_eval = EnsembleEvaluator(base_models, NoneLinearStrategy())
    print(nonlinear_eval.evaluate(X, y))
