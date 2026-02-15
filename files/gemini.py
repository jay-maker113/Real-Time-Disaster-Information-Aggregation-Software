import os
from dotenv import load_dotenv
from google import genai

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -------------------------------------------------
# Initialize Gemini client (NEW SDK)
# -------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------------------------------
# Analyze News Articles
# -------------------------------------------------
def analyze_articles_with_gemini(articles):
    """
    Uses Gemini to extract structured insights from news articles.
    Returns a concise summary or a safe fallback on failure.
    """
    if not articles:
        return "No relevant articles available for analysis."

    try:
        prompt = (
            "Analyze the following news articles related to a disaster.\n"
            "Extract key facts, trends, severity indicators, and actionable insights.\n"
            "Respond using clear bullet points.\n\n"
        )

        for article in articles:
            prompt += (
                f"Title: {article.get('title', 'N/A')}\n"
                f"Source: {article.get('source', 'Unknown')}\n"
                f"Published: {article.get('published', 'Unknown')}\n\n"
            )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text if response and response.text else "No insights generated."

    except Exception as e:
        print(f"[Gemini][Articles] Failed: {e}")
        return "AI analysis failed for news articles."

# -------------------------------------------------
# Analyze Social Media Posts
# -------------------------------------------------
def analyze_posts_with_ai(posts):
    """
    Uses Gemini to summarize social/media posts related to disasters.
    """
    if not posts:
        return "No social media signals available."

    try:
        prompt = (
            "Analyze the following social media posts related to a disaster.\n"
            "Identify public sentiment, urgent warnings, and emerging patterns.\n"
            "Respond using concise bullet points.\n\n"
        )

        for post in posts:
            prompt += f"Post: {post.get('text', '')}\n\n"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text if response and response.text else "No insights generated."

    except Exception as e:
        print(f"[Gemini][Posts] Failed: {e}")
        return "AI analysis failed for social posts."
