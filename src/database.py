from sqlalchemy import create_engine, text
import os

# Create a persistent SQLite database file instead of in-memory
DB_PATH = "sqlite:///chatbot.db"

def get_sample_data(engine):
    """Get sample data from all tables."""
    sample_data = {}
    tables = ['customers', 'products', 'orders', 'order_items']
    
    for table in tables:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            columns = result.keys()
            rows = result.fetchall()
            sample_data[table] = {
                'columns': columns,
                'rows': rows
            }
    
    return sample_data

def initialize_database():
    """Initialize the SQLite database with schema and sample data."""
    # Create a persistent SQLite database
    engine = create_engine(DB_PATH, echo=True)
    
    # Check if tables exist
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"))
        if not result.fetchone():
            # Create tables and insert data
            with engine.begin() as conn:
                # Create tables
                conn.execute(text("""
                    CREATE TABLE customers (
                        customer_id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT
                    );
                """))

                conn.execute(text("""
                    CREATE TABLE products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT,
                        price FLOAT
                    );
                """))

                conn.execute(text("""
                    CREATE TABLE orders (
                        order_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        order_date TEXT,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    );
                """))

                conn.execute(text("""
                    CREATE TABLE order_items (
                        item_id INTEGER PRIMARY KEY,
                        order_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                    );
                """))

                # Insert sample data
                conn.execute(text("""
                    INSERT INTO customers VALUES
                    (1, 'Alice', 'alice@example.com'),
                    (2, 'Bob', 'bob@example.com');
                """))

                conn.execute(text("""
                    INSERT INTO products VALUES
                    (1, 'Laptop', 1000.0),
                    (2, 'Mouse', 25.0),
                    (3, 'Keyboard', 45.0);
                """))

                conn.execute(text("""
                    INSERT INTO orders VALUES
                    (101, 1, '2024-01-10'),
                    (102, 2, '2024-02-15');
                """))

                conn.execute(text("""
                    INSERT INTO order_items VALUES
                    (1, 101, 1, 1),
                    (2, 101, 2, 2),
                    (3, 102, 2, 1),
                    (4, 102, 3, 1);
                """))
    
    return engine

def execute_query(engine, query):
    """Execute a SQL query and return the results."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall()
    except Exception as e:
        return f"Error executing query: {str(e)}" 