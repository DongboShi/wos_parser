#!/usr/bin/env python3
"""
Example queries for the WOS XML MySQL/MariaDB database

This script demonstrates common queries you can perform on the imported data.
Works with both MySQL and MariaDB servers.

Requirements:
    - pymysql package: pip install pymysql
    - OR mysqlclient package: pip install mysqlclient
"""

import sys

# Try to import the MySQL/MariaDB library
try:
    import pymysql
    DB_LIBRARY = 'pymysql'
except ImportError:
    try:
        import MySQLdb
        # Create a compatibility wrapper for mysqlclient
        # This allows us to use the same API as pymysql throughout the code
        class MySQLClientWrapper:
            """Wrapper to make MySQLdb API compatible with pymysql"""
            Error = MySQLdb.Error
            
            @staticmethod
            def connect(**kwargs):
                return MySQLdb.connect(**kwargs)
            
            class cursors:
                DictCursor = MySQLdb.cursors.DictCursor
        
        pymysql = MySQLClientWrapper()
        DB_LIBRARY = 'mysqlclient'
    except ImportError:
        print("Error: No MySQL/MariaDB library found!")
        print("Please install one of the following:")
        print("  - PyMySQL: pip install pymysql")
        print("  - mysqlclient: pip install mysqlclient")
        sys.exit(1)


def connect_db(host='localhost', user='root', password='', database='wos_xml'):
    """Connect to the MySQL/MariaDB database"""
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        # Detect database type
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()['VERSION()']
            db_type = "MariaDB" if "MariaDB" in version else "MySQL"
            print(f"Connected to {db_type} (version: {version})")
            print(f"Using library: {DB_LIBRARY}\n")
        
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def run_query(connection, query, description):
    """Execute a query and display results"""
    print("\n" + "="*70)
    print(f"Query: {description}")
    print("="*70)
    print(f"SQL: {query}")
    print("-"*70)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                print("No results found.")
                return
            
            # Print results in a formatted way
            for i, row in enumerate(results[:20], 1):  # Limit to first 20 rows
                print(f"\nResult {i}:")
                for key, value in row.items():
                    # Truncate long text fields
                    if isinstance(value, str) and len(value) > 100:
                        value = value[:100] + "..."
                    print(f"  {key}: {value}")
            
            if len(results) > 20:
                print(f"\n... and {len(results) - 20} more results")
            else:
                print(f"\nTotal results: {len(results)}")
                
    except pymysql.Error as e:
        print(f"Error executing query: {e}")


def main():
    """Run example queries"""
    print("="*70)
    print("WOS XML Database - Example Queries (MySQL/MariaDB)")
    print("="*70)
    
    # Connect to database
    connection = connect_db()
    if not connection:
        return 1
    
    try:
        # Query 1: Count total papers
        run_query(
            connection,
            "SELECT COUNT(*) as total_papers FROM item",
            "Total number of papers in database"
        )
        
        # Query 2: Papers by year
        run_query(
            connection,
            """
            SELECT pubyear, COUNT(*) as count 
            FROM item 
            WHERE pubyear IS NOT NULL
            GROUP BY pubyear 
            ORDER BY pubyear DESC
            LIMIT 10
            """,
            "Papers published per year (top 10 recent years)"
        )
        
        # Query 3: Papers with abstracts
        run_query(
            connection,
            """
            SELECT COUNT(*) as papers_with_abstract 
            FROM item_abstract
            """,
            "Total papers with abstracts"
        )
        
        # Query 4: Top authors by number of papers
        run_query(
            connection,
            """
            SELECT full_name, COUNT(*) as paper_count 
            FROM item_authors 
            WHERE full_name IS NOT NULL
            GROUP BY full_name 
            ORDER BY paper_count DESC 
            LIMIT 10
            """,
            "Most prolific authors"
        )
        
        # Query 5: Top countries by address
        run_query(
            connection,
            """
            SELECT country, COUNT(DISTINCT uid) as paper_count 
            FROM item_addresses 
            WHERE country IS NOT NULL
            GROUP BY country 
            ORDER BY paper_count DESC 
            LIMIT 10
            """,
            "Top countries by number of papers"
        )
        
        # Query 6: Top organizations
        run_query(
            connection,
            """
            SELECT organization, COUNT(DISTINCT uid) as paper_count 
            FROM item_orgs 
            WHERE organization IS NOT NULL
            GROUP BY organization 
            ORDER BY paper_count DESC 
            LIMIT 10
            """,
            "Top organizations by number of papers"
        )
        
        # Query 7: Papers by document type
        run_query(
            connection,
            """
            SELECT doctype, COUNT(DISTINCT uid) as count 
            FROM item_doc_types 
            WHERE doctype IS NOT NULL
            GROUP BY doctype 
            ORDER BY count DESC
            """,
            "Papers by document type"
        )
        
        # Query 8: Top research subjects
        run_query(
            connection,
            """
            SELECT subject, COUNT(DISTINCT uid) as paper_count 
            FROM item_subjects 
            WHERE subject IS NOT NULL
            GROUP BY subject 
            ORDER BY paper_count DESC 
            LIMIT 10
            """,
            "Top research subjects"
        )
        
        # Query 9: Papers with grants
        run_query(
            connection,
            """
            SELECT COUNT(DISTINCT uid) as papers_with_grants 
            FROM item_grants
            """,
            "Total papers with grant funding"
        )
        
        # Query 10: Top grant agencies
        run_query(
            connection,
            """
            SELECT grant_agency, COUNT(DISTINCT uid) as paper_count 
            FROM item_grants 
            WHERE grant_agency IS NOT NULL
            GROUP BY grant_agency 
            ORDER BY paper_count DESC 
            LIMIT 10
            """,
            "Top grant agencies"
        )
        
        # Query 11: Sample paper with full details
        run_query(
            connection,
            """
            SELECT 
                i.uid,
                i.pubyear,
                t.title,
                LEFT(a.abstract, 200) as abstract_preview,
                s.source
            FROM item i
            LEFT JOIN item_title t ON i.uid = t.uid
            LEFT JOIN item_abstract a ON i.uid = a.uid
            LEFT JOIN item_source s ON i.uid = s.uid
            WHERE t.title IS NOT NULL
            LIMIT 5
            """,
            "Sample papers with basic information"
        )
        
        # Query 12: Authors with ORCID
        run_query(
            connection,
            """
            SELECT COUNT(DISTINCT uid) as papers_with_orcid_authors 
            FROM item_author_ids 
            WHERE orcid IS NOT NULL
            """,
            "Papers with authors having ORCID"
        )
        
        # Query 13: Open Access papers
        run_query(
            connection,
            """
            SELECT oa_type, COUNT(DISTINCT uid) as count 
            FROM item_oas 
            WHERE oa_type IS NOT NULL
            GROUP BY oa_type
            """,
            "Papers by Open Access type"
        )
        
        # Query 14: Citation patterns
        run_query(
            connection,
            """
            SELECT COUNT(*) as total_citations 
            FROM item_references 
            WHERE cited_uid IS NOT NULL
            """,
            "Total citations within WOS database"
        )
        
        # Query 15: Papers with conferences
        run_query(
            connection,
            """
            SELECT COUNT(DISTINCT uid) as conference_papers 
            FROM item_conferences
            """,
            "Total conference papers"
        )
        
        print("\n" + "="*70)
        print("All example queries completed!")
        print("="*70)
        print("\nTip: Modify these queries or create your own to explore the data.")
        print("See MYSQL_IMPORT_GUIDE.md for more query examples and tips.")
        
        return 0
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        connection.close()


if __name__ == '__main__':
    sys.exit(main())
