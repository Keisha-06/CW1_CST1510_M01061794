def create_users_table(conn):
    """Create users table if it doesn't exist """

    cursor = conn.cursor()

     # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Users table created successfully!")
    

def create_cyber_incidents_table(conn):
    """Create cyber incidents table if it doesn't exist"""

    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date: TEXT 
        incident_type: TEXT 
        severity: TEXT 
        status: TEXT 
        description: TEXT
        reported_by: TEXT 
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Cyber Incidents table created successfully!")

def create_datasets_metadata_table(conn):
    """Create the datasets_metadata table if it doesn't exist"""

    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name: TEXT NOT NULL,
        category: TEXT (e.g., 'Threat Intelligence', 'Network Logs'),
        source: TEXT (origin of the dataset),
        last_updated: TEXT (format: YYYY-MM-DD),
        record_count: INTEGER,
        file_size_mb: REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Datasets metadata table created successfully!")

def create_it_tickets_table(conn):
    """Create the it_tickets table."""

    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id: INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id: TEXT UNIQUE NOT NULL,
        priority: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low'),
        status: TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed'),
        category: TEXT (e.g., 'Hardware', 'Software', 'Network'),
        subject: TEXT NOT NULL,
        description: TEXT,
        reated_date: TEXT (format: YYYY-MM-DD),
        resolved_date: TEXT,
        assigned_to: TEXT,
        created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ It tickets table created successfully!")
   

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

print("All tables created successfully!)")

   