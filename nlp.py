import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import re
import string
import joblib

# Load and preprocess data
def load_data(data_path):
    df = pd.read_csv(data_path)
    print(df.columns)  # Check the column names
    X = df['message']  # Adjust based on the actual column name for messages
    y = df.drop(['id', 'message', 'original', 'genre'], axis=1)
    return X, y

data_path = './Disaster-Response/data/disaster_categories.csv'
X, y = load_data(data_path)

# Clean the text data
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\[.*?\]', '', text)  # Remove text in square brackets
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation
    text = re.sub(r'\w*\d\w*', '', text)  # Remove words containing numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove excess whitespace
    return text

# Vectorize text data and build a pipeline
def build_pipeline():
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    return pipeline

# Hyperparameter tuning
def tune_model(pipeline, X_train, y_train):
    param_grid = {
        'clf__estimator__n_estimators': [100, 200],
        'clf__estimator__max_depth': [None, 10, 20],
        'clf__estimator__min_samples_split': [2, 5],
    }
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, verbose=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    for i, col in enumerate(y_test.columns):
        print(f"Classification report for {col}:")
        print(classification_report(y_test[col], y_pred[:, i]))

    accuracy = (y_pred == y_test).mean().mean()
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
def save_model(model, filename="disaster_model.pkl"):
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

if __name__ == "__main__":
    data_path = './Disaster-Response/data/disaster_categories.csv'  # Filepath to your dataset

    # Load and clean data
    X, y = load_data(data_path)
    X_cleaned = X.apply(clean_text)  # Apply text cleaning

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_cleaned, y, test_size=0.2, random_state=42)

    # Build pipeline and tune model
    pipeline = build_pipeline()
    model = tune_model(pipeline, X_train, y_train)

    # Evaluate the tuned model
    evaluate_model(model, X_test, y_test)

    # Save the model
    save_model(model)
