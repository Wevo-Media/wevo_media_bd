class InsertQuery:
    def __init__(self, table_name, data):
        self.table_name = table_name
        self.data = data

    def build_query(self):
        columns = ', '.join(self.data.keys())
        placeholders = ', '.join(['%s'] * len(self.data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(self.data.values())
        return query, values