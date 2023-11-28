from sqlalchemy import Column, Enum
from sqlalchemy.dialects.sqlite import FLOAT, INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from trainstop import Trainstop, Verkehr

Base = declarative_base()

class TrainstopDb(Base):
    __tablename__ = 'trainstops'
    _eva_nr = Column('EVA_NR', INTEGER, primary_key=True, nullable=False)
    _ds100 = Column('DS100', VARCHAR)
    _ifotp = Column('IFOPT', VARCHAR)
    _name = Column('NAME', VARCHAR)
    _verkehr = Column('Verkehr', Enum(Verkehr))
    _laenge = Column('Laenge', FLOAT)
    _breite = Column('Breite', FLOAT)
    _betreiber_name = Column('Betreiber_Name', VARCHAR)
    _betreiber_nr = Column('Betreiber_Nr', INTEGER)

    def __init__(self, trainstop:Trainstop):
        self._eva_nr = trainstop.eva_nr
        self._ds100 = trainstop.ds100
        self._ifotp = trainstop.ifotp
        self._name = trainstop.name
        self._verkehr = trainstop.verkehr
        self._laenge = trainstop.laenge
        self._breite = trainstop.breite
        self._betreiber_name = trainstop.betreiber_name
        self._betreiber_nr = trainstop.betreiber_nr