import streamlit as st
import tweepy
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Twitter client (optional)
client = None
if tweepy and BEARER_TOKEN != "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N":
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
    except Exception as e:
        st.warning(f"Failed to initialize Twitter client: {e}")


# Ensure required NLTK data is downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words('english'))

# --- Twitter API Setup ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- Preprocessing function ---
def preprocess(text):
    words = text.lower().split()
    return " ".join([word for word in words if word.isalpha() and word not in stop_words])

# --- Fetch Tweets (Cached) ---
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


# --- Hashtag Recommender ---
def recommend_hashtags(user_input, tweet_data, top_k=3):
    processed_input = preprocess(user_input)
    documents = [preprocess(tweet["text"]) for tweet in tweet_data]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    input_vec = vectorizer.transform([processed_input])

    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]

    recommended = set()
    for idx in top_indices:
        recommended.update(tweet_data[idx]["hashtags"])

    return list(recommended)

# --- Streamlit UI ---
st.set_page_config(page_title="Hashtag Recommender", layout="centered")

st.title("📲 Twitter-Based Hashtag Recommendation")
st.write("Enter a sentence or topic to get real-time hashtag suggestions from Twitter:")

user_input = st.text_input("📝 Your sentence or topic:", "")

if st.button("Generate Hashtags"):
    if user_input.strip() == "":
        st.warning("Please enter a valid sentence or topic.")
    else:
        with st.spinner("🔍 Fetching tweets and generating hashtags..."):
            tweets = fetch_tweets_with_hashtags(user_input)
            if not tweets:
                st.error("No relevant tweets found or you've hit the rate limit.")
            else:
                tags = recommend_hashtags(user_input, tweets)
                if tags:
                    st.success("✅ Recommended Hashtags:")
                    st.write(" ".join(tags))
                else:
                    st.info("No matching hashtags found. Try a different sentence.")
