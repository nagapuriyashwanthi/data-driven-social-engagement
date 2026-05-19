import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- STEP 1: Load Comments ---
print("Loading comments...")
df = pd.read_csv("comments_data.csv")
print(f"Total comments loaded: {len(df)}")

# --- STEP 2: Clean Comments ---
print("Cleaning comments...")
df["comment"] = df["comment"].astype(str)  # make sure all are strings
df["comment"] = df["comment"].str.replace(r'[^\x00-\x7F]+', ' ', regex=True)  # remove emojis
df["comment"] = df["comment"].str.strip()  # remove extra spaces
df = df[df["comment"].str.len() > 2]  # remove very short comments
print(f"Comments after cleaning: {len(df)}")

# --- STEP 3: Analyze Sentiment ---
print("Analyzing sentiment...")

def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    score = analysis.sentiment.polarity
    
    if score > 0.1:
        return "Relatable", score
    elif score < -0.1:
        return "Not Relatable", score
    else:
        return "Neutral", score

# Apply to all comments
df["label"], df["score"] = zip(*df["comment"].apply(analyze_sentiment))

print("✅ Sentiment analysis complete!")

# --- STEP 4: Show Results ---
print("\n--- RESULTS ---")
print(df[["comment", "label", "score"]].head(10))

print("\n--- SUMMARY ---")
print(df["label"].value_counts())

# --- STEP 5: Save Results ---
df.to_csv("sentiment_results.csv", index=False)
print("\n✅ Results saved to sentiment_results.csv")

# --- STEP 6: Visualize Results ---
print("Creating chart...")
label_counts = df["label"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(
    label_counts.index,
    label_counts.values,
    color=["green", "gray", "red"]
)
plt.title("Comment Sentiment Analysis")
plt.xlabel("Sentiment Label")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.savefig("sentiment_chart.png")
plt.show()
print("✅ Chart saved as sentiment_chart.png")

input("Press Enter to close...")