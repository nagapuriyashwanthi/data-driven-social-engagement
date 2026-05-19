import pandas as pd
import matplotlib.pyplot as plt

# --- STEP 1: Load Video Data ---
print("Loading video data...")
df = pd.read_csv("youtube_data.csv")
print(f"Total videos loaded: {len(df)}")

# --- STEP 2: Convert Numbers ---
for col in ["views", "likes", "comments"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# --- STEP 3: Calculate Viral Coefficient ---
print("Calculating viral scores...")

def viral_coefficient(views, likes, comments):
    score = (views * 1) + (likes * 2) + (comments * 3)
    return round(score, 2)

df["viral_score"] = df.apply(
    lambda row: viral_coefficient(
        row["views"],
        row["likes"],
        row["comments"]
    ), axis=1
)

# --- STEP 4: Rank Videos ---
df = df.sort_values("viral_score", ascending=False)
df["rank"] = range(1, len(df) + 1)

# --- STEP 5: Label Viral Potential ---
def viral_label(score):
    if score >= df["viral_score"].quantile(0.75):
        return "🔥 High Potential"
    elif score >= df["viral_score"].quantile(0.50):
        return "⚡ Medium Potential"
    else:
        return "❄️ Low Potential"

df["potential"] = df["viral_score"].apply(viral_label)

# --- STEP 6: Show Results ---
print("\n--- TOP 10 VIRAL VIDEOS ---")
print(df[["rank", "title", "views", "likes", "comments", "viral_score", "potential"]].head(10).to_string())

print("\n--- SUMMARY ---")
print(df["potential"].value_counts())

# --- STEP 7: Save Results ---
df.to_csv("viral_scores.csv", index=False)
print("\n✅ Results saved to viral_scores.csv")

# --- STEP 8: Visualize Top 10 ---
print("Creating chart...")
top10 = df.head(10)

plt.figure(figsize=(12, 6))
plt.barh(
    top10["title"].str[:30],  # first 30 chars of title
    top10["viral_score"],
    color="orange"
)
plt.xlabel("Viral Score")
plt.title("Top 10 Most Viral Videos")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("viral_chart.png")
plt.show()
print("✅ Chart saved as viral_chart.png")

input("Press Enter to close...")