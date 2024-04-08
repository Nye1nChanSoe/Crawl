from database.connection import DatabaseConnection
from database.table_builder import TableBuilder

def create_rent_table():
    # Establish a database connection
    connection = DatabaseConnection("localhost", "root", "", "db_rent")
    table_builder = TableBuilder("rents", connection)

    table_builder.id()
    table_builder.column("nearest_mrt_lrt").varchar()
    table_builder.column("mrt_lrt_line").varchar()
    table_builder.column("price").decimal(10, 2)
    table_builder.column("cooking_allowed").boolean()
    table_builder.column("gender").varchar(50)
    table_builder.column("available_from").date()
    table_builder.column("contact_no").varchar(20)
    table_builder.column("email").varchar(255)
    table_builder.column("location_map").varchar(40)
    table_builder.column("description").text()
    table_builder.column("created_at").datetime()
    table_builder.column("updated_at").datetime(True)

    table_builder.create()