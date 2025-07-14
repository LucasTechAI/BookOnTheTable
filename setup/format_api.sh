cd "$(dirname "$0")/.." || exit 1

echo "Formatting all Python files in ./src/api with black..."

find ./src/api -type f -name "*.py" | while read file; do
    echo "Formatting $file"
    black "$file"
done

echo "Formatting complete."