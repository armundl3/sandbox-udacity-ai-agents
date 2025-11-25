"""
Setup script to populate the sales.db database with sample Dell laptop sales data.
"""

import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from pathlib import Path

# Configuration
DB_PATH = Path(__file__).parent.parent / "nb" / "sales.db"
NUM_RECORDS = 120

# Dell laptop models
MODELS = [
    "Dell XPS 13",
    "Dell XPS 15",
    "Dell Inspiron 14",
    "Dell Inspiron 15",
    "Dell Latitude 7310",
    "Dell Latitude 7410",
    "Dell G5 15",
]

# Price ranges for each model (min, max)
PRICE_RANGES = {
    "Dell XPS 13": (1200, 2500),
    "Dell XPS 15": (1400, 2800),
    "Dell Inspiron 14": (600, 1500),
    "Dell Inspiron 15": (700, 2400),
    "Dell Latitude 7310": (1000, 2000),
    "Dell Latitude 7410": (1100, 2100),
    "Dell G5 15": (800, 1800),
}


def generate_random_date():
    """Generate a random date in 2024."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


def generate_sales_data(num_records):
    """Generate random sales data."""
    sales_data = []
    for i in range(1, num_records + 1):
        model = random.choice(MODELS)
        min_price, max_price = PRICE_RANGES[model]

        record = {
            "id": i,
            "transaction_date": generate_random_date(),
            "model": model,
            "price": round(random.uniform(min_price, max_price), 2),
            "quantity": random.randint(1, 4),
            "customer_id": random.randint(1000, 1100),
        }
        sales_data.append(record)

    return sales_data


def setup_database():
    """Create and populate the sales database."""
    print(f"Setting up database at: {DB_PATH}")

    # Create database engine
    engine = create_engine(f"sqlite:///{DB_PATH}")

    with engine.begin() as connection:
        # Drop existing table
        print("Dropping existing 'sales' table if it exists...")
        connection.execute(text("DROP TABLE IF EXISTS sales"))

        # Create sales table
        print("Creating 'sales' table...")
        connection.execute(text("""
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                transaction_date DATE NOT NULL,
                model VARCHAR(50) NOT NULL,
                price FLOAT NOT NULL,
                quantity INTEGER,
                customer_id INTEGER
            )
        """))

        # Generate and insert data
        print(f"Generating {NUM_RECORDS} sales records...")
        sales_data = generate_sales_data(NUM_RECORDS)

        print("Inserting data into database...")
        for record in sales_data:
            connection.execute(
                text("""
                    INSERT INTO sales (id, transaction_date, model, price, quantity, customer_id)
                    VALUES (:id, :transaction_date, :model, :price, :quantity, :customer_id)
                """),
                record
            )

        # Verify insertion
        result = connection.execute(text("SELECT COUNT(*) FROM sales"))
        count = result.scalar()
        print(f"\n✓ Successfully inserted {count} records into the database!")

        # Show sample data
        print("\nSample data (first 5 rows):")
        result = connection.execute(text("SELECT * FROM sales LIMIT 5"))
        for row in result:
            print(f"  {row}")


if __name__ == "__main__":
    setup_database()
