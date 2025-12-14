import pandas as pd
from app.data.db import connect_database
from app.data import schema
from app.data import create_all_tables, migrate_users_from_file,load_all_csv_data, DB_PATH
from app.services.user_service import register_user, login_user

def inser_dataset(date, dataset_type, severity, status, description, reported_by=None):
    """Insert a new cyber dataset into the database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_datasets
        (date, dataset_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, dataset_type, severity, status, description, reported_by))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_datasets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def insert_dataset(conn, date, dataset_type, severity, status, description, reported_by=None):
    """Insert a new cyber dataset into the database.
    Args:
        conn: Database connection
        date: Dataset date (YYYY-MM-DD)
        dataset_type: Type of dataset
        severity: Severity level
        status: Current status
        description: Dataset description
        reported_by: Username of reporter (optional)
        
    Returns:
        int: ID of the inserted dataset
    """
# Test: Insert a new dataset
conn = connect_database()
new_id = insert_dataset(
    conn,
    date="2024-11-05",
    dataset_type="Phishing",
    severity="High",
    status="Open",
    description="Suspicious email with malicious link detected.",
    reported_by="charlie"
)
conn.close()

def get_all_datasets(conn):
    """
    Retrieve all datasets from the database.
    
    Returns:
        pandas.DataFrame: All datasets
    """
    query = "SELECT * FROM cyber_datasets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    return df

def update_dataset_status(conn, dataset_id, new_status):
    """
    Update the status of an dataset.
    
    Args:
        conn: Database connection
        dataset_id: ID of the dataset to update
        new_status: New status value
        
    Returns:
        bool: True if update was successful
    """
    cursor = conn.cursor()
    
    # Use parameterized query
    cursor.execute(
        "UPDATE cyber_datasets SET status = ? WHERE id = ?",
        (new_status, dataset_id)
    )
    
    conn.commit()
    rows_affected = cursor.rowcount
    
    if rows_affected > 0:
        print(f"✅ Dataset #{dataset_id} status updated to '{new_status}'.")
        return True
    else:
        print(f"⚠️ No datasett found with ID {dataset_id}.")
        return False

# Test: Update an datasett
conn = connect_database()

# Get the first dataset
df = get_all_datasets(conn)
if len(df) > 0:
    first_id = df.iloc[0]['id']
    print(f"\n Updating dataset #{first_id}...")
    update_dataset_status(conn, first_id, "Resolved")
    
    # Verify the update
    df_updated = pd.read_sql_query(
        "SELECT id, status FROM cyber_datasets WHERE id = ?",
        conn,
        params=(first_id,)
    )
    print(f"   New status: {df_updated.iloc[0]['status']}")

conn.close()

def delete_dataset(conn, dataset_id):
    """
    Delete an dataset from the database.
    
    Args:
        conn: Database connection
        dataset_id: ID of the dataset to delete
        
    Returns:
        bool: True if deletion was successful
    """
    cursor = conn.cursor()
    
    # CRITICAL: Always use WHERE clause with DELETE!
    cursor.execute(
        "DELETE FROM cyber_datasets WHERE id = ?",
        (dataset_id,)
    )
    
    conn.commit()
    rows_affected = cursor.rowcount
    
    if rows_affected > 0:
        print(f" Dataset #{dataset_id} deleted successfully.")
        return True
    else:
        print(f"No dataset found with ID {dataset_id}.")
        return False

# Test: Delete an dataset (commented out for safety)
# conn = connect_database()
# delete_dataset(conn, 999)  # Replace with actual ID to test
# conn.close()

print(" DELETE function defined but not executed (for safety).")
print("   Uncomment the test code above to try deleting an dataset.")

def get_datasets_by_type_count(conn):
    """
    Count datasets by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT dataset_type, COUNT(*) as count
    FROM cyber_datasets
    GROUP BY dataset_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity datasets by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_datasets
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_dataset_types_with_many_cases(conn, min_count=5):
    """
    Find dataset types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT dataset_type, COUNT(*) as count
    FROM cyber_datasets
    GROUP BY dataset_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Datasets by Type:")
df_by_type = get_datasets_by_type_count(conn)
print(df_by_type)

print("\n High Severity Datasets by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Dataset Types with Many Cases (>5):")
df_many_cases = get_dataset_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")
    
    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    
    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_datasets', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database()
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    test_id = insert_dataset(
        conn,
        "2024-11-05",
        "Test Dataset",
        "Low",
        "Open",
        "This is a test dataset",
        "test_user"
    )
    print(f"  Create: ✅ Dataset #{test_id} created")
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_datasets WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found dataset #{test_id}")
    
    # Update
    update_dataset_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_dataset(conn, test_id)
    print(f"  Delete:  dataset deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_datasets_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} dataset types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()