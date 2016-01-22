import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Comparison

import config

def main():
    engine = create_engine("sqlite:///comparisons.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    try:
        with open("sample_match.csv", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.next()
            for row in reader:
                record = {
                    'decision_id': row[headers[0]],
                    'decision_description': row[headers[1]],
                    'contract_id': row[headers[2]],
                    'contract_description': row[headers[3]],
                    }
                session.add(Comparison(**record))
        session.commit()
        print("Database populated successfully.")
        session.close()
    except:
        print("Error while loading data, no changes were made to the database.")
        session.rollback()
        session.close()

if __name__ == "__main__":
    main()
