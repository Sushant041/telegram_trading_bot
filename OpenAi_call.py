import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

client = Groq(
    # This is the default and can be omitted
    api_key = os.getenv("GROQ_API_KEY")
)

# Read the CSV file with tweets
def load_tweets(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df['Text'].tolist()  # Assuming 'tweet' column holds the tweet text

# Send tweets to OpenAI for analysis
def analyze_tweets_with_openai(tweets):
    responses = []
    for tweet in tweets:
        # Construct the prompt to send to OpenAI
        prompt = f"""Analyze this tweet:
        {tweet}

        ### Step-by-Step Analysis:
        1. **Identified Cryptocurrency:** Determine which cryptocurrency is mentioned in the tweet (e.g., $XRP, $BTC).
        2. **Market Sentiment:** Assess whether the sentiment in the tweet is bullish, bearish, or neutral.
        3. **Buy/Sell Signal:** Check if the tweet suggests a potential trading action.
        4. **Final Decision:** Based on the sentiment and signal, conclude whether the recommended action is to buy, sell, or stay neutral.

        ### Final Output Format: 
        - **Decision:** `"buy token"`, `"sell token"`, or `"neutral"` (strict format). where `token` is the cryptocurrency symbol.

        ### Example Output:
        **Decision:** `buy $BTC`  
        """

        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            # print(response.choices[0].message.content.strip())
            analysis = response.choices[0].message.content.strip()
            responses.append((tweet, analysis))
        except Exception as e:
            responses.append((tweet, f"Error: {str(e)}"))
    
    return responses

# Output the analysis results
def output_results(results):
    for tweet, analysis in results:
        print(f"Tweet: {tweet}")
        print(f"Analysis: {analysis}\n")
        print("--------------------------------END----------------------------------\n")
    
# Full process
def OpenAi_call():
    # Provide your CSV path
    csv_file_path = "crypto_tweets.csv"
    
    # Load tweets from CSV
    tweets = load_tweets(csv_file_path)

    # Analyze tweets using OpenAI
    results = analyze_tweets_with_openai(tweets)
    
    # Output results
    # output_results(results)
    return results