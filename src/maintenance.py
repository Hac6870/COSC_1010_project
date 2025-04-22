from database import Database
from datetime import datetime

class MaintenanceManager:
    def __init__(self, db=None):
        """Initialize the maintenance manager"""
        self.db = db if db else Database()
    
    def get_maintenance_history(self, machine_id=None):
        """Get maintenance history for all or specific machine"""
        query = """
        SELECT m.id, vm.name as machine, m.maintenance_date, m.description, m.performed_by
        FROM maintenance_records m
        JOIN vending_machines vm ON m.machine_id = vm.id
        """
        
        if machine_id:
            query += " WHERE m.machine_id = ?"
            return self.db.execute_query(query, (machine_id,))
        else:
            query += " ORDER BY m.maintenance_date DESC"
            return self.db.execute_query(query)
    
    def add_maintenance_record(self, machine_id, description, performed_by):
        """Add a new maintenance record"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        query = """
        INSERT INTO maintenance_records (machine_id, maintenance_date, description, performed_by)
        VALUES (?, ?, ?, ?)
        """
        record_id = self.db.execute_insert(query, (machine_id, current_date, description, performed_by))
        
        # Update the last maintenance date in the vending machine record
        update_query = """
        UPDATE vending_machines
        SET last_maintenance_date = ?
        WHERE id = ?
        """
        self.db.execute_insert(update_query, (current_date, machine_id))
        
        print(f"Added maintenance record for machine {machine_id}")
        return record_id
    
    def get_machines_due_maintenance(self, days=30):
        """Get machines that haven't had maintenance in specified days"""
        query = """
        SELECT vm.id, vm.name, b.name as building, vm.location_description, vm.last_maintenance_date,
        JULIANDAY('now') - JULIANDAY(vm.last_maintenance_date) as days_since_maintenance
        FROM vending_machines vm
        JOIN buildings b ON vm.building_id = b.id
        WHERE JULIANDAY('now') - JULIANDAY(vm.last_maintenance_date) >= ?
        ORDER BY days_since_maintenance DESC
        """
        return self.db.execute_query(query, (days,))
    
    def schedule_maintenance(self, machine_ids, maintenance_date, description='Scheduled maintenance'):
        """Schedule maintenance for machines"""
        # In a real application, this might connect to a calendar system
        # For now, we'll just print the schedule
        for machine_id in machine_ids:
            machine_name = self.db.execute_query("SELECT name FROM vending_machines WHERE id = ?", (machine_id,))[0][0]
            print(f"Scheduled maintenance for {machine_name} on {maintenance_date}: {description}")
            