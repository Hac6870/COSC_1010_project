from database import Database
from datetime import datetime

class InventoryManager:
    def __init__(self, db=None):
        """Initialize the inventory manager"""
        self.db = db if db else Database()
    
    def get_all_machines(self):
        """Get list of all vending machines"""
        query = """
        SELECT vm.id, vm.name, b.name as building, vm.location_description, vm.last_maintenance_date
        FROM vending_machines vm
        JOIN buildings b ON vm.building_id = b.id
        """
        return self.db.execute_query(query)
    
    def get_machine_inventory(self, machine_id):
        """Get inventory for a specific machine"""
        query = """
        SELECT p.id, p.name, p.price, i.quantity, i.last_restock_date
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        WHERE i.machine_id = ?
        """
        return self.db.execute_query(query, (machine_id,))
    
    def update_inventory(self, machine_id, product_id, new_quantity):
        """Update product quantity in machine"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        query = """
        UPDATE inventory
        SET quantity = ?, last_restock_date = ?
        WHERE machine_id = ? AND product_id = ?
        """
        self.db.execute_insert(query, (new_quantity, current_date, machine_id, product_id))
        print(f"Updated product {product_id} in machine {machine_id} to quantity {new_quantity}")
    
    def get_low_stock_items(self, threshold=5):
        """Get items that are below threshold quantity"""
        query = """
        SELECT vm.name as machine, b.name as building, p.name as product, i.quantity
        FROM inventory i
        JOIN vending_machines vm ON i.machine_id = vm.id
        JOIN buildings b ON vm.building_id = b.id
        JOIN products p ON i.product_id = p.id
        WHERE i.quantity <= ?
        ORDER BY i.quantity ASC
        """
        return self.db.execute_query(query, (threshold,))
    
    def add_new_product(self, name, price, category):
        """Add a new product to the database"""
        query = """
        INSERT INTO products (name, price, category)
        VALUES (?, ?, ?)
        """
        product_id = self.db.execute_insert(query, (name, price, category))
        print(f"Added new product: {name} (ID: {product_id})")
        return product_id
    
    def add_product_to_machine(self, machine_id, product_id, quantity):
        """Add a product to a machine's inventory"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        query = """
        INSERT INTO inventory (machine_id, product_id, quantity, last_restock_date)
        VALUES (?, ?, ?, ?)
        """
        inventory_id = self.db.execute_insert(query, (machine_id, product_id, quantity, current_date))
        print(f"Added product {product_id} to machine {machine_id} with quantity {quantity}")
        return inventory_id
    