import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --- PAGE SETTINGS ---
st.set_page_config(
    page_title="Social Engagement Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- TITLE ---
st.title("📊 Data-Driven Social Engagement Dashboard")
st.markdown("**Analyzing YouTube content performance — Shisha Couple Channel**")
st.divider()

# --- LOAD DATA ---
@st.cache_data
def load_data():
    videos     = pd.read_csv(r"C:\Users\saikiran\Desktop\youtube-project\Data_Collection\youtube_data.csv")
    sentiment  = pd.read_csv(r"C:\Users\saikiran\Desktop\youtube-project\Sentiment_Analysis\sentiment_results.csv")
    viral      = pd.read_csv(r"C:\Users\saikiran\Desktop\youtube-project\Viral_Coefficient\viral_scores.csv")
    prediction = pd.read_csv(r"C:\Users\saikiran\Desktop\youtube-project\Prediction_Model\prediction_results.csv")

    for col in ["views", "likes", "comments"]:
        videos[col] = pd.to_numeric(
            videos[col], errors="coerce"
        ).fillna(0).astype(int)

    return videos, sentiment, viral, prediction

videos, sentiment, viral, prediction = load_data()

# --- ROW 1: KEY METRICS ---
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Videos",   len(videos))
col2.metric("Total Views",    f"{videos['views'].sum():,}")
col3.metric("Total Likes",    f"{videos['likes'].sum():,}")
col4.metric("Total Comments", f"{videos['comments'].sum():,}")

st.divider()

# --- ROW 2: TOP VIDEOS TABLE ---
st.subheader("🔥 Top 10 Most Viral Videos")
top10 = viral.head(10)[["title", "views", "likes", "comments", "viral_score", "potential"]]
st.dataframe(top10, use_container_width=True)

st.divider()

# --- ROW 3: CHARTS ---
st.subheader("📊 Performance Charts")
col1, col2 = st.columns(2)

# Chart 1: Top 10 Videos by Views
with col1:
    st.markdown("**Top 10 Videos by Views**")
    top_views = videos.nlargest(10, "views")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        top_views["title"].str[:25],
        top_views["views"],
        color="royalblue"
    )
    ax.invert_yaxis()
    ax.set_xlabel("Views")
    plt.tight_layout()
    st.pyplot(fig)

# Chart 2: Viral Score Distribution
with col2:
    st.markdown("**Viral Score Distribution**")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(
        viral["viral_score"],
        bins=10,
        color="orange",
        edgecolor="black"
    )
    ax2.set_xlabel("Viral Score")
    ax2.set_ylabel("Number of Videos")
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# --- ROW 4: SENTIMENT ANALYSIS ---
st.subheader("💬 Sentiment Analysis Results")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Comment Sentiment Breakdown**")
    sentiment_counts = sentiment["label"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    colors = ["green", "gray", "red"]
    ax3.bar(
        sentiment_counts.index,
        sentiment_counts.values,
        color=colors[:len(sentiment_counts)]
    )
    ax3.set_xlabel("Sentiment")
    ax3.set_ylabel("Number of Comments")
    plt.tight_layout()
    st.pyplot(fig3)

with col2:
    st.markdown("**Sample Comments with Labels**")
    st.dataframe(
        sentiment[["comment", "label", "score"]].head(10),
        use_container_width=True
    )

st.divider()

# --- ROW 5: PREDICTION TOOL ---
st.subheader("🔮 Predict Video Performance")
st.markdown("Move the slider to predict views based on expected comments")

# Train model
X = videos[["comments"]]
y = videos["views"]
model = LinearRegression()
model.fit(X, y)

comments_input = st.slider("Expected Comments", 0, 1000, 100)

if st.button("🔮 Predict Views"):
    input_data = pd.DataFrame({"comments": [comments_input]})
    predicted  = model.predict(input_data)[0]
    st.success(f"📊 Predicted Views: **{int(predicted):,}**")

    if predicted > videos["views"].mean():
        st.info("🔥 This video has HIGH viral potential!")
    else:
        st.warning("📉 This video may need better engagement strategy")

st.divider()

# --- ROW 6: RAW DATA ---
st.subheader("📄 Raw Video Data")
st.dataframe(videos, use_container_width=True)

st.divider()

# --- FOOTER ---
st.markdown("**Built with Python & Streamlit | Data-Driven Social Engagement Initiative | Shisha Couple**")