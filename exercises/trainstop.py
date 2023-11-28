from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
Base = declarative_base()
class Trainstop(Base):
    __tablename__ = 'trainstops'
    _eva_nr = Column('EVA_NR', Integer, primary_key=True, nullable=False)
    _ds100 = Column('DS100', String)
    _ifotp = Column('IFOPT', String)
    _name = Column('NAME', String)
    _verkehr = Column('Verkehr', String)
    _laenge = Column('Laenge', String)#Float)
    _breite = Column('Breite', String)#Float)
    _betreiber_name = Column('Betreiber_Name', String)
    _betreiber_nr = Column('Betreiber_Nr', Integer)#, unique=True)
    #_status = Column('Status', String)

    def __init__(self):
        self._eva_nr:int=None
        self._ds100:str=None
        self._ifotp:str=None
        self._name:str=None
        self._verkehr:str=None
        self._laenge:float=None
        self._breite:float=None
        self._betreiber_name:str=None
        self._betreiber_nr:int=None
        #self._status:str=None

    def __init__(self, **csv):
        self.eva_nr = csv.get('EVA_NR')
        self.ds100 = csv.get('DS100')
        self.ifotp = csv.get('IFOPT')
        self.name = csv.get('NAME')
        self.verkehr = csv.get('Verkehr')
        self.laenge = csv.get('Laenge')
        self.breite = csv.get('Breite')
        self.betreiber_name = csv.get('Betreiber_Name')
        self.betreiber_nr = csv.get('Betreiber_Nr')
        #self.status = csv.get('Status')

    def as_dict(self):
        return {'EVA_NR': self._eva_nr, 'DS100': self._ds100, 'IFOPT': self._ifotp, 'NAME': self._name, 'Verkehr': self._verkehr, 'Laenge': self._laenge, 'Breite': self._breite, 'Betreiber_Name': self._betreiber_name, 'Betreiber_Nr': self._betreiber_nr}#, 'Status': self._status}

    @hybrid_property
    def eva_nr(self):
        return self._eva_nr
    @eva_nr.setter
    def eva_nr(self, eva_nr:int):
        self._eva_nr = eva_nr

    @hybrid_property
    def ds100(self):
        return self._ds100
    @ds100.setter
    def ds100(self, ds100:str):
        self._ds100 = ds100

    @hybrid_property
    def ifotp(self):
        return self._ifotp
    @ifotp.setter
    def ifotp(self, ifotp:str):
        self._ifotp = ifotp

    @hybrid_property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = name

    @hybrid_property
    def verkehr(self):
        return self._verkehr
    @verkehr.setter
    def verkehr(self, verkehr:str):
        self._verkehr = verkehr

    @hybrid_property
    def laenge(self):
        return self._laenge
    @laenge.setter
    def laenge(self, laenge:str):#:float):
        self._laenge = laenge

    @hybrid_property
    def breite(self):
        return self._breite
    @breite.setter
    def breite(self, breite:str):#:float):
        self._breite = breite

    @hybrid_property
    def betreiber_name(self):
        return self._betreiber_name
    @betreiber_name.setter
    def betreiber_name(self, betreiber_name:str):
        self._betreiber_name = betreiber_name

    @hybrid_property
    def betreiber_nr(self):
        return self._betreiber_nr
    @betreiber_nr.setter
    def betreiber_nr(self, betreiber_nr:int):
        self._betreiber_nr = betreiber_nr

    # @hybrid_property
    # def status(self):
    #     return self._status
    # @status.setter
    # def status(self, status:str):
    #     self._status = status