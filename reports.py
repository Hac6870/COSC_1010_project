# Ensure required packages are installed by running the following command in your terminal:
# pip install pandas matplotlib
from .json_database import JsonDatabase as Database
import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self, db=None):
        """Initialize the report generator"""
        self.db = db if db else Database()
        os.makedirs('reports', exist_ok=True)
    
    def generate_inventory_report(self, export_csv=False):
        """Generate inventory report for all machines"""
        inventory = self.db.execute_query("inventory")
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        products = {p['id']: p for p in self.db.execute_query("products")}
        
        data = []
        for item in inventory:
            machine = machines.get(item['machine_id'], {})
            building = buildings.get(machine.get('building_id'), {})
            product = products.get(item['product_id'], {})
            data.append((
                machine.get('name', ''),
                building.get('name', ''),
                product.get('name', ''),
                product.get('category', ''),
                item.get('quantity', 0),
                item.get('last_restock_date', '')
            ))
        
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Product', 'Category', 'Quantity', 'Last Restock'])
        
        print("\n=== Inventory Report ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/inventory_report.csv', index=False)
            print("Report exported to reports/inventory_report.csv")
        
        return df
    
    def generate_maintenance_report(self, export_csv=False):
        """Generate maintenance report"""
        records = self.db.execute_query("maintenance_records")
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        
        data = []
        for r in records:
            machine = machines.get(r['machine_id'], {})
            building = buildings.get(machine.get('building_id'), {})
            data.append((
                machine.get('name', ''),
                building.get('name', ''),
                r['maintenance_date'],
                r['description'],
                r['performed_by']
            ))
        
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Date', 'Description', 'Performed By'])
        
        print("\n=== Maintenance Report ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/maintenance_report.csv', index=False)
            print("Report exported to reports/maintenance_report.csv")
        
        return df
    
    def generate_low_stock_report(self, threshold=5, export_csv=False):
        """Generate report of low stock items"""
        inventory = self.db.execute_query("inventory")
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        products = {p['id']: p for p in self.db.execute_query("products")}
        
        data = []
        for item in inventory:
            if item['quantity'] <= threshold:
                machine = machines.get(item['machine_id'], {})
                building = buildings.get(machine.get('building_id'), {})
                product = products.get(item['product_id'], {})
                data.append((
                    machine.get('name', ''),
                    building.get('name', ''),
                    product.get('name', ''),
                    product.get('category', ''),
                    item['quantity'],
                    item['last_restock_date']
                ))
        
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Product', 'Category', 'Quantity', 'Last Restock'])
        
        print(f"\n=== Low Stock Report (Threshold: {threshold}) ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/low_stock_report.csv', index=False)
            print("Report exported to reports/low_stock_report.csv")
        
        return df
    
    def visualize_inventory_by_machine(self):
        """Create a bar chart of product counts by machine"""
        inventory = self.db.execute_query("inventory")
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        
        totals = {}
        for item in inventory:
            machine_name = machines.get(item['machine_id'], {}).get('name', 'Unknown Machine')
            totals[machine_name] = totals.get(machine_name, 0) + item['quantity']
        
        df = pd.DataFrame(list(totals.items()), columns=['Machine', 'Total Items'])
        
        plt.figure(figsize=(10, 6))
        plt.bar(df['Machine'], df['Total Items'], color='skyblue')
        plt.title('Total Inventory by Machine')
        plt.xlabel('Machine')
        plt.ylabel('Number of Items')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig('reports/inventory_by_machine.png')
        print("Chart saved to reports/inventory_by_machine.png")
        plt.show()
    
    def visualize_product_distribution(self):
        """Create a pie chart of product category distribution"""
        inventory = self.db.execute_query("inventory")
        products = {p['id']: p for p in self.db.execute_query("products")}
        
        totals = {}
        for item in inventory:
            product = products.get(item['product_id'], {})
            category = product.get('category', 'Other')
            totals[category] = totals.get(category, 0) + item['quantity']
        
        df = pd.DataFrame(list(totals.items()), columns=['Category', 'Quantity'])
        
        plt.figure(figsize=(8, 8))
        plt.pie(df['Quantity'], labels=df['Category'], autopct='%1.1f%%', startangle=90, shadow=True)
        plt.title('Product Distribution by Category')
        plt.axis('equal')
        
        plt.savefig('reports/product_distribution.png')
        print("Chart saved to reports/product_distribution.png")
        plt.show()
