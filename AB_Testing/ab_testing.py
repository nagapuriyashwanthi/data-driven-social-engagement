import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# --- LOAD DATA ---
print("Loading data...")
df = pd.read_csv(r"C:\Users\saikiran\Desktop\youtube-project\Data_Collection\youtube_data.csv")

for col in ["views", "likes", "comments"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

print(f"Total videos: {len(df)}")

# --- A/B TEST 1: SHORT vs LONG VIDEOS ---
print("\n--- A/B TEST 1: Short vs Long Videos ---")

# Convert duration to seconds
def duration_to_seconds(duration):
    duration = duration.replace("PT", "")
    seconds = 0
    if "M" in duration:
        parts = duration.split("M")
        seconds += int(parts[0]) * 60
        duration = parts[1]
    if "S" in duration:
        seconds += int(duration.replace("S", ""))
    return seconds

df["duration_seconds"] = df["duration"].apply(duration_to_seconds)

# Split into short and long
short_videos = df[df["duration_seconds"] <= 60]["views"]
long_videos  = df[df["duration_seconds"] > 60]["views"]

print(f"Short videos (<=60s): {len(short_videos)}")
print(f"Long videos  (>60s):  {len(long_videos)}")
print(f"Short videos avg views: {short_videos.mean():,.0f}")
print(f"Long videos  avg views: {long_videos.mean():,.0f}")

# T-Test
if len(short_videos) > 1 and len(long_videos) > 1:
    t_stat, p_value = stats.ttest_ind(short_videos, long_videos)
    print(f"\nT-Statistic: {t_stat:.4f}")
    print(f"P-Value:     {p_value:.4f}")
    if p_value < 0.05:
        print("✅ Statistically SIGNIFICANT difference!")
        if short_videos.mean() > long_videos.mean():
            print("🏆 Winner: SHORT videos perform better!")
        else:
            print("🏆 Winner: LONG videos perform better!")
    else:
        print("❌ No statistically significant difference")

# --- A/B TEST 2: HIGH vs LOW COMMENTS ---
print("\n--- A/B TEST 2: High vs Low Comments ---")

median_comments = df["comments"].median()
high_comments = df[df["comments"] >= median_comments]["views"]
low_comments  = df[df["comments"] < median_comments]["views"]

print(f"High comment videos avg views: {high_comments.mean():,.0f}")
print(f"Low comment videos  avg views: {low_comments.mean():,.0f}")

if len(high_comments) > 1 and len(low_comments) > 1:
    t_stat2, p_value2 = stats.ttest_ind(high_comments, low_comments)
    print(f"\nT-Statistic: {t_stat2:.4f}")
    print(f"P-Value:     {p_value2:.4f}")
    if p_value2 < 0.05:
        print("✅ Statistically SIGNIFICANT difference!")
        if high_comments.mean() > low_comments.mean():
            print("🏆 Winner: HIGH comment videos perform better!")
        else:
            print("🏆 Winner: LOW comment videos perform better!")
    else:
        print("❌ No statistically significant difference")

# --- CHARTS ---
print("\nCreating charts...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Short vs Long
axes[0].bar(
    ["Short Videos\n(<=60s)", "Long Videos\n(>60s)"],
    [short_videos.mean(), long_videos.mean()],
    color=["royalblue", "orange"]
)
axes[0].set_title("A/B Test 1: Short vs Long Videos")
axes[0].set_ylabel("Average Views")

# Chart 2: High vs Low Comments
axes[1].bar(
    ["High Comments", "Low Comments"],
    [high_comments.mean(), low_comments.mean()],
    color=["green", "red"]
)
axes[1].set_title("A/B Test 2: High vs Low Comments")
axes[1].set_ylabel("Average Views")

plt.tight_layout()
plt.savefig(r"C:\Users\saikiran\Desktop\youtube-project\AB_Testing\ab_testing_chart.png")
plt.show()
print("✅ Chart saved as ab_testing_chart.png")

# --- SAVE RESULTS ---
results = pd.DataFrame({
    "Test": [
        "Short vs Long Videos",
        "High vs Low Comments"
    ],
    "Group A": [
        f"Short: {short_videos.mean():,.0f} views",
        f"High Comments: {high_comments.mean():,.0f} views"
    ],
    "Group B": [
        f"Long: {long_videos.mean():,.0f} views",
        f"Low Comments: {low_comments.mean():,.0f} views"
    ],
    "P-Value": [
        round(p_value, 4),
        round(p_value2, 4)
    ],
    "Significant": [
        "Yes" if p_value < 0.05 else "No",
        "Yes" if p_value2 < 0.05 else "No"
    ]
})

results.to_csv(r"C:\Users\saikiran\Desktop\youtube-project\AB_Testing\ab_testing_results.csv", index=False)
print("✅ Results saved to ab_testing_results.csv")
print("\n--- FINAL RESULTS ---")
print(results.to_string())

input("\nPress Enter to close...")