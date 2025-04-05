# ui/feature_importance_window.py

import os
import matplotlib.pyplot as plt
import seaborn as sns

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLabel, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class FeatureImportanceWindow(QMainWindow):
    def __init__(self, importance_df):
        super().__init__()
        self.setWindowTitle("Важност на характеристиките")
        self.setGeometry(300, 300, 700, 500)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        title = QLabel("Характеристики, които влияят най-много на прогнозата")
        title.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Характеристика", "Важност"])

        sorted_df = importance_df.sort_values(by="Importance", ascending=False).reset_index(drop=True)
        self.table.setRowCount(len(sorted_df))

        for i in range(len(sorted_df)):
            feature = sorted_df.loc[i, "Feature"]
            importance = sorted_df.loc[i, "Importance"]
            self.table.setItem(i, 0, QTableWidgetItem(feature))
            self.table.setItem(i, 1, QTableWidgetItem(f"{importance:.4f}"))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Export chart button
        self.export_btn = QPushButton("💾 Експортирай графиката като PNG")
        self.export_btn.clicked.connect(lambda: self.export_chart(importance_df))
        layout.addWidget(self.export_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def export_chart(self, importance_df):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Запази като", "feature_importance.png", "PNG Files (*.png)"
        )
        if file_path:
            plt.figure(figsize=(10, 6))
            sns.barplot(x="Importance", y="Feature", data=importance_df)
            plt.title("Feature Importance")
            plt.tight_layout()
            plt.savefig(file_path)
            QMessageBox.information(self, "Успех", "Графиката е запазена успешно.")
