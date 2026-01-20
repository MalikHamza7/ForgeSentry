import sys
import os
import subprocess
import time

# Define paths
Project_Root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Log_Extractor = os.path.join(Project_Root, "data_processing", "log_extractor.py")
Trainer = os.path.join(Project_Root, "ai_engine", "train_model.py")
Data_File = os.path.join(Project_Root, "data_processing", "extracted_logs.csv")
Model_File = os.path.join(Project_Root, "ai_engine", "model.pkl")

def run_pipeline():
    print("🚀 Starting Real-World Feedback Loop...")

    # Step 1: Extract real logs from Elasticsearch
    print("\n[Step 1] Extracting logs from Honeypots...")
    try:
        # Assuming ES is up, we try to fetch. If not, we might fail, but this is the "Real" loop.
        # Adding --source es to arguments
        subprocess.run(["python", Log_Extractor, "--source", "es", "--output", Data_File], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Extraction failed. Ensure Elasticsearch is running.")
        return

    # Step 2: Retrain Model
    print("\n[Step 2] Retraining AI Model with new data...")
    if os.path.exists(Data_File):
        try:
            subprocess.run(["python", Trainer, "--input", Data_File, "--output", Model_File], check=True)
            print("✅ Model successfully retrained and updated!")
        except subprocess.CalledProcessError:
            print("❌ Training failed.")
    else:
        print("⚠️  No data found to train on.")

if __name__ == "__main__":
    run_pipeline()
