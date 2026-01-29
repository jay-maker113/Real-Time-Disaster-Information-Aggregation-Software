
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit, QTextBrowser
from PyQt5.QtWebEngineWidgets import QWebEngineView
from files.helper import parse_thread
from files.gemini import analyze_articles_with_gemini
from files.fetch_gdcas_events import fetch_google_news_rss
from playwright.sync_api import sync_playwright
from parsel import Selector
import json
from nested_lookup import nested_lookup
import folium
import requests
from files.constants import DISASTERBOXES
from files.gemini import analyze_posts_with_ai


class AlertDetailsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)


        back_button = QPushButton("Back to Dashboard")
        back_button.clicked.connect(lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.dashboard_page))
        layout.addWidget(back_button)


        self.alert_details = QTextEdit()
        self.alert_details.setReadOnly(True)
        layout.addWidget(self.alert_details)







        self.insights_label = QLabel("🔍 Insights from News Articles")
        self.insights_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(self.insights_label)

        self.insights = QTextEdit()
        self.insights.setReadOnly(True)
        layout.addWidget(self.insights)






        self.news_articles_label = QLabel("📰 News Articles")
        self.news_articles_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(self.news_articles_label)

        self.news_articles = QTextBrowser()
        self.news_articles.setReadOnly(True)
        self.news_articles.setOpenExternalLinks(True)

        layout.addWidget(self.news_articles)




        self.media_label = QLabel("🔍 Insights from Media Posts")
        self.media_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(self.media_label)

        self.media_posts = QTextEdit()
        self.media_posts.setReadOnly(True)
        layout.addWidget(self.media_posts)




        self.map_label = QLabel("📍 Nearby Shelters:")
        self.map_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(self.map_label)

        self.shelter_map = QWebEngineView()
        layout.addWidget(self.shelter_map)



            
    def set_alert_details(self, alert):

        details = f"""
        <h1>{alert['title']}</h1>
        <p><b>Time:</b> {alert['time_ago']}</p>
        <p><b>Location:</b> {alert['location']}</p>
        <p><b>Severity:</b> {alert['severity']}</p>
        """
        self.alert_details.setHtml(details)

        map_html = self.generate_shelter_map(alert)


        self.shelter_map.setHtml(map_html)
            
        self.fetch_data(alert)


    def fetch_data(self, alert):
        query = f"{alert['details']['gdacs:country']} {alert['type']}"


        if alert['type'] == None or alert['details']['gdacs:country'] == None:
            articles = []
        else:
            articles = fetch_google_news_rss(query)

        if articles:
            articles_html = "<h2>News Articles</h2><ul>"
            for article in articles:
                articles_html += f"<li><a href='{article['link']}'>{article['title']}</a> ({article['source']})</li>"
            articles_html += "</ul>"
            self.news_articles.setHtml(articles_html)


            insights = analyze_articles_with_gemini(articles)
            self.insights.setPlainText(insights)


            self.insights_label.show()
            self.insights.show()

            self.news_articles_label.show()
            self.news_articles.show()


        else:

            self.news_articles_label.hide()
            self.news_articles.hide()
            self.insights_label.hide()
            self.insights.hide()

        
        posts = self.scrape_threads(query)


        if posts:
            post_insights = analyze_posts_with_ai(posts)
            
            self.media_posts.setPlainText(post_insights)
            self.media_label.show()
            self.media_posts.show()


        else:
            self.media_label.hide()
            self.media_posts.hide()


    def scrape_threads(self, query):

        url = f"https://www.threads.net/search?q={query}"
        threads = []

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)  
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            page.goto(url)
            page.wait_for_selector("[data-pressable-container=true]")

            selector = Selector(page.content())
            hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()


            for hidden_dataset in hidden_datasets:

                if '"ScheduledServerJS"' not in hidden_dataset:
                    continue
                if "thread_items" not in hidden_dataset:
                    continue


                data = json.loads(hidden_dataset)
                thread_items = nested_lookup("thread_items", data)
                if not thread_items:
                    continue


                for thread in thread_items:
                    for t in thread:
                        threads.append(parse_thread(t))
                        if len(threads) >= 10: 
                            break
                    if len(threads) >= 10:
                        break
                if len(threads) >= 10:
                    break


            browser.close()

        return threads[:10]




    def generate_shelter_map(self, alert_location):

        lat = alert_location['details'].get("geo:Point", {}).get("geo:lat", "Unknown")
        lon = alert_location['details'].get("geo:Point", {}).get("geo:long", "Unknown")

        if lat == 'Unknown' or lon == 'Unknown':
            return None
        
        else:


            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["emergency"="yes"](around:500000,{lat},{lon});
            );
            out body;
            """
            response = requests.get(overpass_url, params={"data": overpass_query})

            shelter_map = folium.Map(location=[lat, lon], zoom_start=14)

            flag = False
            for i in DISASTERBOXES:
                if i['id'] == alert_location['id']:
                    box = i
                    flag = True
                    break
            
            if flag:
                if box['type'] == 'polygon':
                    folium.Polygon(
                        locations=box['bbox'],
                        color=box['color'],
                        fill=True,
                        fill_color=box['color'],
                        fill_opacity=0.4,
                        popup=box['label']
                    ).add_to(shelter_map)
                elif box['type'] == 'square':

                    folium.Rectangle(
                        bounds=[(box['bbox'][2], box['bbox'][0]), (box['bbox'][3], box['bbox'][1])],
                        color=box['color'],
                        fill=True,
                        fill_color=box['color'],
                        fill_opacity=0.4,
                        popup=box['label']
                    ).add_to(shelter_map)

            if response.status_code == 200:
                data = response.json()
                for element in data["elements"]:
                    if "lat" in element and "lon" in element:
                        name = element["tags"].get("name", "Unnamed")
                        if name == "Unnamed":
                            pass
                        else:
                            folium.Marker(
                                [element["lat"], element["lon"]],
                                popup=name,
                                icon=folium.Icon(color="blue", icon="info-sign"),
                            ).add_to(shelter_map)
            else:
                print("Failed Overpass")

            return shelter_map._repr_html_()
