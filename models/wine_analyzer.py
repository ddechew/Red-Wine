import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import graphviz
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

class WineAnalyzer:
        def __init__(self, csv_path):
            self.csv_path = csv_path
            self.df = None
            self.clf = None
            self.X_train = self.X_test = self.y_train = self.y_test = None
            self.y_pred = None

        def load_and_prepare_data(self):
            self.df = pd.read_csv(self.csv_path, sep=';')
            self.df['quality_label'] = self.df['quality'].apply(lambda q: 'good' if q >= 7 else 'not good')
            self.df['Excel_Row'] = self.df.index + 2

            X = self.df.drop(['quality', 'quality_label', 'Excel_Row'], axis=1)
            y = self.df['quality_label']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )

        def train_model(self):
            self.clf = DecisionTreeClassifier(random_state=42)
            self.clf.fit(self.X_train, self.y_train)
            self.y_pred = self.clf.predict(self.X_test)

        def get_feature_importance_plot(self):
            importances = pd.DataFrame({
                'Feature': self.X_train.columns,
                'Importance': self.clf.feature_importances_
            }).sort_values(by='Importance', ascending=False)

            plt.figure(figsize=(10, 6))
            sns.barplot(x='Importance', y='Feature', data=importances)
            plt.title("Feature Importance")
            plt.tight_layout()
            plt.show(block=False)

        def get_confusion_matrix_plot(self):
            cm = confusion_matrix(self.y_test, self.y_pred)
            plt.figure(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=self.clf.classes_, yticklabels=self.clf.classes_)
            plt.title("Confusion Matrix")
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            plt.tight_layout()
            plt.show(block=False)

        def export_decision_tree(self, out_file="wine_decision_tree"):
            dot_data = export_graphviz(
                self.clf,
                out_file=None,
                feature_names=self.X_train.columns,
                class_names=self.clf.classes_,
                filled=True,
                rounded=True,
                special_characters=True
            )
            graph = graphviz.Source(dot_data)
            graph.render(out_file)
            return graph

        def get_true_positives(self):
            mask = (self.y_test == self.y_pred) & (self.y_test == "good")
            true_positives = self.X_test[mask].copy()
            true_positives["Actual Label"] = self.y_test[mask]
            true_positives["Predicted Label"] = self.y_pred[mask]
            true_positives["quality"] = self.df.loc[true_positives.index, "quality"]
            true_positives["Wine #"] = "Wine " + self.df.loc[true_positives.index, "Excel_Row"].astype(str)
            return true_positives.sort_values(by="quality", ascending=False).reset_index(drop=True)

        def get_explanation_text(self):
            return (
                "Показаните вина са така наречените 'Истински положителни' (True Positives), което означава, че:\n"
                " - В действителност са етикетирани като 'добри' (качество = 7) или 'премиум' (качество ≥ 8)\n"
                " - И моделът ги е класифицирал правилно като такива.\n\n"
                "Критериите, по които те са били класифицирани като добри или премиум, включват:\n"
                " - Високо съдържание на алкохол (обикновено ≥ 10)\n"
                " - Сулфати около или над 0.6\n"
                " - Балансирана киселинност и pH\n\n"
                "Тези вина са най-надеждни за предлагане в магазините на Kaufland."
            )

        def get_feature_importance_data(self):
            return pd.DataFrame({
                'Feature': self.X_train.columns,
                'Importance': self.clf.feature_importances_
            }).sort_values(by='Importance', ascending=False)
