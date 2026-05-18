import pandas as pd
import numpy as np
import joblib
from sklearn.neighbors import KNeighborsClassifier

def main():
    # Step 1: Create DataFrame
    data = {
        "annual_income": [15, 16, 17, 25, 30, 35, 50, 55, 60],
        "spending_score": [39, 81, 6, 40, 60, 20, 50, 65, 10]
    }
    df = pd.DataFrame(data)

    # Create simple labels (low/medium/high income groups)
    conditions = [
        df["annual_income"] < 30,
        df["annual_income"].between(30, 50),
        df["annual_income"] > 50
    ]
    choices = [0, 1, 2]
    df["label"] = np.select(conditions, choices, default=1)

    print("Training Data:")
    print(df)

    # Step 2: Select features (X) and labels (y)
    X = df[["annual_income", "spending_score"]]
    y = df["label"]

    # Step 3: Train KNN model
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)

    # Step 4: Save model
    joblib.dump(model, "knn_model.pkl")
    print("KNN model saved as knn_model.pkl")

if __name__ == "__main__":
    main()