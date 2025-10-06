"""
Initialize database
"""

from app.db.base import Base
from app.db.session import engine
from app.models import CalculationHistory


def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    print("🔧 Initializing database...")
    init_db()
