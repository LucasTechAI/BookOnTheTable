BookOnTheTable
==============

BookOnTheTable is a web application built with FastAPI that provides a RESTful API for managing book-related data, including authentication, categorization, statistics, scraping, and dashboard visualization. The project is configured for deployment on Vercel and uses a local SQLite database.

Project Structure
-----------------

.
├── books_data.csv               # Extracted book data
├── docs                         # Documentation and challenge materials
├── tmp/bookonthetable.db   # SQLite database
├── main.py                      # Main execution entrypoint
├── README.md                    # Project README
├── requirements.txt             # Python dependencies
├── setup                        # Setup and formatting scripts
├── src
│   ├── api                      # FastAPI core application
│   ├── dashboards               # (WIP) Visual dashboards
│   └── scraper                  # Web scraping scripts
├── utils                        # Utility modules and helpers
└── vercel.json                  # Deployment configuration for Vercel

Getting Started
---------------

1. Clone the repository:

    git clone https://github.com/your-user/BookOnTheTable.git
    cd BookOnTheTable

2. Create a virtual environment:

    python -m venv venv
    source venv/bin/activate        # On Linux/macOS
    venv\Scripts\activate           # On Windows

3. Install the dependencies:

    pip install -r requirements.txt

4. Initialize the database:

    sqlite3 tmp/bookonthetable.db < setup/creator.sql

5. Run the application:

    uvicorn src.api.app:app --reload

Access the API docs at: http://127.0.0.1:8000/docs

Features
--------

- JWT-based authentication
- Book listing, filtering, and management
- Category creation and retrieval
- Usage statistics and metrics
- Request logging middleware
- Web scraping via BeautifulSoup
- (Coming soon) Interactive dashboards
- Easy deployment on Vercel

Deployment
----------

This project includes a `vercel.json` file for seamless deployment on [Vercel](https://vercel.com/). The main entrypoint is defined in `main.py`.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

Challenge
---------

This project was developed as part of the "Tech Challenge - Phase 1 - Machine Learning Engineering" from Pos Tech.

Author
------

Lucas Mendes  
Data Scientist Mid-Level
Website: https://musicmoodai.com.br  
Email: lucas.mendestech@gmail.com

