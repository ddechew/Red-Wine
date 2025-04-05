import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QTabWidget
)
from PyQt5.QtGui import QFont, QIcon


class InspectWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Преглед на винените данни")
        self.setGeometry(250, 250, 900, 600)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.df = df

        central_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("📊 Данни за вината")
        title_label.setFont(QFont("Arial", 14))
        layout.addWidget(title_label)

        self.table = QTableWidget()
        self.load_dataframe()
        layout.addWidget(self.table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_dataframe(self):
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iat[i, j]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # ❗ Make item read-only
                self.table.setItem(i, j, item)
