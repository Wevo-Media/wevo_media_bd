import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class ConnectionDB:

    def __init__(self):
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def create_connection(self):
        
        try:
            connection = psycopg2.connect(
                database=self.database,
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            print(f"Database connection established: {connection.status}")
            return connection
        
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
        