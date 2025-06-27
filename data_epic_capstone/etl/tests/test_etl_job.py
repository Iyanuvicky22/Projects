"""
- test for duplicates.
- test for invalid rows.
- test for correct upserts.
"""
from utils.utils import fetch_db_records

def test_duplicates():
    db_data = fetch_db_records()    
    assert db_data['name'].duplicated().count() == 0

def test_invalid_rows():
    db_data = fetch_db_records()
    pass
