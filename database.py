__author__ = 'maciejbanasiewicz'

import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pprint import pprint


Base = declarative_base()
engine = create_engine('sqlite:///metafiles.sqlite')
Base.metadata.bind = engine

class File(Base):
        __tablename__ = 'files'
        # Here we define columns for the table person
        # Notice that each column is also a normal Python instance attribute.
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        file_path = Column(String(1024), nullable=False)


def createFile(name, file_path):
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    new_file = File(name=name, file_path=file_path)
    session.add(new_file)
    session.commit()



def getListOfFiles():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    files = session.query(File).all()
    return files


def createDatabase():
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)