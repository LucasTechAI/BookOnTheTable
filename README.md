# 📚 BookOnTheTable

**BookOnTheTable** is a web application built with **FastAPI** that offers a **public RESTful API** for querying books, including features such as authentication, categorization, statistics, automated scraping, and endpoints designed for consumption by Machine Learning models.

> You can find all the challenge requirements and details in the official document:  
[Tech Challenge - Phase 1 - Machine Learning Engineering (PDF)](https://github.com/LucasTechAI/BookOnTheTable/blob/main/docs/Pos_tech%20-%20Tech%20Challenge%20-%20Fase%201%20-%20Machine%20Learning%20Engineering.pdf)

---

## 🌐 Public URL

Access the public API hosted on Vercel:

- 🔗 **API:** [https://book-on-the-table.vercel.app](https://book-on-the-table.vercel.app)  
- 📑 **Swagger UI:** [https://book-on-the-table.vercel.app/docs](https://book-on-the-table.vercel.app/docs)  
- 📘 **Redoc:** [https://book-on-the-table.vercel.app/redoc](https://book-on-the-table.vercel.app/redoc)  

---

## 🧩 Project Structure

```bash
BookOnTheTable/
├── books_data.csv               # Extracted book data from scraping
├── docs                         # PDF and challenge documents
├── tmp/bookonthetable.db        # SQLite database
├── main.py                      # Main entry point
├── requirements.txt             # Project dependencies
├── setup/                       # Helper scripts (SQL, formatters)
├── src/
│   ├── api/                     # FastAPI app (routes, schemas, services)
│   ├── dashboards/              # (WIP) Streamlit dashboards
│   ├── scraper/                 # Web scraper using BeautifulSoup
│   └── test/                    # Automated tests
├── utils/                       # General utilities (JWT, DB, etc.)
├── vercel.json                  # Vercel deployment config
└── README.md
```

---

## 🚀 How to run the API locally

1. **Clone the repository**

```bash
git clone https://github.com/LucasTechAI/BookOnTheTable.git
cd BookOnTheTable
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate       # Windows
```

3. **Install the dependencies**

```bash
pip install -r requirements.txt
```
4. **Run the application**

```bash
PYTHONPATH=. uvicorn src.api.app:app --reload
```

API Docs available locally at:  
📑 http://127.0.0.1:8000/docs

---

## ✅ Features

- JWT-based authentication (login, register, refresh)
- Book listing and search
- Category filtering
- General and category-specific statistics
- ML-ready endpoints (features, training data, predictions)
- Automated scraping from books.toscrape.com
- Structured logging via middleware
- (Coming soon) Interactive dashboards with Streamlit
- Continuous deployment on Vercel

---

## 📡 Main Endpoints

### Books
- GET /api/v1/books
- GET /api/v1/books/{id}
- GET /api/v1/books/search?title=...&category=...
- GET /api/v1/books/top-rated
- GET /api/v1/books/price-range?min=10&max=50

### Categories
- GET /api/v1/categories

### Health & Logs
- GET /api/v1/health
- GET /api/v1/logs
- DELETE /api/v1/logs

### Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- GET /api/v1/auth/protected

### Machine Learning
- GET /api/v1/ml/features
- GET /api/v1/ml/training-data
- POST /api/v1/ml/predictions
  
---

## 🕷️ Run Only the Scraper (Optional)

If you want to run the scraper separately to update or generate the `books_data.csv` file:

```bash
cd BookOnTheTable
python3 src/scraper/main.py
```

This will fetch all book data from [books.toscrape.com](https://books.toscrape.com/) and save it in `books_data.csv` for local use or further ML processing.

---

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- SQLite3
- BeautifulSoup
- Pydantic
- Uvicorn
- Vercel (deployment)
- JWT

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 👨‍💻 Author

**Lucas Mendes**  
Mid-Level Data Scientist  
🌐 https://musicmoodai.com.br  
📧 lucas.mendestech@gmail.com