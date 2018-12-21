from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class Tile(Base):
    __tablename__ = 'tile'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    implode = Column(Integer, nullable=True)
    can_add_objectives = Column(Boolean, default=False)
    level = Column(Integer, ForeignKey('level.id'))


class Objective(Base):
    __tablename__ = 'objective'
    id = Column(Integer, primary_key=True)
    tile = Column(Integer, ForeignKey('tile.id'))
    number = Column(Integer)
    level = Column(Integer, ForeignKey('level.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    current_level = Column(Integer, ForeignKey('level.id'))

    def __init__(self, name, current_level):
        self.name = name
        self.current_level = current_level


engine = create_engine('sqlite:///../game.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
