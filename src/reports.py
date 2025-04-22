# Ensure required packages are installed by running the following command in your terminal:
# pip install pandas matplotlib
from database import Database
import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self, db=None):
        """Initialize the report generator"""
        self.db = db if db else Database()
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
    
    def generate_inventory_report(self, export_csv=False):
        """Generate inventory report for all machines"""
        query = """
        SELECT vm.name as machine, b.name as building, p.name as product, 
               p.category, i.quantity, i.last_restock_date
        FROM inventory i
        JOIN vending_machines vm ON i.machine_id = vm.id
        JOIN buildings b ON vm.building_id = b.id
        JOIN products p ON i.product_id = p.id
        ORDER BY b.name, vm.name, p.category, p.name
        """
        data = self.db.execute_query(query)
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Product', 'Category', 'Quantity', 'Last Restock'])
        
        print("\n=== Inventory Report ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/inventory_report.csv', index=False)
            print("Report exported to reports/inventory_report.csv")
        
        return df
    
    def generate_maintenance_report(self, export_csv=False):
        """Generate maintenance report"""
        query = """
        SELECT vm.name as machine, b.name as building, m.maintenance_date,
               m.description, m.performed_by
        FROM maintenance_records m
        JOIN vending_machines vm ON m.machine_id = vm.id
        JOIN buildings b ON vm.building_id = b.id
        ORDER BY m.maintenance_date DESC
        """
        data = self.db.execute_query(query)
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Date', 'Description', 'Performed By'])
        
        print("\n=== Maintenance Report ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/maintenance_report.csv', index=False)
            print("Report exported to reports/maintenance_report.csv")
        
        return df
    
    def generate_low_stock_report(self, threshold=5, export_csv=False):
        """Generate report of low stock items"""
        query = """
        SELECT vm.name as machine, b.name as building, p.name as product, 
               p.category, i.quantity, i.last_restock_date
        FROM inventory i
        JOIN vending_machines vm ON i.machine_id = vm.id
        JOIN buildings b ON vm.building_id = b.id
        JOIN products p ON i.product_id = p.id
        WHERE i.quantity <= ?
        ORDER BY i.quantity ASC
        """
        data = self.db.execute_query(query, (threshold,))
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Machine', 'Building', 'Product', 'Category', 'Quantity', 'Last Restock'])
        
        print(f"\n=== Low Stock Report (Threshold: {threshold}) ===")
        print(df)
        
        if export_csv:
            df.to_csv('reports/low_stock_report.csv', index=False)
            print("Report exported to reports/low_stock_report.csv")
        
        return df
    
    def visualize_inventory_by_machine(self):
        """Create a bar chart of product counts by machine"""
        query = """
        SELECT vm.name as machine, SUM(i.quantity) as total_items
        FROM inventory i
        JOIN vending_machines vm ON i.machine_id = vm.id
        GROUP BY vm.name
        ORDER BY total_items DESC
        """
        data = self.db.execute_query(query)
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Machine', 'Total Items'])
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(df['Machine'], df['Total Items'], color='skyblue')
        plt.title('Total Inventory by Machine')
        plt.xlabel('Machine')
        plt.ylabel('Number of Items')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the chart
        plt.savefig('reports/inventory_by_machine.png')
        print("Chart saved to reports/inventory_by_machine.png")
        
        # Display the chart in interactive mode
        plt.show()
    
    def visualize_product_distribution(self):
        """Create a pie chart of product category distribution"""
        query = """
        SELECT p.category, SUM(i.quantity) as total_quantity
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        GROUP BY p.category
        """
        data = self.db.execute_query(query)
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Category', 'Quantity'])
        
        # Create pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(df['Quantity'], labels=df['Category'], autopct='%1.1f%%', startangle=90, shadow=True)
        plt.title('Product Distribution by Category')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Save the chart
        plt.savefig('reports/product_distribution.png')
        print("Chart saved to reports/product_distribution.png")
        
        # Display the chart in interactive mode
        plt.show()
