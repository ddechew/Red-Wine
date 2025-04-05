import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox
)
from ui.inspect_window import InspectWindow
from ui.predictor_window import PredictorWindow
import pandas as pd
from ui.analysis_window import AnalysisWindow
from models.wine_analyzer import WineAnalyzer
from ui.true_positives_window import TruePositivesWindow
from models.predictor import WinePredictor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Съветник за качеството на червено вино - Kaufland")
        self.setGeometry(200, 200, 600, 400)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))


        self.df = None

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.import_button = QPushButton("📂 Импортирай CSV файл")
        self.import_button.clicked.connect(self.import_csv)
        layout.addWidget(self.import_button)

        self.inspect_button = QPushButton("👁️ Прегледай данните")
        self.inspect_button.setEnabled(False)
        self.inspect_button.clicked.connect(self.open_inspect_window)
        layout.addWidget(self.inspect_button)

        self.analysis_button = QPushButton("📈 Анализ на модела")
        self.analysis_button.setEnabled(False)
        self.analysis_button.clicked.connect(self.open_analysis_window)
        layout.addWidget(self.analysis_button)

        self.tp_button = QPushButton("✅ Прегледай най-добрите вина")
        self.tp_button.setEnabled(False)
        self.tp_button.clicked.connect(self.open_true_positives)
        layout.addWidget(self.tp_button)

        self.predictor_button = QPushButton("🤖 Прогнозирай качество")
        self.predictor_button.setEnabled(False)
        self.predictor_button.clicked.connect(self.open_predictor_window)
        layout.addWidget(self.predictor_button)

        self.status_label = QLabel("Моля, импортирайте CSV файл за начало.")
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Избери CSV файл", "", "CSV файлове (*.csv);;Всички файлове (*)"
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=";")
                # ✅ Initialize WineAnalyzer here
                self.analyzer = WineAnalyzer(file_path)
                self.analyzer.load_and_prepare_data()
                self.analyzer.train_model()

                self.status_label.setText(f"📄 Зареден файл: {file_path}")
                self.inspect_button.setEnabled(True)
                self.predictor_button.setEnabled(True)
                self.analysis_button.setEnabled(True)
                self.tp_button.setEnabled(True)
                QMessageBox.information(self, "Успех", "CSV файлът е зареден успешно!")
            except Exception as e:
                QMessageBox.critical(self, "Грешка", f"Проблем при зареждане: {str(e)}")

    def open_inspect_window(self):
        if self.df is not None:
            self.inspect_window = InspectWindow(self.df)
            self.inspect_window.show()

    def open_predictor_window(self):
        if self.df is not None:
            # Use the same path that was used to initialize WineAnalyzer
            csv_path = self.analyzer.csv_path
            predictor = WinePredictor(csv_path)
            self.predictor_window = PredictorWindow(predictor)
            self.predictor_window.show()

    def open_analysis_window(self):
        if self.df is not None:
            self.analysis_window = AnalysisWindow(self.analyzer)
            self.analysis_window.show()

    def open_true_positives(self):
        if hasattr(self, 'analyzer'):
            self.tp_window = TruePositivesWindow(self.analyzer)
            self.tp_window.show()
