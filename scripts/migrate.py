# run_migrations.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from migrations.create_rent_table import create_rent_table

if __name__ == "__main__":
    create_rent_table()