class DatabaseTable:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_table(self, table = "table_1"):
        cursor = self.connection.connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS {table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nearest_mrt_lrt VARCHAR(255),
                mrt_lrt_line VARCHAR(255),
                price DECIMAL(10, 2),
                gender VARCHAR(50),
                cooking_allowed BOOLEAN,
                available_from DATE,
                contact_no VARCHAR(20),
                email VARCHAR(255),
                location_map TEXT,
                description TEXT
            );
        """.format(table = table)

        cursor.execute(query)
        self.connection.connection.commit()
        cursor.close()