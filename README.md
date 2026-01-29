<<<<<<< HEAD
# 🌍 Real-Time Disaster Information Aggregation Software

A comprehensive desktop application for real-time disaster monitoring and response, built with Python and PyQt5. This software aggregates data from multiple sources including GDACS API, news feeds, social media, and emergency contacts to provide actionable insights during disaster events.

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🏠 Dashboard
- **Real-time Alerts**: Displays active disaster alerts from GDACS API
- **Visual Cards**: Each alert shown with disaster image, title, location, severity, and timestamp
- **Interactive**: Click on alerts to view detailed information

### 🗺️ Map View
- **Interactive World Map**: Built with Folium for smooth navigation
- **Disaster Zones**: Visual representation of affected areas using polygons and rectangles
- **Color-coded**: Different disaster types have distinct colors (e.g., red for volcanoes, blue for cyclones)

### 🚨 Emergency Contacts
- **Country-wise Data**: Emergency numbers for ambulance, fire, and police
- **Easy Access**: Dropdown selector for quick country selection
- **Comprehensive**: Covers multiple countries with reliable contact information

### 📊 Alert Details
- **Detailed Information**: Complete alert data including location, severity, and timing
- **AI-Powered Insights**:
  - News analysis using Google News RSS feeds
  - Social media sentiment from Threads.net posts
  - Gemini AI-powered summarization and trend analysis
- **Shelter Mapping**: Nearby emergency shelters displayed on interactive maps using Overpass API

## 🛠️ Technologies Used

- **Frontend**: PyQt5, PyQtWebEngine
- **Mapping**: Folium
- **AI/ML**: Google Gemini AI (gemini-2.0-flash-exp)
- **Data Sources**:
  - GDACS API for disaster alerts
  - Google News RSS for articles
  - Threads.net for social media posts
  - Overpass API for shelter locations
- **Web Scraping**: Playwright, Parsel
- **Data Processing**: Requests, Feedparser, XMLtoDict, Nested Lookup
- **Other**: Concurrent Futures for threading, SMTPLib for email (if needed)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd disaster-shelter-software
   ```

2. **Install dependencies**:
   ```bash
   pip install -r assets/requirements.txt
   ```

3. **Set up environment variables**:
   - Ensure you have a valid Google Gemini API key (currently hardcoded in `files/gemini.py`)

4. **Run the application**:
   ```bash
   python assets/main.py
   ```

## 🚀 Usage

1. **Launch the Application**: Run `python assets/main.py` to start the desktop app
2. **Navigate Dashboard**: View active disaster alerts in card format
3. **Explore Map**: Switch to map view to see disaster-affected areas
4. **Access Emergency Contacts**: Select a country to view emergency numbers
5. **Drill Down**: Click on any alert card to see detailed information, AI insights, and shelter maps

## 📁 Project Structure

```
disaster-shelter-software/
│
├── assets/
│   ├── main.py                 # Main application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── emergency_contacts.json # Emergency contact data
│   ├── *.png                   # Disaster type images
│   ├── *.ttf                   # Custom fonts
│   └── *.jpg                   # Additional images
│
├── files/
│   ├── __init__.py
│   ├── constants.py            # Application constants and paths
│   ├── Dashboard.py            # Dashboard page implementation
│   ├── Mappage.py              # Map view with Folium integration
│   ├── emergency.py            # Emergency contacts page
│   ├── Alertdetails.py         # Alert card widget
│   ├── Alertpage.py            # Detailed alert view with AI insights
│   ├── gdcas_alerts.py         # GDACS API integration
│   ├── fetch_gdcas_events.py   # Event and polygon fetching
│   ├── gemini.py               # AI analysis functions
│   └── helper.py               # Utility functions
│
└── README.md                   # Project documentation
```

## 📊 Data Sources

- **GDACS API**: Provides real-time disaster alerts, severity levels, and geographical data
- **Google News RSS**: Fetches recent news articles related to disasters
- **Threads.net**: Scrapes social media posts for community insights
- **Overpass API**: Retrieves nearby emergency shelter locations
- **Emergency Contacts JSON**: Static database of country-wise emergency numbers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Jayhv** - *Initial work and development*

## 🙏 Acknowledgments

- GDACS for providing disaster alert data
- Google for News RSS and Gemini AI services
- Meta for Threads.net platform
- OpenStreetMap contributors for Overpass API data

---

*Built with ❤️ for disaster response and community safety*
=======
# disaster-shelter-software
>>>>>>> 4de9fb7a9318bbf87ef11f0388f8f768a8cdc719
