from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

class MapPage(QWebEngineView):
    """
    A map view to display disaster zones.
    This uses Folium and embeds the HTML SVG into a QWebEngineView.
    """

    def __init__(self, disaster_boxes=None):
        super().__init__()
        # Accept a list of disaster boxes or an empty list
        self.disaster_boxes = disaster_boxes or []
        self.load_map()

    def load_map(self):
        """
        Generate the initial map HTML with all disaster shapes.
        """
        # Create a world center map
        m = folium.Map(location=[0, 0], zoom_start=2)

        # Add each box shape
        for box in self.disaster_boxes:
            try:
                shape_type = box.get("type")
                bbox = box.get("bbox", [])
                color = box.get("color", "blue")
                label = box.get("label", "")

                # Polygon shape
                if shape_type == "polygon":
                    folium.Polygon(
                        locations=bbox,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.4,
                        popup=label,
                    ).add_to(m)

                # Rectangle shape (fallback)
                elif shape_type == "square":
                    if len(bbox) == 4:
                        folium.Rectangle(
                            bounds=[(bbox[2], bbox[0]), (bbox[3], bbox[1])],
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.4,
                            popup=label,
                        ).add_to(m)

            except Exception as e:
                print(f"[Mappage] Error drawing shape: {e}")
                continue

        # Safely set HTML to QtWebEngine
        try:
            html = m._repr_html_()
            self.setHtml(html)
        except Exception as e:
            print(f"[Mappage] Failed to set map HTML: {e}")
            # Fallback to a message
            fallback_html = "<h2>Map could not be displayed.</h2>"
            self.setHtml(fallback_html)

    def set_theme(self):
        """
        Reload map — for future toggle themes, etc.
        """
        self.load_map()
