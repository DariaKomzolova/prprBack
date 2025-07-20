from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./electives.db", connect_args={"check_same_thread": False})

with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL;"))

print("✅ WAL mode enabled")
