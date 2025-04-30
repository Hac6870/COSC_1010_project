import json
import os

class JsonDatabase:
    def __init__(self, json_path='data/vending_data.json'):
        self.json_path = json_path
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        if not os.path.exists(self.json_path):
            self.data = {
                "buildings": [],
                "vending_machines": [],
                "products": [],
                "inventory": [],
                "maintenance_records": []
            }
            self.save()
        else:
            self.load()

    def load(self):
        with open(self.json_path, 'r') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def execute_query(self, table, filter_fn=None):
        records = self.data.get(table, [])
        if filter_fn:
            records = list(filter(filter_fn, records))
        return records

    def execute_insert(self, table, record):
        record['id'] = self._generate_new_id(table)
        self.data[table].append(record)
        self.save()
        return record['id']

    def execute_update(self, table, record_id, update_fields):
        for record in self.data.get(table, []):
            if record['id'] == record_id:
                record.update(update_fields)
                self.save()
                return True
        return False

    def _generate_new_id(self, table):
        existing = self.data.get(table, [])
        if not existing:
            return 1
        return max(item['id'] for item in existing) + 1

    def close(self):
        pass
