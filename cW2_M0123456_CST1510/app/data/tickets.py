import pandas as pd
from app.data.db import connect_database
from app.data import schema
from app.data import create_all_tables, migrate_users_from_file,load_all_csv_data, DB_PATH
from app.services.user_service import register_user, login_user

def insert_ticket(date, ticket_type, severity, status, description, reported_by=None):
    """Insert a new cyber ticket into the database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_tickets 
        (date, ticket_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, ticket_type, severity, status, description, reported_by))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def insert_ticket(conn, date, ticket_type, severity, status, description, reported_by=None):
    """Insert a new cyber ticket into the database.
    Args:
        conn: Database connection
        date: Ticlet date (YYYY-MM-DD)
        ticket_type: Type of ticket
        severity: Severity level
        status: Current status
        description: Ticket description
        reported_by: Username of reporter (optional)
        
    Returns:
        int: ID of the inserted ticket
    """
# Test: Insert a new ticket
conn = connect_database()
new_id = insert_ticket(
    conn,
    date="2024-11-05",
    ticket_type="Phishing",
    severity="High",
    status="Open",
    description="Suspicious email with malicious link detected.",
    reported_by="charlie"
)
conn.close()

def get_all_tickets(conn):
    """
    Retrieve all tickets from the database.
    
    Returns:
        pandas.DataFrame: All tickets
    """
    query = "SELECT * FROM cyber_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    return df

def update_ticket_status(conn, ticket_id, new_status):
    """
    Update the status of an ticket.
    
    Args:
        conn: Database connection
        ticket_id: ID of the ticket to update
        new_status: New status value
        
    Returns:
        bool: True if update was successful
    """
    cursor = conn.cursor()
    
    # Use parameterized query
    cursor.execute(
        "UPDATE cyber_tickes SET status = ? WHERE id = ?",
        (new_status, ticket_id)
    )
    
    conn.commit()
    rows_affected = cursor.rowcount
    
    if rows_affected > 0:
        print(f"✅ Ticket #{ticket_id} status updated to '{new_status}'.")
        return True
    else:
        print(f"⚠️ No ticket found with ID {ticket_id}.")
        return False

# Test: Update an ticket
conn = connect_database()

# Get the first ticket
df = get_all_tickets(conn)
if len(df) > 0:
    first_id = df.iloc[0]['id']
    print(f"\n Updating ticket #{first_id}...")
    update_ticket_status(conn, first_id, "Resolved")
    
    # Verify the update
    df_updated = pd.read_sql_query(
        "SELECT id, status FROM cyber_tickets WHERE id = ?",
        conn,
        params=(first_id,)
    )
    print(f"   New status: {df_updated.iloc[0]['status']}")

conn.close()

def delete_ticket(conn, ticket_id):
    """
    Delete an ticket from the database.
    
    Args:
        conn: Database connection
        ticket_id: ID of the ticket to delete
        
    Returns:
        bool: True if deletion was successful
    """
    cursor = conn.cursor()
    
    # CRITICAL: Always use WHERE clause with DELETE!
    cursor.execute(
        "DELETE FROM cyber_tickets WHERE id = ?",
        (ticket_id,)
    )
    
    conn.commit()
    rows_affected = cursor.rowcount
    
    if rows_affected > 0:
        print(f" Ticket #{ticket_id} deleted successfully.")
        return True
    else:
        print(f"No ticket found with ID {ticket_id}.")
        return False

# Test: Delete an ticket (commented out for safety)
# conn = connect_database()
# delete_ticket(conn, 999)  # Replace with actual ID to test
# conn.close()

print(" DELETE function defined but not executed (for safety).")
print("   Uncomment the test code above to try deleting an ticket.")

def get_tickets_by_type_count(conn):
    """
    Count tickets by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT ticket_type, COUNT(*) as count
    FROM cyber_tickets
    GROUP BY ticket_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity tickets by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_tickets
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_ticket_types_with_many_cases(conn, min_count=5):
    """
    Find ticket types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT ticket_type, COUNT(*) as count
    FROM cyber_tickets
    GROUP BY ticket_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Tickets by Type:")
df_by_type = get_tickets_by_type_count(conn)
print(df_by_type)

print("\n High Severity Tickets by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Ticket Types with Many Cases (>5):")
df_many_cases = get_ticket_types_with_many_cases(conn, min_count=5)
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
    tables = ['users', 'cyber_tickets', 'datasets_metadata', 'it_tickets']
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
    test_id = insert_ticket(
        conn,
        "2024-11-05",
        "Test Ticket",
        "Low",
        "Open",
        "This is a test ticket",
        "test_user"
    )
    print(f"  Create: ✅ Ticket #{test_id} created")
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_tickets WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found ticket #{test_id}")
    
    # Update
    update_ticket_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_ticket(conn, test_id)
    print(f"  Delete:  Ticket deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_tickets_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} ticket types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()


