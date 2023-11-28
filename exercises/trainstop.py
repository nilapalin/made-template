import enum
from locale import LC_NUMERIC, atof, setlocale
import re

class Verkehr(enum.Enum):
    FV = "FV"
    RV = "RV"
    DPN = "nur DPN"
class Trainstop():

    def __init__(self, csv:dict):
        self.eva_nr = csv.get('EVA_NR')
        self.ds100 = csv.get('DS100')
        self.ifotp = csv.get('IFOPT')
        self.name = csv.get('NAME')
        self.verkehr = csv.get('Verkehr')
        self.laenge = csv.get('Laenge')
        self.breite = csv.get('Breite')
        self.betreiber_name = csv.get('Betreiber_Name')
        self.betreiber_nr = csv.get('Betreiber_Nr')

    def as_dict(self):
        return {'EVA_NR': self._eva_nr, 'DS100': self._ds100, 'IFOPT': self._ifotp, 'NAME': self._name, 'Verkehr': self._verkehr, 'Laenge': self._laenge, 'Breite': self._breite, 'Betreiber_Name': self._betreiber_name, 'Betreiber_Nr': self._betreiber_nr}#, 'Status': self._status}

    @property
    def eva_nr(self):
        return self._eva_nr
    @eva_nr.setter
    def eva_nr(self, eva_nr:int):
        self._eva_nr = withNotEmpty(eva_nr)

    @property
    def ds100(self):
        return self._ds100
    @ds100.setter
    def ds100(self, ds100:str):
        self._ds100 = withNotEmpty(ds100)

    @property
    def ifotp(self):
        return self._ifotp
    @ifotp.setter
    def ifotp(self, ifotp:str):
        withNotEmpty(ifotp)
        self._ifotp = withRegexp(ifotp, '^[a-zA-Z]{2}:\d*:\d*(:\d*)?$')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = withNotEmpty(name)

    @property
    def verkehr(self):
        return self._verkehr
    @verkehr.setter
    def verkehr(self, verkehr:Verkehr):
        withNotEmpty(verkehr)
        self._verkehr = withValidVerkehrValue(verkehr)

    @property
    def laenge(self):
        return self._laenge
    @laenge.setter
    def laenge(self, laenge):
        withNotEmpty(laenge)
        if (type(laenge) == str):
            laenge = withLocaleForFloat(laenge, 'de-DE')
        self._laenge = withFloatBetweenInclusive(laenge, -90, 90)

    @property
    def breite(self):
        return self._breite
    @breite.setter
    def breite(self, breite):
        withNotEmpty(breite)
        if (type(breite) == str):
            breite = withLocaleForFloat(breite, 'de-DE')
        self._breite = withFloatBetweenInclusive(breite, -90, 90)

    @property
    def betreiber_name(self):
        return self._betreiber_name
    @betreiber_name.setter
    def betreiber_name(self, betreiber_name:str):
        self._betreiber_name = withNotEmpty(betreiber_name)

    @property
    def betreiber_nr(self):
        return self._betreiber_nr
    @betreiber_nr.setter
    def betreiber_nr(self, betreiber_nr:int):
        self._betreiber_nr = withNotEmpty(betreiber_nr)

def withLocaleForFloat(value, locale):
    setlocale(LC_NUMERIC, locale)
    return atof(value)

def withFloatBetweenInclusive(value:float, min:float, max:float):
    if (value >= min and value <= max):
        return value
    raise ValueError("Value has to be inbetween (inclusive) min " + str(min) + " and max " + str(max) + " but is " + str(value))

def withValidVerkehrValue(value):
    enumValue = Verkehr(value)
    if (not isinstance(enumValue, Verkehr)):
        raise ValueError(f"{value} has to be a enum of Verkehr")
    return value

def withRegexp(value, regexp):
    p = re.compile(regexp)
    if(not p.match(value)):
        raise ValueError(f"{value} does not comply with regexp {regexp}")
    return value

def withNotEmpty(value):
    if (value != value or value == None or (isinstance(value, str) and len(str(value).strip()) == 0)):#nan:value!=vaue
        raise ValueError(f"{value} is null or empty")
    return value