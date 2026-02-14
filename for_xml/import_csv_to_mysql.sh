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

# Check if CSV directory exists
if [ ! -d "$CSV_DIR" ]; then
    echo "✗ Error: CSV directory '$CSV_DIR' not found!"
    echo "Please run the XML parser first to generate CSV files:"
    echo "  python xml_proc_main.py path/to/xml/files/"
    exit 1
fi

# Detect if we have mysql or mariadb command
if command -v mariadb &> /dev/null; then
    MYSQL_CMD="mariadb"
elif command -v mysql &> /dev/null; then
    MYSQL_CMD="mysql"
else
    echo "✗ Error: Neither 'mysql' nor 'mariadb' command found!"
    echo "Please install MySQL or MariaDB client."
    exit 1
fi

echo "Using $MYSQL_CMD command..."
echo ""

# Build MySQL/MariaDB connection arguments
MYSQL_ARGS="-h $DB_HOST -u $DB_USER"
if [ -n "$DB_PASSWORD" ]; then
    MYSQL_ARGS="$MYSQL_ARGS -p$DB_PASSWORD"
fi

# Step 1: Create database and tables
echo "Step 1: Creating database and tables..."
echo "=================================================="
if [ -n "$DB_PASSWORD" ]; then
    $MYSQL_CMD -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" < create_database_and_tables.sql
else
    $MYSQL_CMD -h "$DB_HOST" -u "$DB_USER" < create_database_and_tables.sql
fi

if [ $? -eq 0 ]; then
    echo "✓ Database and tables created successfully!"
else
    echo "✗ Failed to create database and tables"
    exit 1
fi
echo ""

# Step 2: Import CSV data
echo "Step 2: Importing CSV data..."
echo "=================================================="

# Create a temporary SQL file with updated CSV paths
TMP_SQL=$(mktemp)
sed "s|'xml_output/|'$SCRIPT_DIR/$CSV_DIR/|g" import_csv_data.sql > "$TMP_SQL"

if [ -n "$DB_PASSWORD" ]; then
    $MYSQL_CMD -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" --local-infile=1 < "$TMP_SQL"
else
    $MYSQL_CMD -h "$DB_HOST" -u "$DB_USER" --local-infile=1 < "$TMP_SQL"
fi

exit_code=$?
rm -f "$TMP_SQL"

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
    echo ""
    echo "Note: If you see 'command not allowed' errors, you may need to:"
    echo "1. Enable local_infile in your MySQL/MariaDB configuration"
    echo "2. Grant FILE privilege to the user"
    echo "3. Check secure_file_priv settings"
    exit $exit_code
fi
