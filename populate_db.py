import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Comparison


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def main():
    engine = create_engine("sqlite:///comparisons.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    try:
        with open("sample_match.csv", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = {
                    'decision_id': row['decision_id'],
                    'decision_description': row['decision_description'],
                    'contract_id': row['contract_id'],
                    'contract_description': row['contract_description'],
                    }
                session.add(Comparison(**record))
    except:
        print("Error while loading data, no changes were made to the database.")
        session.rollback()
    finally:
        session.commit()
        print("Database populated successfully.")
        session.close()


if __name__ == "__main__":
    main()
