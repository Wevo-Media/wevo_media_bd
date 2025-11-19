class DeleteQuery:
    def __init__(self, table_name, conditions):
        self.table_name = table_name
        self.conditions = conditions

    def build_query(self):
        condition_str = ' AND '.join(f"{key}='{value}'" for key, value in self.conditions.items())
        query = f"DELETE FROM {self.table_name} WHERE {condition_str};"
        return query