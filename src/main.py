from database import Database
from inventory import InventoryManager
from maintenance import MaintenanceManager
from reports import ReportGenerator
import os

class VendingMachineSystem:
    def __init__(self):
        """Initialize the system"""
        self.db = Database()
        self.inventory = InventoryManager(self.db)
        self.maintenance = MaintenanceManager(self.db)
        self.reports = ReportGenerator(self.db)
    
    def display_menu(self):
        """Display main menu"""
        print("\n=== Vending Machine Inventory Management System ===")
        print("1. View All Machines")
        print("2. View Machine Inventory")
        print("3. Update Product Quantity")
        print("4. View Low Stock Items")
        print("5. Add Maintenance Record")
        print("6. View Maintenance History")
        print("7. Generate Inventory Report")
        print("8. Generate Maintenance Report")
        print("9. Generate Low Stock Report")
        print("10. Visualize Inventory")
        print("0. Exit")
        return input("Enter your choice: ")
    
    def view_all_machines(self):
        """Display all vending machines"""
        machines = self.inventory.get_all_machines()
        print("\n=== All Vending Machines ===")
        print("ID | Machine Name | Building | Location | Last Maintenance")
        print("-" * 70)
        for machine in machines:
            print(f"{machine[0]} | {machine[1]} | {machine[2]} | {machine[3]} | {machine[4]}")
    
    def view_machine_inventory(self):
        """View inventory for a specific machine"""
        self.view_all_machines()
        machine_id = input("\nEnter machine ID to view inventory: ")
        try:
            machine_id = int(machine_id)
            inventory = self.inventory.get_machine_inventory(machine_id)
            
            if not inventory:
                print("No inventory found for this machine or invalid machine ID.")
                return
                
            print(f"\n=== Inventory for Machine ID: {machine_id} ===")
            print("ID | Product Name | Price | Quantity | Last Restock")
            print("-" * 60)
            for item in inventory:
                print(f"{item[0]} | {item[1]} | ${item[2]:.2f} | {item[3]} | {item[4]}")
        except ValueError:
            print("Invalid input. Please enter a valid machine ID.")
    
    def update_product_quantity(self):
        """Update product quantity in a machine"""
        self.view_all_machines()
        machine_id = input("\nEnter machine ID: ")
        
        try:
            machine_id = int(machine_id)
            inventory = self.inventory.get_machine_inventory(machine_id)
            
            if not inventory:
                print("No inventory found for this machine or invalid machine ID.")
                return
            
            print(f"\n=== Inventory for Machine ID: {machine_id} ===")
            print("ID | Product Name | Price | Quantity | Last Restock")
            print("-" * 60)
            for item in inventory:
                print(f"{item[0]} | {item[1]} | ${item[2]:.2f} | {item[3]} | {item[4]}")
                
            product_id = input("\nEnter product ID to update: ")
            try:
                product_id = int(product_id)
                # Check if product exists in this machine
                product_exists = False
                for item in inventory:
                    if item[0] == product_id:
                        product_exists = True
                        break
                
                if not product_exists:
                    print("Product not found in this machine.")
                    return
                
                new_quantity = input("Enter new quantity: ")
                try:
                    new_quantity = int(new_quantity)
                    if new_quantity < 0:
                        print("Quantity cannot be negative.")
                        return
                    
                    self.inventory.update_inventory(machine_id, product_id, new_quantity)
                    print("Inventory updated successfully!")
                except ValueError:
                    print("Invalid input. Please enter a valid quantity.")
            except ValueError:
                print("Invalid input. Please enter a valid product ID.")
        except ValueError:
            print("Invalid input. Please enter a valid machine ID.")
    
    def view_low_stock_items(self):
        """View items with low stock"""
        threshold = input("Enter quantity threshold (default: 5): ")
        try:
            threshold = int(threshold) if threshold else 5
            low_stock = self.inventory.get_low_stock_items(threshold)
            
            if not low_stock:
                print(f"No items below threshold of {threshold} found.")
                return
                
            print(f"\n=== Low Stock Items (Threshold: {threshold}) ===")
            print("Machine | Building | Product | Quantity")
            print("-" * 60)
            for item in low_stock:
                print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]}")
        except ValueError:
            print("Invalid input. Please enter a valid threshold.")
    
    def add_maintenance_record(self):
        """Add a new maintenance record"""
        self.view_all_machines()
        machine_id = input("\nEnter machine ID for maintenance: ")
        
        try:
            machine_id = int(machine_id)
            # Check if machine exists
            machines = self.inventory.get_all_machines()
            machine_exists = False
            for machine in machines:
                if machine[0] == machine_id:
                    machine_exists = True
                    break
            
            if not machine_exists:
                print("Invalid machine ID.")
                return
            
            description = input("Enter maintenance description: ")
            performed_by = input("Enter name of person performing maintenance: ")
            
            self.maintenance.add_maintenance_record(machine_id, description, performed_by)
            print("Maintenance record added successfully!")
        except ValueError:
            print("Invalid input. Please enter a valid machine ID.")
    
    def view_maintenance_history(self):
        """View maintenance history"""
        print("\n1. View history for all machines")
        print("2. View history for specific machine")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            history = self.maintenance.get_maintenance_history()
            print("\n=== Maintenance History (All Machines) ===")
            print("ID | Machine | Date | Description | Performed By")
            print("-" * 70)
            for record in history:
                print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")
        elif choice == '2':
            self.view_all_machines()
            machine_id = input("\nEnter machine ID: ")
            try:
                machine_id = int(machine_id)
                history = self.maintenance.get_maintenance_history(machine_id)
                
                if not history:
                    print("No maintenance history found for this machine or invalid machine ID.")
                    return
                    
                print(f"\n=== Maintenance History for Machine ID: {machine_id} ===")
                print("ID | Machine | Date | Description | Performed By")
                print("-" * 70)
                for record in history:
                    print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")
            except ValueError:
                print("Invalid input. Please enter a valid machine ID.")
        else:
            print("Invalid choice.")
    
    def generate_inventory_report(self):
        """Generate inventory report"""
        export = input("Export to CSV file? (y/n): ").lower() == 'y'
        self.reports.generate_inventory_report(export)
    
    def generate_maintenance_report(self):
        """Generate maintenance report"""
        export = input("Export to CSV file? (y/n): ").lower() == 'y'
        self.reports.generate_maintenance_report(export)
    
    def generate_low_stock_report(self):
        """Generate low stock report"""
        threshold = input("Enter quantity threshold (default: 5): ")
        try:
            threshold = int(threshold) if threshold else 5
            export = input("Export to CSV file? (y/n): ").lower() == 'y'
            self.reports.generate_low_stock_report(threshold, export)
        except ValueError:
            print("Invalid input. Please enter a valid threshold.")
    
    def visualize_inventory(self):
        """Visualize inventory data"""
        print("\n1. Inventory by Machine (Bar Chart)")
        print("2. Product Distribution by Category (Pie Chart)")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            self.reports.visualize_inventory_by_machine()
        elif choice == '2':
            self.reports.visualize_product_distribution()
        else:
            print("Invalid choice.")
    
    def run(self):
        """Run the main application loop"""
        while True:
            choice = self.display_menu()
            
            if choice == '0':
                print("Exiting system. Goodbye!")
                self.db.close()
                break
            elif choice == '1':
                self.view_all_machines()
            elif choice == '2':
                self.view_machine_inventory()
            elif choice == '3':
                self.update_product_quantity()
            elif choice == '4':
                self.view_low_stock_items()
            elif choice == '5':
                self.add_maintenance_record()
            elif choice == '6':
                self.view_maintenance_history()
            elif choice == '7':
                self.generate_inventory_report()
            elif choice == '8':
                self.generate_maintenance_report()
            elif choice == '9':
                self.generate_low_stock_report()
            elif choice == '10':
                self.visualize_inventory()
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    system = VendingMachineSystem()
    system.run()
    