import sys
import csv
from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import codecs

Base = declarative_base()


class Comparison(Base):
    __tablename__ = 'comparison'
    id = Column(Integer, primary_key=True)
    decision_id = Column(Unicode)
    decision_description = Column(Unicode)
    contract_id = Column(Unicode)
    contract_description = Column(Unicode)
    is_match = Column(Integer, default=0)
    is_not_match = Column(Integer, default=0)
    total_comparisons = Column(Integer, default=0)


if __name__ == "__main__":
    engine = create_engine('sqlite:///comparisons.db')
    Base.metadata.create_all(engine)
