import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pickle
import os

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../models/crop_yield.csv")

df = pd.read_csv(DATA_PATH)

# Preprocessing: One-Hot Encoding Categorical Variables
df = pd.get_dummies(df, columns=['Crop', 'State', 'Season'])

# Split into Features & Target
X = df.drop(columns=['Yield'])
y = df['Yield']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6)
model.fit(X_train, y_train)

# Save Model
MODEL_PATH = os.path.join(BASE_DIR, "../models/yield_model.pkl")
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained & saved successfully!")
