# Crypto Sentiment Analysis API

This project is a Flask-based API that fetches cryptocurrency-related tweets, analyzes their sentiment using Groq AI, and returns a recommendation to **buy**, **sell**, or stay **neutral** based on the tweets.

## Features 🚀
- Fetches real-time tweets using **twikit**
- Performs **sentiment analysis** using Groq AI
- Provides a recommendation: `buy $TOKEN`, `sell $TOKEN`, or `neutral`
- Supports **custom search queries** for tweets
- Deployable on **Render** for free hosting
- Integrated with **Telegram bot** (optional)

---

## Installation 🛠️

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/crypto-sentiment-api.git
cd crypto-sentiment-api
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a **.env** file in the project root and add:
```
TWITTER_USERNAME=your_username
TWITTER_EMAIL=your_email
TWITTER_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
```

> **Note:** Keep your `.env` file secret and never commit it to GitHub.

---

## Usage 🏃‍♂️

### Run the Flask API Locally
```sh
python app.py
```

### Test with Postman or cURL
#### Default Crypto Query:
```sh
curl -X POST "http://127.0.0.1:5000/fetch-tweets"
```
#### Custom Query:
```sh
curl -X POST "http://127.0.0.1:5000/fetch-tweets" -H "Content-Type: application/json" -d '{"query": "Solana OR Cardano"}'
```

**Response Example:**
```json
{
  "message": "Tweet collection and sentiment analysis completed!",
  "status": "success",
  "tweets": [
    {
      "tweet": "Bitcoin is breaking out! 🚀",
      "analysis": "Bullish sentiment detected. Decision: buy $BTC"
    },
    {
      "tweet": "Ethereum is looking weak. Might drop soon!",
      "analysis": "Bearish sentiment detected. Decision: sell $ETH"
    }
  ]
}
```

---

## Deploying to Render 🌍

### 1️⃣ Create a `requirements.txt` file
```sh
pip freeze > requirements.txt
```

### 2️⃣ Create a `render.yaml` file (optional for auto-deployment)
```yaml
services:
  - type: web
    name: crypto-sentiment-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn -w 4 -b 0.0.0.0:5000 app:app"
```

### 3️⃣ Push to GitHub
```sh
git add .
git commit -m "Initial commit"
git push origin main
```

### 4️⃣ Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New Web Service**
3. Connect your GitHub repo
4. Set the **Environment Variables**
5. Click **Deploy** 🎉

---

## Contributing 🤝
Feel free to submit a **pull request** or open an **issue** to improve this project!

---

## License 📜
This project is open-source under the **MIT License**.

