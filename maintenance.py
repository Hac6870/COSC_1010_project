from .json_database import JsonDatabase as Database
from datetime import datetime

class MaintenanceManager:
    def __init__(self, db=None):
        """Initialize the maintenance manager"""
        self.db = db if db else Database()
    
    def get_maintenance_history(self, machine_id=None):
        """Get maintenance history for all or specific machine"""
        records = self.db.execute_query("maintenance_records")
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        
        if machine_id:
            records = [r for r in records if r['machine_id'] == machine_id]
        
        result = []
        for r in records:
            machine = machines.get(r['machine_id'], {})
            result.append((r['id'], machine.get('name', ''), r['maintenance_date'], r['description'], r['performed_by']))
        
        # Sort by maintenance date (descending)
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def add_maintenance_record(self, machine_id, description, performed_by):
        """Add a new maintenance record"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Insert maintenance record
        record_id = self.db.execute_insert("maintenance_records", {
            "machine_id": machine_id,
            "maintenance_date": current_date,
            "description": description,
            "performed_by": performed_by
        })
        
        # Update last maintenance date on machine
        machines = self.db.execute_query("vending_machines")
        for machine in machines:
            if machine['id'] == machine_id:
                self.db.execute_update("vending_machines", machine_id, {"last_maintenance_date": current_date})
                break
        
        print(f"Added maintenance record for machine {machine_id}")
        return record_id
    
    def get_machines_due_maintenance(self, days=30):
        """Get machines that haven't had maintenance in specified number of days"""
        machines = self.db.execute_query("vending_machines")
        buildings = {b['id']: b for b in self.db.execute_query("buildings")}
        result = []
        today = datetime.now()
        
        for m in machines:
            if m.get('last_maintenance_date'):
                last_date = datetime.strptime(m['last_maintenance_date'], '%Y-%m-%d')
                diff_days = (today - last_date).days
                if diff_days >= days:
                    building = buildings.get(m['building_id'], {})
                    result.append((
                        m['id'],
                        m['name'],
                        building.get('name', ''),
                        m['location_description'],
                        m['last_maintenance_date'],
                        diff_days
                    ))
        
        # Sort by most overdue
        result.sort(key=lambda x: x[5], reverse=True)
        return result
    
    def schedule_maintenance(self, machine_ids, maintenance_date, description='Scheduled maintenance'):
        """Schedule maintenance for multiple machines"""
        machines = {m['id']: m for m in self.db.execute_query("vending_machines")}
        
        for machine_id in machine_ids:
            machine_name = machines.get(machine_id, {}).get('name', 'Unknown Machine')
            print(f"Scheduled maintenance for {machine_name} on {maintenance_date}: {description}")
