import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import argparse
import os

def train_model(data_path, model_path='model.pkl'):
    if not os.path.exists(data_path):
        print(f"Error: Data file {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    # Check required columns
    if 'input' not in df.columns or 'label' not in df.columns:
        print("Error: CSV must contain 'input' and 'label' columns.")
        return

    # Handle missing values
    df['input'] = df['input'].fillna('')

    X = df['input']
    y = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create pipeline: TF-IDF Vectorizer -> Random Forest
    pipeline = make_pipeline(
        TfidfVectorizer(max_features=1000),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )

    print("Training model...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train AI Threat Classifier")
    parser.add_argument('--input', type=str, required=True, help="Path to training CSV")
    parser.add_argument('--output', type=str, default='model.pkl', help="Path to save model")
    
    args = parser.parse_args()
    
    train_model(args.input, args.output)
