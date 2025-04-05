import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

class WinePredictor:
    def __init__(self, csv_path="data/winequality-red.csv"):
        self.csv_path = csv_path
        self.model_path = "models/wine_model.pkl"
        self.model = None

        self._load_data()
        self._prepare_model()

    def _load_data(self):
        self.df = pd.read_csv(self.csv_path, sep=";")
        self.features = self.df.drop("quality", axis=1)
        self.labels = self.df["quality"]

    def _prepare_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                self.features, self.labels, test_size=0.2, random_state=42
            )
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            joblib.dump(self.model, self.model_path)

    def predict(self, input_data: dict):
        """Expects input_data as a dictionary with keys matching CSV column names."""
        df = pd.DataFrame([input_data])
        prediction = self.model.predict(df)[0]
        return round(prediction, 2)
