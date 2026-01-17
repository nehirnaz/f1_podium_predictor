import os
import kaggle

# Set the dataset path
dataset_name = "vshreekamalesh/comprehensive-formula-1-dataset-2020-2025"
download_dir = "data"

# Create data directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

print(f"🚀 Downloading dataset: {dataset_name}...")
try:
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset_name, path=download_dir, unzip=True)
    print(" Download complete! Files in 'data':")
    print(os.listdir(download_dir))
except Exception as e:
    print("\n Error: Authentication failed or API key missing.")
    print("1. Go to https://www.kaggle.com/settings")
    print("2. Scroll to 'API' -> click 'Create New Token'")
    print("3. Move the downloaded 'kaggle.json' file to this folder: C:\\Users\\nehir\\.kaggle\\")
    print(f"   (Or on Mac/Linux: ~/.kaggle/)")
    print(f"\nTechnical error: {e}")
