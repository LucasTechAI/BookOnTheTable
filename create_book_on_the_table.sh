#!/bin/bash

PROJECT_NAME="BookOnTheTable"

mkdir -p src/api/routes
mkdir -p src/api/models
mkdir -p src/api/services
mkdir -p src/api/utils

mkdir -p src/dashboards/components
mkdir -p src/etl
mkdir -p src/database/models

mkdir -p tests
mkdir -p data/raw
mkdir -p data/processed
mkdir -p docs

touch README.md
touch .gitignore
touch requirements.txt
touch vercel.json
touch .env.example

touch src/api/__init__.py
touch src/api/main.py
touch src/api/config.py

touch src/api/routes/__init__.py
touch src/api/routes/books.py
touch src/api/routes/categories.py
touch src/api/routes/stats.py
touch src/api/routes/health.py

touch src/api/models/__init__.py
touch src/api/services/__init__.py
touch src/api/utils/__init__.py

touch src/dashboards/__init__.py
touch src/dashboards/app.py
touch src/dashboards/components/charts.py

touch src/etl/__init__.py
touch src/etl/scraping.py
touch src/etl/transform.py

touch src/database/__init__.py
touch src/database/db_main.py
touch src/database/db_logs.py
touch src/database/models/__init__.py
touch src/database/models/base.py
touch src/database/models/book.py

touch tests/test_api.py
touch tests/test_scraping.py

touch docs/README_detalhado.md
touch docs/architecture.png

echo "Project '$PROJECT_NAME' created successfully with all initial structure!"