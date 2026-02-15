from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView
from files.helper import parse_thread
from files.gemini import analyze_articles_with_gemini, analyze_posts_with_ai
from files.fetch_gdacs_events import fetch_google_news_rss
from files.constants import DISASTERBOXES
import folium
import requests


class AlertDetailsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        back_button = QPushButton("Back to Dashboard")
        back_button.clicked.connect(
            lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.dashboard_page)
        )
        layout.addWidget(back_button)

        self.alert_details = QTextEdit()
        self.alert_details.setReadOnly(True)
        layout.addWidget(self.alert_details)

        self.insights_label = QLabel("🔍 Insights from News Articles")
        layout.addWidget(self.insights_label)

        self.insights = QTextEdit()
        self.insights.setReadOnly(True)
        layout.addWidget(self.insights)

        self.news_articles_label = QLabel("📰 News Articles")
        layout.addWidget(self.news_articles_label)

        self.news_articles = QTextBrowser()
        self.news_articles.setOpenExternalLinks(True)
        layout.addWidget(self.news_articles)

        self.media_label = QLabel("🔍 Insights from Social Posts")
        layout.addWidget(self.media_label)

        self.media_posts = QTextEdit()
        self.media_posts.setReadOnly(True)
        layout.addWidget(self.media_posts)

        self.map_label = QLabel("📍 Nearby Shelters:")
        layout.addWidget(self.map_label)

        self.shelter_map = QWebEngineView()
        layout.addWidget(self.shelter_map)

    def set_alert_details(self, alert):
        details_html = f"""
        <h1>{alert['title']}</h1>
        <p><b>Time:</b> {alert['time_ago']}</p>
        <p><b>Location:</b> {alert['location']}</p>
        <p><b>Severity:</b> {alert['severity']}</p>
        """
        self.alert_details.setHtml(details_html)

        map_html = self.generate_shelter_map(alert)
        self.shelter_map.setHtml(map_html)

        self.fetch_additional_data(alert)

    def fetch_additional_data(self, alert):

        # 🔥 FIXED: Build query from title directly (GeoRSS has no structured country field)
        query = alert.get("title", "")

        # ---------------- NEWS ----------------
        articles = fetch_google_news_rss(query) if query else []

        if articles:
            html = "<ul>"
            for article in articles:
                html += f"<li><a href='{article['link']}'>{article['title']}</a> ({article['source']})</li>"
            html += "</ul>"
            self.news_articles.setHtml(html)

            ai_insights = analyze_articles_with_gemini(articles)
            self.insights.setPlainText(ai_insights)

            self.news_articles_label.show()
            self.news_articles.show()
            self.insights_label.show()
            self.insights.show()
        else:
            self.news_articles_label.hide()
            self.news_articles.hide()
            self.insights_label.hide()
            self.insights.hide()

        # ---------------- SOCIAL ----------------
        posts = self.scrape_threads(query) if query else []

        if posts:
            post_insights = analyze_posts_with_ai(posts)
            self.media_posts.setPlainText(post_insights)
            self.media_label.show()
            self.media_posts.show()
        else:
            self.media_label.hide()
            self.media_posts.hide()

    def scrape_threads(self, query):
        try:
            from playwright.sync_api import sync_playwright
            from parsel import Selector
            import json
            from nested_lookup import nested_lookup
        except ImportError:
            return []

        threads = []

        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(f"https://www.threads.net/search?q={query}")
                page.wait_for_timeout(3000)

                selector = Selector(page.content())
                hidden_data = selector.css(
                    'script[type="application/json"][data-sjs]::text'
                ).getall()

                for hidden in hidden_data:
                    if "thread_items" not in hidden:
                        continue

                    data = json.loads(hidden)
                    thread_items = nested_lookup("thread_items", data)

                    for thread in thread_items:
                        for item in thread:
                            parsed = parse_thread(item)
                            if parsed:
                                threads.append(parsed)
                            if len(threads) >= 10:
                                break
                        if len(threads) >= 10:
                            break
                    if len(threads) >= 10:
                        break

                browser.close()

        except Exception as e:
            print(f"[scrape_threads] Failed: {e}")

        return threads

    def generate_shelter_map(self, alert_location):

        # 🔥 FIXED: Use GeoRSS lat/lon fields
        lat = alert_location["details"].get("lat")
        lon = alert_location["details"].get("lon")

        if not lat or not lon:
            return "<h2>Location coordinates unavailable</h2>"

        try:
            lat = float(lat)
            lon = float(lon)
        except Exception:
            return "<h2>Invalid coordinates</h2>"

        shelter_map = folium.Map(location=[lat, lon], zoom_start=8)

        # Mark event location
        folium.Marker(
            [lat, lon],
            popup="Disaster Location",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(shelter_map)

        # Overpass query
        try:
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
                [out:json];
                node["emergency"="yes"](around:5000,{lat},{lon});
                out body;
            """
            response = requests.get(overpass_url, params={"data": overpass_query}, timeout=5)

            if response.status_code == 200:
                data = response.json()
                for element in data.get("elements", []):
                    lat_e = element.get("lat")
                    lon_e = element.get("lon")
                    name = element.get("tags", {}).get("name")

                    if lat_e and lon_e and name:
                        folium.Marker(
                            [lat_e, lon_e],
                            popup=name,
                            icon=folium.Icon(color="blue"),
                        ).add_to(shelter_map)

        except Exception:
            pass

        return shelter_map._repr_html_()
