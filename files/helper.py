from nested_lookup import nested_lookup

# -------------------------------------------
# Geo Bounding Box Adjustment
# -------------------------------------------
def shrink_square(bbox, factor=0.5):
    """
    Shrinks a bounding box toward its center by a given factor.
    Args:
        bbox (list): [lon_min, lon_max, lat_min, lat_max]
        factor (float): How much to shrink (0.5 = half size)
    Returns:
        list: New [lon_min, lon_max, lat_min, lat_max]
    """
    try:
        lon_min, lon_max, lat_min, lat_max = bbox
    except Exception:
        # If bbox is malformed, just return as is
        return bbox

    lon_center = (lon_min + lon_max) / 2
    lat_center = (lat_min + lat_max) / 2

    lon_range = lon_max - lon_min
    lat_range = lat_max - lat_min

    new_lon_range = lon_range * factor
    new_lat_range = lat_range * factor

    new_lon_min = lon_center - new_lon_range / 2
    new_lon_max = lon_center + new_lon_range / 2
    new_lat_min = lat_center - new_lat_range / 2
    new_lat_max = lat_center + new_lat_range / 2

    return [new_lon_min, new_lon_max, new_lat_min, new_lat_max]


# -------------------------------------------
# Thread/Post Parsing
# -------------------------------------------
def parse_thread(thread):
    """
    Given a thread item (scraped JSON),
    extracts text, username, and timestamp safely.

    Returns a dict with those keys, or None on failure.
    """
    try:
        text_val = nested_lookup("text", thread)
        user_val = nested_lookup("username", thread)
        time_val = nested_lookup("timestamp", thread)

        # Ensure extracted results are plain values, not nested lists
        text = text_val[0] if isinstance(text_val, list) and text_val else ""
        username = user_val[0] if isinstance(user_val, list) and user_val else ""
        timestamp = time_val[0] if isinstance(time_val, list) and time_val else ""

        return {
            "text": text,
            "username": username,
            "timestamp": timestamp
        }
    except Exception as e:
        # If parsing fails, return minimal structure
        print(f"[helper.parse_thread] failed: {e}")
        return {
            "text": "",
            "username": "",
            "timestamp": ""
        }
