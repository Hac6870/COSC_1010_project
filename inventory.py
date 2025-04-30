from .json_database import JsonDatabase as Database
from datetime import datetime

class InventoryManager:
    def __init__(self, db=None):
        """Initialize the inventory manager"""
        self.db = db if db else Database()
    
    def get_all_machines(self):
        """Get list of all vending machines"""
        machines = self.db.execute_query("vending_machines")
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        result = []
        for m in machines:
            building_name = buildings.get(m['building_id'], {}).get('name', '')
            result.append((m['id'], m['name'], building_name, m['location_description'], m['last_maintenance_date']))
        return result
    
    def get_machine_inventory(self, machine_id):
        """Get inventory for a specific machine"""
        inventory = [i for i in self.db.execute_query("inventory") if i['machine_id'] == machine_id]
        products = {p['id']: p for p in self.db.execute_query("products")}
        result = []
        for item in inventory:
            product = products.get(item['product_id'])
            if product:
                result.append((product['id'], product['name'], product['price'], item['quantity'], item['last_restock_date']))
        return result
    
    def update_inventory(self, machine_id, product_id, new_quantity):
        """Update product quantity in machine"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        for item in self.db.execute_query("inventory"):
            if item['machine_id'] == machine_id and item['product_id'] == product_id:
                self.db.execute_update("inventory", item['id'], {"quantity": new_quantity, "last_restock_date": current_date})
                print(f"Updated product {product_id} in machine {machine_id} to quantity {new_quantity}")
                return
        print("Inventory item not found.")
    
    def get_low_stock_items(self, threshold=5):
        """Get items that are below threshold quantity"""
        inventory = self.db.execute_query("inventory")
        products = {p['id']: p for p in self.db.execute_query("products")}
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        
        low_stock = []
        for item in inventory:
            if item['quantity'] <= threshold:
                machine = machines.get(item['machine_id'], {})
                building = buildings.get(machine.get('building_id'))
                product = products.get(item['product_id'])
                if machine and building and product:
                    low_stock.append((machine['name'], building['name'], product['name'], item['quantity']))
        return low_stock
    
    def add_new_product(self, name, price, category):
        """Add a new product to the database"""
        product_id = self.db.execute_insert("products", {
            "name": name,
            "price": price,
            "category": category
        })
        print(f"Added new product: {name} (ID: {product_id})")
        return product_id
    
    def add_product_to_machine(self, machine_id, product_id, quantity):
        """Add a product to a machine's inventory"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        inventory_id = self.db.execute_insert("inventory", {
            "machine_id": machine_id,
            "product_id": product_id,
            "quantity": quantity,
            "last_restock_date": current_date
        })
        print(f"Added product {product_id} to machine {machine_id} with quantity {quantity}")
        return inventory_id
