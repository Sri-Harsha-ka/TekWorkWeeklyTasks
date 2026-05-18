import pandas as pd
import joblib
from sklearn.cluster import KMeans

# Step 1: Create DataFrame
data = {
    "annual_income": [15, 16, 17, 25, 30, 35, 50, 55, 60],
    "spending_score": [39, 81, 6, 40, 60, 20, 50, 65, 10]
}
df = pd.DataFrame(data)

print("Training Data:")
print(df)

# Step 2: Select features (X)
X = df[["annual_income", "spending_score"]]

# Step 3: Train KMeans model
model = KMeans(n_clusters=3, random_state=42)
model.fit(X)

# Step 4: Save model
joblib.dump(model, "model.pkl")
print("✅ KMeans model saved as model.pkl")




