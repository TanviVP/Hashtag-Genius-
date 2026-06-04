# Hashtag Genius 🏷️

An NLP-powered hashtag recommendation system that generates relevant, context-aware hashtags from user-provided text — combining classical NLP techniques with a live Streamlit interface.

🔗 **Live Demo**: [hashtag-genuis.streamlit.app](https://hashtag-genuis.streamlit.app/#hash-tag-genius)

---

## Overview

Hashtag Genius helps content creators, marketers, and social media users generate meaningful hashtags instantly. The system analyzes input text using TF-IDF vectorization and cosine similarity to surface the most relevant hashtags from a trained corpus, eliminating the guesswork from content tagging.

---

## Features

- **NLP-based recommendation** — uses TF-IDF vectorization and cosine similarity to match input text with contextually relevant hashtags
- **TweetEval dataset** — trained on a real-world Twitter benchmark dataset for authentic, social-media-native suggestions
- **Real-time interface** — interactive Streamlit web app with instant hashtag generation
- **Clean UI** — simple input-output design optimized for quick usage

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| NLP | TF-IDF, Cosine Similarity (scikit-learn) |
| Dataset | TweetEval (HuggingFace / tweet_eval) |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## How It Works

1. User enters a text input (caption, topic, or description)
2. The input is vectorized using TF-IDF
3. Cosine similarity is computed against the TweetEval corpus
4. Top-matching hashtags are returned ranked by relevance

---

## Project Structure

```
Hashtag-Genius/
├── Hashtag_recommender/     # Core NLP logic
├── app.py                   # Flask app (alternate backend)
├── streamlit_app.py         # Main Streamlit application
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version specification
├── Procfile                 # Heroku deployment config
└── vercel.json              # Vercel deployment config
```

---

## Getting Started

### Prerequisites
```
Python 3.8+
```

### Installation

```bash
git clone https://github.com/TanviVP/Hashtag-Genius-.git
cd Hashtag-Genius-
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## Dataset

This project uses the **TweetEval** benchmark dataset — a unified evaluation framework for tweet classification tasks. It provides a diverse, real-world corpus of tweet text that improves the relevance of hashtag recommendations compared to synthetic datasets.

---

## Future Enhancements

- [ ] Integrate an LLM API (Gemini / GPT) for generative hashtag suggestions
- [ ] Add platform-specific recommendations (Instagram vs LinkedIn vs Twitter)
- [ ] Support multi-language input
- [ ] Add hashtag popularity/trending score

---

## Author

**Tanvi Pakhale**
[LinkedIn](https://www.linkedin.com/in/) • [GitHub](https://github.com/TanviVP)

---

## License

This project is open source and available under the [MIT License](LICENSE).
