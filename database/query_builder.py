class QueryBuilder:
    def __init__(self, connection) -> None:
        self.connection = connection
        self._reset()

    def _reset(self):
        self.query = ""
        self.params = []
        return self

    def table(self, name):
        self._table = name
        return self

    def select(self, columns = "*"):
        self.query = f"SELECT {columns} FROM {self._table}"
        return self

    def where(self, condition, param):
        if "WHERE" not in self.query:
            self.query += " WHERE"
        else:
            self.query += " AND"
        self.query += f" {condition}"
        self.params.append(param)
        return self

    def insert(self, columns, values):
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        self.query = f"INSERT INTO {self._table} ({columns_str}) VALUES ({placeholders})"
        self.params.extend(values)
        return self

    def execute(self):
        cursor = self.connection.connection.cursor(buffered=True)
        cursor.execute(self.query, self.params)
        # Check if it's a SELECT operation
        if self.query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        # It's an action query, commit the changes
        else:
            self.connection.connection.commit()
            result = cursor.rowcount
        self._reset()
        cursor.close()
        return result