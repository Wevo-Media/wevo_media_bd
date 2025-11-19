class SelectQuery:
    def __init__(self, table_name, columns=None, where_clause=None):
        self.table_name = table_name
        self.columns = columns if columns is not None else ['*']
        self.where_clause = where_clause

    def build_query(self):
        query = f"SELECT {', '.join(self.columns)} FROM {self.table_name}"
        if self.where_clause:
            query += f" WHERE {self.where_clause}"
        return query