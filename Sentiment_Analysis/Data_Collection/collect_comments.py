from googleapiclient.discovery import build
import pandas as pd

# --- YOUR DETAILS ---
API_KEY = "AIzaSyDIiqUTv6m5H3LfMJThR3u2VAzq-we_VL4"

# --- CONNECT TO YOUTUBE ---
youtube = build("youtube", "v3", developerKey=API_KEY)

# --- READ VIDEO IDs FROM YOUR CSV ---
print("Reading video IDs from youtube_data.csv...")
df_videos = pd.read_csv("youtube_data.csv")
video_ids = df_videos["video_id"].tolist()
print(f"Found {len(video_ids)} videos")

# --- COLLECT COMMENTS FOR EACH VIDEO ---
all_comments = []

for i, video_id in enumerate(video_ids):
    print(f"Fetching comments for video {i+1}/{len(video_ids)}...")
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            order="relevance"
        )
        response = request.execute()

        for item in response["items"]:
            c = item["snippet"]["topLevelComment"]["snippet"]
            all_comments.append({
                "video_id": video_id,
                "comment":  c["textDisplay"],
                "likes":    c["likeCount"],
                "date":     c["publishedAt"]
            })

    except Exception as e:
        print(f"⚠️ Skipping video {video_id} — {e}")
        continue

# --- SAVE TO CSV ---
df_comments = pd.DataFrame(all_comments)
df_comments.to_csv("comments_data.csv", index=False)
print(f"✅ Done! {len(all_comments)} comments saved to comments_data.csv")
print(df_comments.head())

input("Press Enter to close...")