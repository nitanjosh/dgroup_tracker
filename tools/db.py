import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set. Please set it in your .env or Streamlit Secrets.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Connection test
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Database connected successfully!")
except Exception as e:
    print("Database connection failed:", e)

# Authentication function
def verify_admin(username, password):
    """Verify admin credentials from database"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT * FROM admin 
                WHERE username = :username AND password = :password
            """)
            result = conn.execute(query, {"username": username, "password": password})
            return result.fetchone() is not None
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

# Dgroup functions
def insert_dgroup_record(first_name, last_name, dgroup_type, upline_meet=None, 
                        downline_meet=None, leader_name=None):
    """Insert a new dgroup record"""
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO dgroup 
                (first_name, last_name, dgroup_type, dgroup_leader, downline_recent_meet, upline_recent_meet)
                VALUES (:first_name, :last_name, :dgroup_type, :dgroup_leader, :downline_recent_meet, :upline_recent_meet)
            """)
            conn.execute(query, {
                "first_name": first_name,
                "last_name": last_name,
                "dgroup_type": dgroup_type,
                "dgroup_leader": leader_name,
                "downline_recent_meet": downline_meet,
                "upline_recent_meet": upline_meet
            })
            conn.commit()
            return True
    except Exception as e:
        print(f"Insert error: {e}")
        return False

def get_all_dgroup_records():
    """Retrieve all dgroup records"""
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM dgroup ORDER BY id DESC")
            result = conn.execute(query)
            return result.fetchall()
    except Exception as e:
        print(f"Query error: {e}")
        return []