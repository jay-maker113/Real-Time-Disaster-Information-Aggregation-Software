
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium



class MapPage(QWebEngineView):
    def __init__(self, disaster_boxes=None):
        super().__init__()
        self.disaster_boxes = disaster_boxes if disaster_boxes else []
        self.load_map()

    def load_map(self):


        m = folium.Map(location=[0, 0], zoom_start=2)

        for box in self.disaster_boxes:
            if box['type'] == 'polygon':
                folium.Polygon(
                    locations=box['bbox'],
                    color=box['color'],
                    fill=True,
                    fill_color=box['color'],
                    fill_opacity=0.4,
                    popup=box['label']
                ).add_to(m)
            elif box['type'] == 'square':

                folium.Rectangle(
                    bounds=[(box['bbox'][2], box['bbox'][0]), (box['bbox'][3], box['bbox'][1])],
                    color=box['color'],
                    fill=True,
                    fill_color=box['color'],
                    fill_opacity=0.4,
                    popup=box['label']
                ).add_to(m)


        self.setHtml(m._repr_html_())

    def set_theme(self):
        self.load_map()