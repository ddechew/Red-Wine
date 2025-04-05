import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel

class PredictorWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Прогноза за качество")
        self.setGeometry(300, 300, 500, 300)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.label = QLabel("Тук ще бъде формата за прогнозиране...", self)
        self.label.move(50, 50)
