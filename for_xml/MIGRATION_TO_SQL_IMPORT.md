# Migration from Python Import to SQL Import

## Summary of Changes

The MariaDB/MySQL import process has been updated to use direct SQL commands instead of Python scripts. This change simplifies the import process and removes the dependency on Python packages for database operations.

## What Changed

### New Files
- `create_database_and_tables.sql` - SQL script to create database schema and all 33 tables
- `import_csv_data.sql` - SQL script to import CSV data using `LOAD DATA LOCAL INFILE`

### Modified Files
- `import_csv_to_mysql.sh` - Updated to use SQL commands via mysql/mariadb CLI instead of Python
- `requirements_mysql.txt` - Updated to note Python packages are only needed for example queries
- `README.md` - Updated with new import instructions
- `MYSQL_IMPORT_GUIDE.md` - Comprehensive update with SQL-based approach
- `MYSQL_IMPORT_README_CN.md` - Chinese documentation updated

### Removed Files
- `import_to_mysql.py` - Python import script no longer needed

## Migration Guide

If you were previously using the Python import script:

### Old Method (No Longer Supported)
```bash
pip install pymysql
python import_to_mysql.py --host localhost --user root --password mypass
```

### New Method (Current)

**Option 1: Using the bash script (Recommended)**
```bash
./import_csv_to_mysql.sh mypass wos_xml
```

**Option 2: Using SQL commands directly**
```bash
# Step 1: Create database and tables
mysql -u root -p < create_database_and_tables.sql

# Step 2: Import CSV data
mysql -u root -p --local-infile=1 < import_csv_data.sql
```

## Benefits of This Change

1. **Simpler Dependencies**: No Python packages required for database import
2. **Better Performance**: Direct SQL import is faster than Python-based row-by-row insertion
3. **Standard Tools**: Uses standard mysql/mariadb CLI tools available on all systems
4. **Easier Debugging**: SQL scripts can be easily inspected and modified
5. **More Portable**: Works on any system with MySQL/MariaDB client installed

## Notes

- Python is still needed for:
  - Running the XML parser (`xml_proc_main.py`)
  - Running example queries (`example_queries.py`)
  
- The database schema and import order remain exactly the same
- All 33 tables are created with the same structure, indexes, and foreign keys

## Troubleshooting

If you encounter issues with the new import method, see the [MYSQL_IMPORT_GUIDE.md](MYSQL_IMPORT_GUIDE.md) troubleshooting section, which includes:
- LOAD DATA INFILE permission issues
- local_infile configuration
- secure_file_priv settings
- File path issues
