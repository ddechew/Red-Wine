# ui/confusion_matrix_window.py
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon


class ConfusionMatrixWindow(QMainWindow):
    def __init__(self, y_true, y_pred, classes):
        super().__init__()
        self.setWindowTitle("Матрица на объркване")
        self.setGeometry(300, 300, 600, 400)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.y_true = y_true
        self.y_pred = y_pred
        self.classes = classes

        layout = QVBoxLayout()

        title = QLabel("📉 Матрица на объркване (Confusion Matrix)")
        title.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(title)

        # Plot matrix
        self.plot_confusion_matrix()

        # Export button
        export_btn = QPushButton("💾 Експортирай графиката като PNG")
        export_btn.clicked.connect(self.export_matrix)
        layout.addWidget(export_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def plot_confusion_matrix(self):
        cm = confusion_matrix(self.y_true, self.y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=self.classes, yticklabels=self.classes)
        plt.title("Confusion Matrix")
        plt.xlabel("Предсказано")
        plt.ylabel("Истинско")
        plt.tight_layout()
        plt.show(block=False)

    def export_matrix(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Запази като", "confusion_matrix.png", "PNG Files (*.png)"
        )
        if file_path:
            cm = confusion_matrix(self.y_true, self.y_pred)
            plt.figure(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=self.classes, yticklabels=self.classes)
            plt.title("Confusion Matrix")
            plt.xlabel("Предсказано")
            plt.ylabel("Истинско")
            plt.tight_layout()
            plt.savefig(file_path)
            QMessageBox.information(self, "Успех", "Графиката е запазена успешно.")
