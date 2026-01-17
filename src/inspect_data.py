import pandas as pd
import os

# Define the path
csv_path = "data/f1_merged_data.csv"

# Check if file exists
if os.path.exists(csv_path):
    print(f"Found file at {csv_path}")
    try:
        df = pd.read_csv(csv_path)
        print("\n--- DATASET INFO ---")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        print("\n--- COLUMN NAMES ---")
        print(list(df.columns))
        
        print("\n--- FIRST ROW EXAMPLE ---")
        print(df.iloc[0])
    except Exception as e:
        print(f"Error reading CSV: {e}")
else:
    print(f"File not found at: {csv_path}")
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir())
    if os.path.exists("data"):
        print("Files in 'data' folder:", os.listdir("data"))