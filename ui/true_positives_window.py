# ui/true_positives_window.py
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QPushButton, QWidget, QFileDialog, QMessageBox
)
from models.wine_analyzer import WineAnalyzer


class TruePositivesWindow(QMainWindow):
    def __init__(self, analyzer: WineAnalyzer):
        super().__init__()

        style_path = os.path.join(os.path.dirname(__file__), "styles", "true_positives.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

        self.analyzer = analyzer
        self.setWindowTitle("Истински положителни вина")
        self.setGeometry(300, 300, 800, 600)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.df = self.analyzer.get_true_positives()

        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                value = str(self.df.iat[i, j])
                self.table.setItem(i, j, QTableWidgetItem(value))

                self.table.resizeColumnsToContents()

        layout.addWidget(self.table)

        # Export button
        self.export_button = QPushButton("💾 Експортирай в Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Запази като", "true_positives.xlsx", "Excel файлове (*.xlsx)"
        )
        if file_path:
            try:
                self.df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Успех", f"Файлът е запазен успешно:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Грешка", f"Грешка при запис:\n{str(e)}")
