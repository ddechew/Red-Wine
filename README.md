# 🍷 Wine Quality Prediction App (Kaufland Data Academy)

This is a Python-based desktop application built during Kaufland’s Data Academy in collaboration with the University of National and World Economy (UNWE). The goal of the project was to solve a real business case:  
**“How can we help Kaufland choose higher-quality red wine for their stores?”**

## 📌 Overview

The application leverages **machine learning models** to predict the quality of red wine samples based on physicochemical characteristics. It includes features for data visualization, prediction, and model analysis — all wrapped in an intuitive PyQt5 interface.

## 👨‍💻 Technologies Used

- Python 3
- Pandas & NumPy
- Scikit-learn (RandomForestRegressor, DecisionTreeClassifier)
- Matplotlib & Seaborn
- PyQt5 (Desktop GUI)

## 🚀 Features

- 📂 Import red wine dataset (CSV)
- 📊 Data inspection and visualization
- 📈 Train & analyze ML models (classification + regression)
- 🧠 Predict wine quality using AI
- ✅ Identify top-quality wines (true positives)
- 🌳 Visualize decision tree logic
- 📃 Export results and explanations

## 📦 Dataset

- 1,599 samples of red wine
- 11 physicochemical attributes
- Quality ratings (0–10) from professional sommeliers

Source: [UCI Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)

## 🔍 Models Used

- **Random Forest Regressor**  
  Trained to predict numeric wine quality scores and identify the most important features.
  
- **Decision Tree Classifier**  
  Used to classify wines as "Good" or "Not Good" based on quality threshold and to visualize decision paths.
