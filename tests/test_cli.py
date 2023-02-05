import os
from unittest import mock

import pytest
import mysql.connector


@pytest.fixture(scope="module")
def mysql_database():
    """Connect to MySQL
    - Create and new test database (Will drop existing db first)
    - Create tables and insert values
    - Drop created test database at end
    """

    # Connect to the MySQL server
    # Get the values of environment variables or use default values if they are not set
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 3306)
    user = os.environ.get("DB_USER", "")
    password = os.environ.get("DB_PASSWORD", "")
    database = f'{os.environ.get("DB_DATABASE", "budget_db")}__testdb'

    # Connect to the database using the obtained values
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )

    # Drop the database if it exists
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {database}")
    cursor.close()

    # Create a new database
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {database}")
    cursor.close()

    # Create tables
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")

    # Create table `t_shops`
    cursor.execute(
        """
            CREATE TABLE t_shops (
                a_id        INT AUTO_INCREMENT PRIMARY KEY,
                a_name      VARCHAR(255) NOT NULL,
                a_online    BOOLEAN NOT NULL
            )
        """
    )

    # Create table t_budgets
    cursor.execute(
        """
            CREATE TABLE t_budgets (
                a_shop_id       INT,
                a_month         DATE NOT NULL,
                a_budget_amount DECIMAL(10,2) NOT NULL,
                a_amount_spent  DECIMAL(10,2) NOT NULL,
                a_notification_sent BOOLEAN NOT NULL DEFAULT FALSE,
                a_notification_current_threshold DECIMAL(10,2) DEFAULT 0,
                PRIMARY KEY (a_shop_id, a_month),
                FOREIGN KEY (a_shop_id) REFERENCES t_shops (a_id)
            )
        """
    )

    # Insert data to new tables created
    cursor.execute(
        """
            INSERT INTO t_shops
            (a_id, a_name, a_online)
            VALUES
            (1, 'Super Mart', 1),
            (2, 'Trendy Treasures', 0),
            (3, 'Fashion Fix', 1),
            (4, 'Chic Choice', 0),
            (5, 'Stylish Street', 1),
            (6, 'Fashion Forward', 0),
            (7, 'Fashion Frenzy', 1),
            (8, 'Trendy Trends', 1);
        """
    )
    cursor.execute(
        f"""
            INSERT INTO t_budgets
            (a_shop_id, a_month, a_budget_amount, a_amount_spent)
            VALUES
            (1, '2023-02-01', 1150.00, 1000.67),
            (2, '2023-02-01', 1050.00, 900.64),
            (3, '2023-02-01', 1250.00, 1180.81),
            (4, '2023-02-01', 1050.00, 954.93),
            (5, '2023-02-01', 1250.00, 1105.12),
            (6, '2023-02-02', 1150.00, 1155.00),
            (7, '2023-02-03', 1150.00, 1150.00),
            (8, '2023-02-01', 1150.00, 1004.25);
        """
    )

    conn.commit()
    cursor.close()

    yield conn

    # Drop the database if it exists
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {database}")
    cursor.close()

    # Close the database connection
    conn.close()


def test_mysql_database(mysql_database):
    """Test the database connection"""

    # Test database is created
    cursor = mysql_database.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    assert (mysql_database.database,) in databases
    cursor.close()

    # Test tables are created
    cursor = mysql_database.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    assert ("t_shops",) in tables
    assert ("t_budgets",) in tables
    cursor.close()

    # Get the number of rows in the table `t_shops`
    cursor = mysql_database.cursor()
    cursor.execute("SELECT COUNT(*) FROM t_shops")
    count = cursor.fetchone()[0]
    # Assert that the count is what you expect
    assert count == 8
    cursor.close()

    # Get the number of rows in the table `t_budgets`
    cursor = mysql_database.cursor()
    cursor.execute("SELECT COUNT(*) FROM t_budgets")
    count = cursor.fetchone()[0]
    # Assert that the count is what you expect
    assert count == 8
    cursor.close()


def test_cli(capsys, mysql_database):
    with mock.patch("database.connect_to_db") as connect_to_db:
        # Patch database
        connect_to_db.return_value = mysql_database

        # Import should be here to overide database
        from cli import main

        # Call main() with new db
        main()

        captured = capsys.readouterr()
        assert captured.out.strip() != "No budget found!"

        # Call main() after data is updated
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "No budget found!"
