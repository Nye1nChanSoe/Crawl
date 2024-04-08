from connection import DatabaseConnection
from table_builder import TableBuilder
from query_builder import QueryBuilder

if __name__ == "__main__":
    connection = DatabaseConnection("localhost", "root", "", "db_rent")
    table_builder = TableBuilder("users", connection)
    table_builder.id()
    table_builder.column("name").varchar()
    table_builder.column("email").varchar().unique()
    table_builder.column("created_at").datetime()
    table_builder.column("updated_at").datetime(True)
    table_builder.create()

    query_builder = QueryBuilder(connection)
    query_builder.table("users").insert(['name', 'email'], ['John Doe', 'john.doe@email.com']).execute()
    result = query_builder.table("users").select().execute()
    print(result)