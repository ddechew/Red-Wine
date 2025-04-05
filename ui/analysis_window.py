import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from ui.explanation_window import ExplanationWindow
from ui.feature_importance_window import FeatureImportanceWindow
from ui.confusion_matrix_window import ConfusionMatrixWindow
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from models.wine_analyzer import WineAnalyzer


class AnalysisWindow(QMainWindow):
        def __init__(self, analyzer: WineAnalyzer):
            super().__init__()
            self.setWindowTitle("Анализ на винените данни")
            self.setGeometry(300, 300, 500, 400)

            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
            self.setWindowIcon(QIcon(icon_path))

            self.analyzer = analyzer

            layout = QVBoxLayout()

            title = QLabel("Визуализации и анализ")
            title.setFont(QFont("Arial", 14))
            layout.addWidget(title)

            self.btn_explanation = QPushButton("🧠 Обяснение на анализа")
            self.btn_explanation.clicked.connect(self.open_explanation_window)
            layout.addWidget(self.btn_explanation)

            self.btn_feat_imp = QPushButton("🔍 Важност на характеристиките")
            self.btn_feat_imp.clicked.connect(self.show_feature_importance)
            layout.addWidget(self.btn_feat_imp)

            self.btn_confusion = QPushButton("📉 Матрица на объркване")
            self.btn_confusion.clicked.connect(self.show_confusion_matrix)
            layout.addWidget(self.btn_confusion)

            self.btn_tree = QPushButton("🌳 Визуализирай Decision Tree")
            self.btn_tree.clicked.connect(self.show_decision_tree)
            layout.addWidget(self.btn_tree)


            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

        def show_feature_importance(self):
            importance_df = self.analyzer.get_feature_importance_data()
            self.feature_window = FeatureImportanceWindow(importance_df)
            self.feature_window.show()

        def show_confusion_matrix(self):
            y_true = self.analyzer.y_test
            y_pred = self.analyzer.y_pred
            classes = self.analyzer.clf.classes_

            self.conf_window = ConfusionMatrixWindow(y_true, y_pred, classes)
            self.conf_window.show()

        def show_decision_tree(self):
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Запази дървото като", "decision_tree", "PNG Files (*.png)"
            )
            if file_path:
                try:
                    # Graphviz expects the filename WITHOUT extension
                    if file_path.endswith(".png"):
                        file_path = file_path[:-4]

                    graph = self.analyzer.export_decision_tree()
                    graph.format = 'png'

                    # Render and get the actual path (.png will be auto-appended)
                    output_path = graph.render(filename=file_path, cleanup=True)

                    QMessageBox.information(self, "Успех", f"Дървото е експортирано успешно:\n{output_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Грешка", f"Грешка при експортиране: {e}")

        def open_explanation_window(self):
                self.expl_window = ExplanationWindow(self.analyzer)
                self.expl_window.show()
