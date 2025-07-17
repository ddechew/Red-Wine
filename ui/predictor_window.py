from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel,
    QPushButton, QFormLayout, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont
import os
from PyQt5.QtGui import QIcon

class PredictorWindow(QMainWindow):
    def __init__(self, predictor):
        super().__init__()
        self.setWindowTitle("Прогнозиране на качеството на виното")
        self.setGeometry(300, 300, 400, 500)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.predictor = predictor

        layout = QVBoxLayout()

        title = QLabel("Въведете стойности за характеристиките")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.inputs = {}

        for column in self.predictor.features.columns:
            spin = QDoubleSpinBox()
            spin.setRange(0, 100)
            spin.setDecimals(3)
            spin.setSingleStep(0.1)
            self.form_layout.addRow(column, spin)
            self.inputs[column] = spin

        layout.addLayout(self.form_layout)

        predict_btn = QPushButton("Прогнозирай качество")
        predict_btn.clicked.connect(self.predict_quality)
        layout.addWidget(predict_btn)

        example_btn = QPushButton("📊 Попълни примерни стойности")
        example_btn.clicked.connect(self.fill_example_data)
        layout.addWidget(example_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def predict_quality(self):
        input_data = {name: spin.value() for name, spin in self.inputs.items()}
        predicted = self.predictor.predict(input_data)
        category = "good 🍷" if predicted >= 7 else "not good ❌"
        QMessageBox.information(
            self, "Прогноза", f"Прогнозирано качество: {predicted}\nКатегория: {category}"
        )

    def fill_example_data(self):
        example = {
            "fixed acidity": 7.9,
            "volatile acidity": 0.64,
            "citric acid": 0.34,
            "residual sugar": 2.5,
            "chlorides": 0.076,
            "free sulfur dioxide": 8.0,
            "total sulfur dioxide": 17.0,
            "density": 0.99235,
            "pH": 3.15,
            "sulphates": 0.72,
            "alcohol": 13.1
        }
        for key, value in example.items():
            if key in self.inputs:
                self.inputs[key].setValue(value)
