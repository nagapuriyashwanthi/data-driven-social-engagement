import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# --- STEP 1: Load Data ---
print("Loading data...")
df = pd.read_csv("youtube_data.csv")
print(f"Total videos: {len(df)}")

# --- STEP 2: Prepare Data ---
for col in ["views", "comments"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

print(df[["views", "comments"]].head())

# Features — only comments since likes are hidden
X = df[["comments"]]
y = df["views"]

# --- STEP 3: Split Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)
print(f"Training data: {len(X_train)} videos")
print(f"Testing data:  {len(X_test)} videos")

# --- STEP 4: Train Model ---
print("Training model...")
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Model trained!")

# --- STEP 5: Test Model ---
y_pred = model.predict(X_test)

# --- STEP 6: Accuracy ---
mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print("\n--- MODEL ACCURACY ---")
print(f"Mean Absolute Error : {mae:.2f}")
print(f"R2 Score            : {r2:.2f}")
print(f"Model Accuracy      : {r2 * 100:.2f}%")

# --- STEP 7: Predict New Video ---
print("\n--- PREDICT A NEW VIDEO ---")
new_video        = pd.DataFrame({"comments": [100]})
predicted_views  = model.predict(new_video)
print(f"If a video gets 100 comments")
print(f"Predicted Views: {int(predicted_views[0]):,}")

# --- STEP 8: Charts ---
print("\nCreating charts...")

# Chart 1: Actual vs Predicted
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred, color="blue", alpha=0.6)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    color="red",
    linewidth=2
)
plt.xlabel("Actual Views")
plt.ylabel("Predicted Views")
plt.title("Actual vs Predicted Views")
plt.tight_layout()
plt.savefig("actual_vs_predicted.png")
plt.show()

# Chart 2: Comments vs Views
plt.figure(figsize=(8, 5))
plt.scatter(df["comments"], df["views"], color="orange", alpha=0.6)
plt.xlabel("Comments")
plt.ylabel("Views")
plt.title("Comments vs Views")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

# --- STEP 9: Save ---
df["predicted_views"] = model.predict(X)
df.to_csv("prediction_results.csv", index=False)
print("✅ Results saved to prediction_results.csv")

input("Press Enter to close...")