# ui/analysis_window.py
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
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
        self.analyzer.show_feature_importance_plot()

    def show_confusion_matrix(self):
        self.analyzer.show_confusion_matrix_plot()

    def show_decision_tree(self):
        graph = self.analyzer.export_decision_tree()
        graph.view()
