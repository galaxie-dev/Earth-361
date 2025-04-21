# Earth 361

Earth 361 is a sophisticated weather application that provides real-time weather information, forecasts, and interactive maps. Built using Flask for the backend and HTML/CSS/JavaScript for the frontend, this app delivers an intuitive user experience with comprehensive meteorological data.

## Features

### 1. **Real-Time Weather Data**
- Fetches current weather conditions for any city or geographic coordinates.
- Displays detailed metrics including:
  - Temperature (current and "feels like")
  - Humidity
  - Wind speed and direction
  - Atmospheric pressure
  - Visibility
  - Cloud coverage
  - Sunrise and sunset times
- Includes weather icons and descriptions for intuitive understanding.

### 2. **Hourly Forecast**
- Provides weather predictions for the next 24 hours in 3-hour intervals.
- Displays temperature, weather icons, and brief descriptions for each time slot.

### 3. **5-Day Forecast**
- Offers a summarized daily forecast for the next 5 days.
- Shows average temperatures, most frequent weather conditions, and corresponding icons.

### 4. **Interactive Map**
- Integrates OpenStreetMap to display the geographic location of the queried area.
- Highlights the selected location with a marker on the map.

### 5. **Location-Based Weather**
- Automatically detects the user's location using geolocation APIs.
- Allows manual entry of city names or coordinates for weather queries.

### 6. **Dynamic UI Updates**
- Updates local time dynamically based on the timezone of the selected location.
- Smooth loading animations and error handling for a seamless user experience.

---

## Technology Stack

### Backend
- **Flask**: Powers the RESTful API to fetch and process weather data.
- **OpenWeatherMap API**: Provides real-time and forecast weather data.
- **pytz**: Handles timezone conversions for accurate local time representation.

### Frontend
- **HTML5 & CSS3**: Structured layout with modern styling for responsiveness.
- **JavaScript**: Dynamically updates the UI with fetched data and handles user interactions.
- **OpenStreetMap with Leaflet.js**: Renders interactive maps for location visualization.

---

## Installation and Setup

### Prerequisites
- Python 3.x installed on your system.
- An API key from [OpenWeatherMap](https://openweathermap.org/api).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/earth-361.git
   cd earth-361