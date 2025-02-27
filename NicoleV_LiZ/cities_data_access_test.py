import cities_data_access as cda
import pytest
from sqlalchemy import create_engine, text, inspect

cda.DB_URI = 'sqlite:///../../../../data/world_db/world_test.db'

# Create tests for each function in cities_data_access
# Use red30_data_access_test.py to help you with the development of these tests

@pytest.fixture
def setup_database():
    # Fixture to set up a clean database for each test.
    engine = create_engine(cda.DB_URI)
    inspector = inspect(engine)
    if not "city" in inspector.get_table_names():
        with engine.connect() as conn:
            # Create the "city" table
            conn.execute(text("""
                CREATE TABLE "city" (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT,
                    countrycode TEXT,
                    district    TEXT,
                    population  INT
                )
            """))
    else:
        with engine.connect() as conn:
            conn.execute(text('DELETE FROM city'))
            conn.commit()
    # Yield execution to the test function
    yield
    # Return from test function and teardown from test
    # That is, drop the table after each test
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS city'))

def test_connection(setup_database):
    assert True

def test_get_country_codes_and_names():
    expected = ('ABW', 'Aruba')
    cc_name = cda.get_country_codes_and_names()
    actual = cc_name[0]
    assert actual == expected

def test_add_city(setup_database):
    actual = cda.add_city("Kanata", "CAN", "Ontario", 150000)
    assert actual != None
    assert actual > 0

def test_get_city_by_name(setup_database):
    cda.add_city("Kanata", "CAN", "Ontario", 150000)
    actual = cda.get_city_by_name('kanata')
    assert actual != None
    test_none = cda.get_city_by_name('asd')
    assert test_none == None

def test_update_city_population(setup_database):
    cda.add_city("Kanata", "CAN", "Ontario", 150000)
    expected = 1
    actual = cda.update_city_population("Kanata", 100000)
    assert actual == expected

def test_delete_city_by_name(setup_database):
    expected = None
    rowcount = cda.add_city("Kanata","CAN","Ontatio",150000)
    assert rowcount == 1
    cda.delete_city_by_name("Kanata")
    actual = cda.get_city_by_name("Kanata")
    assert actual == expected

