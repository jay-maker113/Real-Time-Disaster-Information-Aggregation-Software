import urllib.parse
import feedparser
from datetime import datetime, timedelta

# ----------------------------------
# GDACS GeoRSS Events
# ----------------------------------

RSS_MAX_ARTICLES = 30
RSS_FEED_URL = "https://www.gdacs.org/xml/rss.xml"

def fetch_gdacs_rss():
    """
    Fetch the GeoRSS feed from GDACS
    """
    try:
        feed = feedparser.parse(RSS_FEED_URL)
    except Exception as e:
        print(f"[fetch_gdacs_rss] Error: {e}")
        return []

    entries = feed.entries if hasattr(feed, "entries") else []
    return entries[:RSS_MAX_ARTICLES]


def parse_rss_entry(entry):
    """
    Parses a GDACS GeoRSS entry into a structured dict.
    """
    title = entry.get("title", "")
    link = entry.get("link", "")
    description = entry.get("description", "")
    published = entry.get("published", "")

    try:
        dt = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
        published_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        published_str = published

    lat = entry.get("geo_lat") or entry.get("geo:lat") or ""
    lon = entry.get("geo_long") or entry.get("geo:long") or ""
    location = f"{lat}, {lon}" if lat and lon else "Unknown"

    return {
        "title": title,
        "link": link,
        "description": description,
        "published": published_str,
        "lat": lat,
        "lon": lon,
        "location": location
    }


# ----------------------------------
# Google News RSS (for Alertpage)
# ----------------------------------

NEWS_MAX_ARTICLES = 10
NEWS_MAX_AGE_WEEKS = 4

def fetch_google_news_rss(query: str):
    """
    Fetches and filters Google News RSS articles based on query.
    """
    if not query:
        return []

    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}"

    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"[fetch_google_news_rss] RSS error: {e}")
        return []

    articles = []
    cutoff = datetime.now() - timedelta(weeks=NEWS_MAX_AGE_WEEKS)

    for entry in feed.entries:
        try:
            published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        except Exception:
            continue

        if published_date < cutoff:
            continue

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": published_date.strftime("%Y-%m-%d %H:%M:%S"),
            "source": getattr(entry, "source", {}).get("title", "Unknown")
        })

        if len(articles) >= NEWS_MAX_ARTICLES:
            break

    return articles
