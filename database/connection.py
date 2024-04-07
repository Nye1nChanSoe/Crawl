import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, user, password, database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to {database} successfully".format(database = self.database))
        except Error as e:
            # If database does not exist, create it
            if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self._create_database()  # Call the internal method
                # Reconnect after creating the database
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            else:
                raise

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def _create_database(self):
        try:
            # Connect to MySQL server without specifying database
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            # Create database
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            connection.close()
            print(f"Database '{self.database}' created successfully.")
        except Error as e:
            print(f"Error creating database: {e}")