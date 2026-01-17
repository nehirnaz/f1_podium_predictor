import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import OneHotEncoder 
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import classification_report, accuracy_score 

# 1. Load the merged data
DATA_PATH = "data/f1_merged_data.csv"
print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH)

# 2. Define the Target
df["podium"] = (df["finish_position"] <= 3).astype(int)

print(f"Dataset shape: {df.shape}")
print(f"Podium distribution:\n{df['podium'].value_counts(normalize=True)}")

# 3. Define Features
numeric_features = ["grid_position", "year"]
categorical_features = ["driver", "team", "gp_name"]

features = numeric_features + categorical_features

# 4. Split Data (Train on older races, Test on newer races)
X = df[features]
y = df["podium"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Build Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ]
)

# 6. Train
print("\nTraining model...")
model.fit(X_train, y_train)

# 7. Evaluate
print("Evaluating...")
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Test Prediction
print("\n--- TEST PREDICTION ---")
test_driver = pd.DataFrame({
    "grid_position": [1],
    "year": [2025],
    "driver": ["max_verstappen"],
    "team": ["red_bull"],
    "gp_name": ["Monaco Grand Prix"]
})

prob = model.predict_proba(test_driver)[0][1]
print(f"Probability of Verstappen (P1, Red Bull) getting a podium: {prob:.1%}")