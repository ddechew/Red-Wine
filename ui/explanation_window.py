import os

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QTextBrowser,
    QPushButton, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy

class ExplanationWindow(QMainWindow):
    def __init__(self, analyzer):
        super().__init__()
        self.setWindowTitle("Обяснение на анализа")
        self.setGeometry(300, 300, 700, 600)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_logo.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.analyzer = analyzer
        explanation_text = self.analyzer.get_explanation_text()

        layout = QVBoxLayout()

        # Text area
        self.text_browser = QTextBrowser()
        self.text_browser.setPlainText(explanation_text)
        self.text_browser.setFont(QFont("Arial", 11))
        self.text_browser.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                padding: 10px;
                background-color: #f9f9f9;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.text_browser)

        # Label for table
        table_label = QLabel("📋 Основни критерии за добро/премиум вино:")
        table_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(table_label)

        # Criteria table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels(["Критерий", "Препоръчана стойност"])

        criteria = [
            ("Алкохол", "≥ 10"),
            ("Сулфати", "≥ 0.6"),
            ("pH / киселинност", "Баланс между 3.1 и 3.5")
        ]

        for row, (criterion, value) in enumerate(criteria):
            self.table.setItem(row, 0, QTableWidgetItem(criterion))
            self.table.setItem(row, 1, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionsMovable(False)
        self.table.horizontalHeader().setSectionsClickable(False)

        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), QSizePolicy.Maximum)
        self.table.setFixedHeight(self.table.verticalHeader().length() + self.table.horizontalHeader().height() + 10)

        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.setShowGrid(False)

        table_container = QWidget()
        table_layout = QHBoxLayout()

        table_layout.addWidget(self.table)
        table_layout.addStretch()  # Left spacer

        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table.setMaximumWidth(400)  # Or 450 depending on look

        table_container.setLayout(table_layout)
        layout.addWidget(table_container)

        # Export to PDF
        self.export_btn = QPushButton("💾 Експортирай в PDF")
        self.export_btn.clicked.connect(self.export_to_pdf)
        layout.addWidget(self.export_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Запази PDF файла", "wine_analysis_explanation.pdf", "PDF файлове (*.pdf)"
        )
        if file_path:
            from PyQt5.QtGui import QTextDocument
            from PyQt5.QtPrintSupport import QPrinter

            image_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "assets", "kaufland_header.png")
            ).replace("\\", "/")

            explanation = self.text_browser.toPlainText().replace('\n', '<br>')

            html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        margin: 50px;
                        @bottom-right {{
                            content: counter(page);
                            font-size: 12px;
                            color: gray;
                        }}
                    }}

                    @page:first {{
                        @bottom-right {{
                            content: none;
                        }}
                    }}

                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                        counter-reset: page 1;
                    }}

                    .logo-page {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        page-break-after: always;
                    }}

                    .logo {{
                        max-width: 250px;
                        height: auto;
                    }}

                    .content {{
                        position: relative;
                    }}

                    h2 {{
                        font-size: 16pt;
                        margin-top: 0;
                    }}

                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 20px;
                    }}

                    th, td {{
                        border: 1px solid #ccc;
                        padding: 8px;
                        font-size: 13px;
                        text-align: left;
                    }}

                    th {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <!-- Page 1 - centered logo -->
                <div class="logo-page">
                    <img class="logo" src="file:///{image_path}" />
                </div>

                <!-- Page 2 - starts with page number 1 -->
                <div class="content">
                    <h2>🧠 Обяснение на анализа</h2>
                    <p>{self.text_browser.toPlainText().replace('\n', '<br>')}</p>

                    <h3>📋 Основни критерии за добро/премиум вино:</h3>
                    <table>
                        <tr><th>Критерий</th><th>Препоръчана стойност</th></tr>
                        <tr><td>Алкохол</td><td>≥ 10</td></tr>
                        <tr><td>Сулфати</td><td>≥ 0.6</td></tr>
                        <tr><td>pH / киселинност</td><td>Баланс между 3.1 и 3.5</td></tr>
                    </table>
                </div>
            </body>
            </html>
            """

            doc = QTextDocument()
            doc.setHtml(html)

            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)

            doc.print_(printer)

            QMessageBox.information(self, "Успех", f"PDF файлът е създаден успешно:\n{file_path}")




