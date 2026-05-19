from googleapiclient.discovery import build
import pandas as pd

# --- YOUR DETAILS ---
API_KEY = "AIzaSyDIiqUTv6m5H3LfMJThR3u2VAzq-we_VL4"
CHANNEL_ID = "UCRVUfAMnsx7gFlpB_ujiTOg"

# --- CONNECT TO YOUTUBE ---
youtube = build("youtube", "v3", developerKey=API_KEY)

# --- GET VIDEO IDs WITH PAGINATION ---
print("Fetching video list...")
video_ids = []
next_page_token = None

while True:
    request = youtube.search().list(
        part="id,snippet",
        channelId=CHANNEL_ID,
        maxResults=50,
        type="video",
        order="date",
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response["items"]:
        video_ids.append(item["id"]["videoId"])

    print(f"Collected so far: {len(video_ids)} videos")

    next_page_token = response.get("nextPageToken")

    # Stop at 500 or no more pages
    if not next_page_token or len(video_ids) >= 500:
        break

print(f"Total video IDs collected: {len(video_ids)}")

# --- GET STATS IN BATCHES OF 50 ---
print("Fetching video stats...")
rows = []

for i in range(0, len(video_ids), 50):
    batch = video_ids[i:i+50]

    stats_response = youtube.videos().list(
        part="statistics,contentDetails,snippet",
        id=",".join(batch)
    ).execute()

    for item in stats_response["items"]:
        s = item["statistics"]
        rows.append({
            "video_id":  item["id"],
            "title":     item["snippet"]["title"],
            "published": item["snippet"]["publishedAt"],
            "views":     s.get("viewCount", 0),
            "likes":     s.get("likeCount", 0),
            "comments":  s.get("commentCount", 0),
            "duration":  item["contentDetails"]["duration"]
        })

    print(f"Stats fetched for {len(rows)} videos so far...")

# --- CLEAN & SAVE ---
df = pd.DataFrame(rows)

for col in ["views", "likes", "comments"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

df.to_csv("youtube_data.csv", index=False)
print(f"✅ Done! {len(df)} videos saved to youtube_data.csv")
print(df.head())

input("Press Enter to close...")