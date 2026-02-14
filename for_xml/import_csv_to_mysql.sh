#!/bin/bash
# Convenience script to import WOS XML CSV files into MySQL/MariaDB
# Works with both MySQL and MariaDB servers
# Usage: ./import_csv_to_mysql.sh [mysql_password] [database_name]

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Default values
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${1:-}"
DB_NAME="${2:-wos_xml}"
CSV_DIR="${CSV_DIR:-xml_output}"

echo "=================================================="
echo "WOS XML to MySQL/MariaDB Import Script"
echo "=================================================="
echo "Host: $DB_HOST"
echo "User: $DB_USER"
echo "Database: $DB_NAME"
echo "CSV Directory: $CSV_DIR"
echo "=================================================="
echo ""

# Check if pymysql is installed
if ! python -c "import pymysql" 2>/dev/null; then
    echo "⚠ pymysql package not found. Installing..."
    pip install pymysql
    echo "✓ pymysql installed successfully"
    echo ""
fi

# Check if CSV directory exists
if [ ! -d "$CSV_DIR" ]; then
    echo "✗ Error: CSV directory '$CSV_DIR' not found!"
    echo "Please run the XML parser first to generate CSV files:"
    echo "  python xml_proc_main.py path/to/xml/files/"
    exit 1
fi

# Run the import script
if [ -n "$DB_PASSWORD" ]; then
    python import_to_mysql.py \
        --host "$DB_HOST" \
        --user "$DB_USER" \
        --password "$DB_PASSWORD" \
        --database "$DB_NAME" \
        --csv-dir "$CSV_DIR"
else
    python import_to_mysql.py \
        --host "$DB_HOST" \
        --user "$DB_USER" \
        --database "$DB_NAME" \
        --csv-dir "$CSV_DIR"
fi

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Import completed successfully!"
    echo "=================================================="
    echo ""
    echo "You can now query the database:"
    echo "  For MySQL: mysql -u $DB_USER -p $DB_NAME"
    echo "  For MariaDB: mariadb -u $DB_USER -p $DB_NAME"
    echo ""
    echo "Or run example queries:"
    echo "  python example_queries.py"
else
    echo ""
    echo "✗ Import failed with exit code $exit_code"
    exit $exit_code
fi
