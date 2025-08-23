#!/usr/bin/env python
# coding: utf-8

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd

def run_forest(df, target_column):

    forest = RandomForestClassifier(n_estimators=100, random_state=3)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
    forest.fit(X_train, y_train)
    
    # Store feature names for validation
    forest.feature_names_in_ = X.columns.tolist()
    
    importance = pd.Series(forest.feature_importances_, index=X.columns)
    with open('output.txt', 'a') as f:
        f.write("Feature Importances:\n")
        f.write(str(importance.sort_values(ascending=False)) + "\n")
    
    accuracy = forest.score(X_test, y_test)
    prob = forest.predict_proba(X_test)
    with open('output.txt', 'a') as f:
        f.write(f"Accuracy: {accuracy}\n")
        f.write(f"First 10 Predictions (probabilities):\n{prob[:10]}\n")
    
    scores = cross_val_score(forest, X, y, cv=5, scoring='accuracy')
    with open('output.txt', 'a') as f:
        f.write(f"CV Accuracy: {scores.mean()} (+/- {scores.std()})\n")
        f.write("\n")
    
    return forest

def plot_shap_summary(model, X, output_file='shap_summary.png', max_samples=50):    
    X_sampled = shap.sample(X, max_samples, random_state=3) if X.shape[0] > max_samples else X
    print("Sampled X shape for SHAP computation:", X_sampled.shape)
    if isinstance(model, RandomForestClassifier):
        shap_explain = shap.KernelExplainer(model.predict_proba, X_sampled)
        shap_values = shap_explain.shap_values(X_sampled)
        print("KernelExplainer SHAP values shape (classifier, all classes):", [v.shape for v in shap_values])
        shap.summary_plot(shap_values[1], X_sampled, show=False)
    elif isinstance(model, RandomForestRegressor):
        shap_explain = shap.KernelExplainer(model.predict, X_sampled)
        shap_values = shap_explain.shap_values(X_sampled)
        print("KernelExplainer SHAP values shape (regressor):", shap_values.shape)
        shap.summary_plot(shap_values, X_sampled, show=False)
    
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()
    with open('output.txt', 'a') as f:
        f.write(f"SHAP summary plot saved as {output_file}\n\n")

def run_forest_regressor(df, target_column):
    forest = RandomForestRegressor(n_estimators=100, random_state=3)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)

    forest.fit(X_train, y_train)
    
    importance = pd.Series(forest.feature_importances_, index=df.drop(target_column, axis=1).columns)
    with open('output.txt', 'a') as f:
        f.write("Feature Importances:\n")
        f.write(str(importance.sort_values(ascending=False)) + "\n")
    
    prob = forest.predict(X_test)
    mse = mean_squared_error(y_test, prob)
    with open('output.txt', 'a') as f:
        f.write(f"Mean Squared Error: {mse}\n")
        f.write("\n")
        f.write(f"First 10 Predictions:\n{prob[:10]}\n")

    return forest

intensity = {'Low': 0, 'Medium': 1, 'High': 2}
quality = {'Poor': 0, 'Average': 1, 'Good': 2}
answer = {'No': 0, 'Yes': 1}

def one_hot(df, target_columns, sep='_'):
    missing_cols = [col for col in target_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} not found in DataFrame")
    df = pd.get_dummies(df, columns=target_columns, prefix=None, prefix_sep=sep, drop_first=False, dtype=int)
    return df