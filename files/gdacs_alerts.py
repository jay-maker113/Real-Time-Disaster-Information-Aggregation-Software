from files.fetch_gdacs_events import fetch_gdacs_rss, parse_rss_entry
from files.helper import shrink_square
from files.constants import DISASTERBOXES
from datetime import datetime

def infer_disaster_type(title):
    """
    Simple keyword best-effort match for disaster types in title text.
    You chose Option 1: straight keyword matching.
    """
    text = title.lower()

    if "flood" in text:
        return "Flood", "green", "flood.png"
    elif "earthquake" in text:
        return "EarthQuake", "brown", "earthquake.png"
    elif "wildfire" in text or "fire" in text:
        return "Wildfire", "darkred", "fire.png"
    elif "tropical cyclone" in text or "cyclone" in text:
        return "Tropical Cyclone", "blue", "cyclone.png"
    elif "volcano" in text:
        return "Volcano", "red", "volcano.png"
    elif "drought" in text:
        return "Drought", "orange", "drought.png"
    else:
        return "Unknown", "gray", ""

def fetch_gdacs_alerts():
    """
    Fetches alerts from GDACS GeoRSS feed,
    maps them into your expected alert structure,
    and returns a list to feed the UI.
    """
    DISASTERBOXES.clear()

    # Pull raw RSS entries
    entries = fetch_gdacs_rss()
    if not entries:
        return []

    alerts = []
    seen_ids = set()

    for entry in entries:
        parsed = parse_rss_entry(entry)

        # Build a fake unique ID from title + published
        uid = f"{parsed['title']}_{parsed['published']}"
        if uid in seen_ids:
            continue
        seen_ids.add(uid)

        # Disaster type inference
        label, color, imagefile = infer_disaster_type(parsed["title"])

        # Default bounding box: small square around point
        try:
            lat = float(parsed["lat"])
            lon = float(parsed["lon"])
            # Build a tiny box around point
            dlat = 0.1
            dlon = 0.1
            bbox = [lon - dlon, lon + dlon, lat - dlat, lat + dlat]
            shape = shrink_square(bbox, factor=0.3)
            shape_type = "square"
        except Exception:
            shape = []
            shape_type = ""

        DISASTERBOXES.append({
            "id": uid,
            "bbox": shape,
            "color": color,
            "label": label,
            "type": shape_type,
        })

        alerts.append({
            "id": uid,
            "name": parsed["title"],
            "type": label,
            "imagefile": imagefile,
            "title": parsed["title"],
            "description": parsed["description"],
            "location": parsed["location"],
            "severity": "",  # RSS feed does not include severity
            "time_ago": parsed["published"],
            "image": "",
            "link": parsed["link"],
            "details": parsed,
        })

    # Sort newest first
    alerts.sort(key=lambda x: x["time_ago"], reverse=True)

    return alerts
