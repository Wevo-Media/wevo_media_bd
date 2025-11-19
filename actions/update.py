class UpdateQuery:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute(self, query, params=None):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.db_connection.commit()
            return cursor.rowcount
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            cursor.close()