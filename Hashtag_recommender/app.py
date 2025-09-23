import streamlit as st
import pandas as pd
import nltk
import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔁 For Twitter API (optional)
try:
    import tweepy
except ImportError:
    tweepy = None

# 🔐 Twitter API setup
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N"  # ⬅️ Replace with your actual token if using online mode
client = None
if tweepy and BEARER_TOKEN != "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N":
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
    except Exception as e:
        st.warning(f"Failed to initialize Twitter client: {e}")

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# ------------------ UI ------------------
st.set_page_config(page_title="Hashtag Recommender", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(to right, #fdfbfb, #ebedee); font-family: 'Segoe UI', sans-serif; }
    .hashtag { background-color: #1DA1F2; color: white; padding: 6px 12px; margin: 5px; display: inline-block; border-radius: 25px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 Hashtag Recommender App")
st.subheader("Choose between live Twitter data or offline dataset")

# ------------------ Load Dataset ------------------
@st.cache_data
def load_offline_dataset():
    try:
        df = pd.read_csv("C:\\Users\\Dell\\tweeteval\\datasets\\hashtag\\train.csv")
        df.dropna(subset=["text", "hashtags"], inplace=True)
        df["hashtags"] = df["hashtags"].apply(lambda x: x.split())  # Convert space-separated to list
        return df
    except Exception as e:
        st.error(f"Failed to load offline dataset: {e}")
        return pd.DataFrame()

offline_df = load_offline_dataset()

# ------------------ Hashtag Functions ------------------
def preprocess(text):
    words = text.lower().split()
    return " ".join([word for word in words if word.isalpha() and word not in stop_words])

def recommend_hashtags_from_dataset(user_input, df, top_k=5):
    corpus = df["text"].tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    input_vec = vectorizer.transform([user_input.lower()])
    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]

    recommended = set()
    for i in top_indices:
        recommended.update(df.iloc[i]["hashtags"])
    return list(recommended)

# ------------------ Twitter Setup ------------------
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N"
if tweepy and BEARER_TOKEN != "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N":
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

@st.cache_data(ttl=3600)
@st.cache_data(ttl=3600)
def fetch_tweets_with_hashtags(keyword, max_results=30):
    if client is None:
        st.warning("Twitter API client is not configured. Using offline mode.")
        return []

    query = f"{keyword} has:hashtags -is:retweet lang:en"
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["text"]
        )
        tweets = []
        if response.data:
            for tweet in response.data:
                hashtags = [word for word in tweet.text.split() if word.startswith("#")]
                if hashtags:
                    tweets.append({"text": tweet.text, "hashtags": hashtags})
        return tweets

    except Exception as e:
        st.error(f"⚠️ Twitter API Error: {e}")
        return []

st.warning("Twitter API is not available. Using offline dataset only.")

def recommend_from_twitter(user_input):
    tweets = fetch_tweets_with_hashtags(user_input)
    
    if not tweets:  # Empty or None
        return []

    df_tweets = pd.DataFrame(tweets)

    if "text" not in df_tweets.columns or "hashtags" not in df_tweets.columns:
        return []

    return recommend_hashtags_from_dataset(user_input, df_tweets)


# ------------------ Streamlit UI ------------------
option = st.radio("Select Data Source:", ["💾 Offline Dataset", "🔁 Live Twitter API"])

user_input = st.text_input("💬 Enter a topic or sentence:")
submit = st.button("🚀 Recommend Hashtags")

if submit:
    if not user_input.strip():
        st.warning("Please enter a sentence.")
    else:
        with st.spinner("Processing..."):
            if option == "💾 Offline Dataset":
                tags = recommend_hashtags_from_dataset(user_input, offline_df)
            else:
                tags = recommend_from_twitter(user_input)

        if tags:
            st.success("✅ Recommended Hashtags:")
            for tag in tags:
                st.markdown(f'<span class="hashtag">{tag}</span>', unsafe_allow_html=True)
        else:
            st.info("No hashtags found. Try a different input.")

st.markdown("---")
st.markdown(
    "<center>🔗 Built with Streamlit | Offline + Twitter Support | By Tanvi</center>",
    unsafe_allow_html=True
)
