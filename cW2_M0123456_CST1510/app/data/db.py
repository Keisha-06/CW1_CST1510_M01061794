import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

#Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

#Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")

import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(db_path))

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table
        
    Returns:
        int: Number of rows loaded
    """

    csv_path = Path(csv_path)

    #Check if CSV file exists.
    if not csv_path.exists():
        print(f"File nt found: {csv_path}")
        return 0
    
    #Read CSV using pandas.read_csv()
    df = pd.read_csv(csv_path)

    #Use df.to_sql() to insert data
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    #Print success message and return row count
    print(f"Loaded {len(df)} rows into '{table_name}' from {csv_path.name}")
    return len(df)
