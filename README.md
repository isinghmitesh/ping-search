# Ping Search

A simple and privacy-focused product discovery and price comparison web application.

> "Everything should be made as simple as possible, but not simpler" - Albert Einstein

## Overview

Ping Search is a Django-based web application that helps you discover and compare products across multiple e-commerce platforms. It aggregates search results from Amazon, Flipkart, Snapdeal, and eBay, allowing you to compare prices and find the best deals without compromising your privacy.

## Features

- **Privacy-Focused Search**: Your searches remain private - no tracking, no targeted ads based on your search history
- **Multi-Platform Price Comparison**: Compare products from Amazon, Flipkart, Snapdeal, and eBay in one place
- **Product Discovery**: Browse and discover products across different platforms
- **Surprise Me Feature**: Randomly discover interesting products
- **Simple Interface**: Clean and straightforward user experience

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Web Scraping**: BeautifulSoup4, Requests

## Installation

### Prerequisites

- Python 2.7 or Python 3.x
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/isinghmitesh/ping-search.git
   cd ping-search
   ```

2. Install required dependencies:
   ```bash
   pip install django
   pip install beautifulsoup4
   pip install requests
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Usage

1. **Search Products**: Enter a product name or keyword in the search box on the homepage
2. **View Results**: Browse through aggregated results from multiple e-commerce platforms
3. **Compare Prices**: See prices from different platforms side by side
4. **Surprise Me**: Click the "Surprise" feature to discover random products

## Project Structure

```
ping-search/
├── ping_search/        # Main Django project settings
├── search/            # Main application
│   ├── templates/     # HTML templates
│   ├── static/        # CSS, JS, and image files
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   └── urls.py        # URL routing
├── manage.py          # Django management script
└── README.md          # This file
```

## Known Limitations

- **First Search Delay**: The first search for a particular keyword may be slower as the application needs to fetch and cache data from multiple platforms
- **Platform Availability**: Search results depend on the availability and responsiveness of third-party e-commerce platforms

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational purposes. When using this application, please respect the terms of service of the e-commerce platforms being accessed.

## Contact

For questions or feedback, please open an issue on the GitHub repository.
