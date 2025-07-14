cd "$(dirname "$0")/.." || exit 1

echo "Formatting all Python files in ./src/scraper with black..."

find ./src/scraper -type f -name "*.py" | while read file; do
    echo "Formatting $file"
    black "$file"
done

echo "Formatting complete."