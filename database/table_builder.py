# CREATE TABLE IF NOT EXISTS {table} (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     nearest_mrt_lrt VARCHAR(255),
#     mrt_lrt_line VARCHAR(255),
#     price DECIMAL(10, 2),
#     cooking_allowed BOOLEAN,
#     gender VARCHAR(50),
#     available_from DATE,
#     contact_no VARCHAR(20),
#     email VARCHAR(255),
#     location_map TEXT,
#     description TEXT
# );

class TableBuilder:
    def __init__(self, table_name, conn):
        self._table_name = table_name
        self._columns = []
        self._conn = conn
        self._last_column_name = None

    def id(self):
        self.column("id").integer()._primary()._auto_increment()
        return self

    def uuid(self):
        self.column("uuid").char(36)._primary()
        return self

    def _primary(self):
        self._current_column["primary_key"] = True
        return self

    def _auto_increment(self):
        self._current_column["auto_increment"] = True
        return self

    def column(self, name):
        self._current_column = {"name": name}
        self._columns.append(self._current_column)
        self._last_column_name = name
        return self

    def varchar(self, amount=255):
        self._current_column["type"] = f"VARCHAR({amount})"
        return self

    def char(self, length):
        self._current_column["type"] = f"CHAR({length})"
        return self

    def integer(self):
        self._current_column["type"] = "INT"
        return self

    def decimal(self, precision=10, scale=2):
        self._current_column["type"] = f"DECIMAL({precision}, {scale})"
        return self

    def boolean(self):
        self._current_column["type"] = "BOOLEAN"
        return self

    def unique(self):
        if self._last_column_name:
            for col in self._columns:
                if col['name'] == self._last_column_name:
                    col['unique'] = True
                    break
        else:
            raise ValueError("No column to apply uniqueness constraint. Please add a column first.")
        return self

    def create(self):
        cursor = self._conn.connection.cursor()

        # Check if table exists
        cursor.execute(f"SHOW TABLES LIKE '{self._table_name}'")
        table_exists = cursor.fetchone()

        if table_exists:
            # Get existing columns in the table
            cursor.execute(f"DESCRIBE {self._table_name}")
            existing_columns = {row[0]: row[3] for row in cursor.fetchall()}

            # Iterate over the columns and add new ones if they don't already exist
            for col in self._columns:
                if col['name'] not in existing_columns:
                    query = f"ALTER TABLE {self._table_name} ADD COLUMN {col['name']} {col['type']}"
                    if col.get('primary_key'):
                        query += " PRIMARY KEY"
                    if col.get('auto_increment'):
                        query += " AUTO_INCREMENT"
                    if col.get('unique'):
                        query += " UNIQUE"
                    cursor.execute(query)

        else:
            # Create new table
            query = f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
            for col in self._columns:
                col_definition = f"{col['name']} {col['type']}"
                if col.get('primary_key'):
                    col_definition += " PRIMARY KEY"
                if col.get('auto_increment'):
                    col_definition += " AUTO_INCREMENT"
                if col.get('unique'):
                    col_definition += " UNIQUE"
                query += col_definition + ", "
            query = query[:-2]  # Remove trailing comma and space
            query += ");"
            cursor.execute(query)

        self._conn.connection.commit()
        cursor.close()
