from flask import Flask, render_template, request, jsonify
import tweepy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import os

app = Flask(__name__)

# Download stopwords if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download("stopwords")

# Twitter API Setup
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH31xAEAAAAAMGqB%2Fx97f9IWzvPftTVLZ0RuSSM%3DIUzZ4itRGRONT9BfgXzSS6GVvC6t6jmg4KDoUnxhYchLcnUN3N"
client = tweepy.Client(bearer_token=BEARER_TOKEN)
stop_words = set(stopwords.words('english'))

def preprocess(text):
    words = text.lower().split()
    return " ".join([word for word in words if word.isalpha() and word not in stop_words])

def fetch_tweets_with_hashtags(keyword, max_results=50):
    try:
        if not keyword.strip():
            return []
        query = f'"{keyword}" has:hashtags -is:retweet lang:en'
        response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["text"])
        
        if not response or not response.data:
            return []
            
        tweets = []
        for tweet in response.data:
            hashtags = [word for word in tweet.text.split() if word.startswith("#")]
            if hashtags:
                tweets.append({
                    "text": tweet.text,
                    "hashtags": hashtags
                })
        return tweets
    except Exception:
        return []

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

def generate_fallback_hashtags(user_input):
    if not user_input.strip():
        return ["#Trending", "#Popular", "#Daily"]
        
    words = user_input.lower().replace(",", " ").replace("-", " ").split()
    hashtags = []
    
    for word in words:
        if word.isalpha() and len(word) > 2 and word not in stop_words:
            hashtags.append(f"#{word.capitalize()}")
    
    text_lower = user_input.lower()
    if any(word in text_lower for word in ["love", "pain", "heart", "emotion"]):
        hashtags.extend(["#Love", "#Life", "#Feelings", "#Emotions"])
    if any(word in text_lower for word in ["study", "jee", "exam", "mains", "education"]):
        hashtags.extend(["#Study", "#JEE", "#Education", "#StudentLife", "#Exam"])
    if any(word in text_lower for word in ["motivation", "inspire", "success"]):
        hashtags.extend(["#Motivation", "#Success", "#Goals"])
    
    return list(set(hashtags))[:8]

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    user_input = data.get('text', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Please enter some text'})
    
    # Try to fetch tweets
    tweets = fetch_tweets_with_hashtags(user_input, max_results=50)
    
    if tweets:
        hashtags = recommend_hashtags(user_input, tweets)
        source = "Twitter API"
    else:
        hashtags = generate_fallback_hashtags(user_input)
        source = "AI Generated"
    
    return jsonify({
        'hashtags': hashtags,
        'source': source,
        'count': len(hashtags)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)