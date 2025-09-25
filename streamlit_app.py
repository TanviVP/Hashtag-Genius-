import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# Download stopwords
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download("stopwords")

stop_words = set(stopwords.words('english'))

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

# Streamlit UI
st.set_page_config(page_title="HashTag Genius", page_icon="#️⃣")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.main-header {
    text-align: center;
    color: white;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.9);
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.hashtag {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    color: white;
    padding: 10px 18px;
    margin: 6px;
    border-radius: 25px;
    font-weight: bold;
    border: 1px solid rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">#️⃣ HashTag Genius</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate perfect hashtags for your content using AI</p>', unsafe_allow_html=True)

user_input = st.text_input("Enter your topic, sentence, or content idea:", placeholder="Love is Pain, Study for JEE-MAINS")

if st.button("🪄 Generate Hashtags", type="primary"):
    if user_input:
        with st.spinner("Generating hashtags..."):
            hashtags = generate_fallback_hashtags(user_input)
            
        st.success("✅ Recommended Hashtags:")
        
        hashtag_html = ""
        for hashtag in hashtags:
            hashtag_html += f'<span class="hashtag">{hashtag}</span>'
        
        st.markdown(hashtag_html, unsafe_allow_html=True)
        
        # Copy all hashtags
        all_hashtags = " ".join(hashtags)
        st.code(all_hashtags)
        st.caption("👆 Click to copy all hashtags")
    else:
        st.error("Please enter some text to generate hashtags!")

st.markdown("---")
st.markdown("Built with ❤️ by Tanvi")