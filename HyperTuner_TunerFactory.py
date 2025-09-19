from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, Type, Tuple, Any

# Constants
RANDOM_SEED = 42
TEST_SIZE = 0.2
NUM_TRIALS = 10


# Abstract Hyperparameter Tuner
class HyperTuner(ABC):
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    @abstractmethod
    def tune(self):
        pass

    def build_model(self, params):
        return RandomForestRegressor(**params, random_state=RANDOM_SEED)


# Optuna Tuner
class OptunaTuner(HyperTuner):
    def tune(self):
        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 10, 200),
                "max_depth": trial.suggest_int("max_depth", 1, 20),
            }
            model = self.build_model(params)
            model.fit(self.X_train, self.y_train)
            return evaluate_model(model, self.X_test, self.y_test)

        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=NUM_TRIALS)
        return study.best_params


class HyperoptTuner(HyperTuner):
    def __init__(self, X_train: Any, y_train: Any, X_test: Any, y_test: Any):
        pass  # Implementation

    def tune(self):
        pass


class RayTuneTuner(HyperTuner):
    def __init__(self, X_train: Any, y_train: Any, X_test: Any, y_test: Any):
        pass  # Implementation

    def tune(self):
        pass


# # Tuner Factory (Factory Pattern)
# class TunerFactory:
#     @staticmethod
#     def create_tuner(tuner_type, X_train, y_train, X_test, y_test):
#         if tuner_type == 'optuna':
#             return OptunaTuner(X_train, y_train, X_test, y_test)
#         elif tuner_type == 'hyperopt':
#             return HyperoptTuner(X_train, y_train, X_test, y_test)
#         elif tuner_type == 'ray_tune':
#             return RayTuneTuner(X_train, y_train, X_test, y_test)
#         else:
#             raise ValueError("Unknown tuner type")


class TunerFactory:
    _tuner_classes: Dict[str, Type] = {
        "optuna": OptunaTuner,
        "hyperopt": HyperoptTuner,
        "ray_tune": RayTuneTuner,
    }

    @staticmethod
    def create_tuner(
        tuner_type: str, X_train: Any, y_train: Any, X_test: Any, y_test: Any
    ) -> HyperTuner:
        tuner_class = TunerFactory._tuner_classes.get(tuner_type)
        if tuner_class is None:
            raise ValueError(f"Unknown tuner type: {tuner_type}")
        return tuner_class(X_train, y_train, X_test, y_test)
