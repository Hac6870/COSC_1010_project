import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='data/vending.db'):
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.initialize_database()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        # Create buildings table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT
        )
        ''')
        
        # Create vending machines table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS vending_machines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            building_id INTEGER,
            location_description TEXT,
            last_maintenance_date TEXT,
            FOREIGN KEY (building_id) REFERENCES buildings (id)
        )
        ''')
        
        # Create products table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
        ''')
        
        # Create inventory table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            machine_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            last_restock_date TEXT,
            FOREIGN KEY (machine_id) REFERENCES vending_machines (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # Create maintenance records table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_records (
            id INTEGER PRIMARY KEY,
            machine_id INTEGER,
            maintenance_date TEXT NOT NULL,
            description TEXT,
            performed_by TEXT,
            FOREIGN KEY (machine_id) REFERENCES vending_machines (id)
        )
        ''')
        
        # Commit changes
        self.conn.commit()
        
        # Add some sample data if tables are empty
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample data if tables are empty"""
        if self.cursor.execute("SELECT COUNT(*) FROM buildings").fetchone()[0] == 0:
            # Add sample buildings
            buildings = [
                (1, 'Science Building', 'North Campus'),
                (2, 'Library', 'Central Campus'),
                (3, 'Student Union', 'South Campus')
            ]
            self.cursor.executemany("INSERT INTO buildings VALUES (?, ?, ?)", buildings)
            
            # Add sample vending machines
            machines = [
                (1, 'Snack Machine 1', 1, '1st Floor Lobby', '2023-10-15'),
                (2, 'Drink Machine 1', 1, '2nd Floor Hallway', '2023-11-20'),
                (3, 'Snack Machine 2', 2, 'Main Entrance', '2023-12-01'),
                (4, 'Drink Machine 2', 3, 'Food Court', '2024-01-05')
            ]
            self.cursor.executemany("INSERT INTO vending_machines VALUES (?, ?, ?, ?, ?)", machines)
            
            # Add sample products
            products = [
                (1, 'Potato Chips', 1.50, 'Snacks'),
                (2, 'Chocolate Bar', 1.25, 'Snacks'),
                (3, 'Cola', 1.75, 'Drinks'),
                (4, 'Water', 1.00, 'Drinks'),
                (5, 'Energy Bar', 2.00, 'Snacks'),
                (6, 'Fruit Juice', 2.25, 'Drinks')
            ]
            self.cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
            
            # Add sample inventory
            inventory = [
                (1, 1, 1, 10, '2024-03-15'),
                (2, 1, 2, 15, '2024-03-15'),
                (3, 2, 3, 20, '2024-03-10'),
                (4, 2, 4, 25, '2024-03-10'),
                (5, 3, 1, 8, '2024-03-12'),
                (6, 3, 5, 12, '2024-03-12'),
                (7, 4, 3, 18, '2024-03-05'),
                (8, 4, 6, 14, '2024-03-05')
            ]
            self.cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory)
            
            # Add sample maintenance records
            maintenance = [
                (1, 1, '2023-10-15', 'Regular maintenance', 'John Doe'),
                (2, 2, '2023-11-20', 'Fixed coin slot', 'Jane Smith'),
                (3, 3, '2023-12-01', 'Regular maintenance', 'John Doe'),
                (4, 4, '2024-01-05', 'Replaced display', 'Jane Smith')
            ]
            self.cursor.executemany("INSERT INTO maintenance_records VALUES (?, ?, ?, ?, ?)", maintenance)
            
            # Commit changes
            self.conn.commit()
    
    def execute_query(self, query, params=()):
        """Execute SQL query and return results"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def execute_insert(self, query, params=()):
        """Execute SQL insert query and commit changes"""
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        