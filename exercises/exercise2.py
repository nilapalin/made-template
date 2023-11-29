import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from trainstop import Trainstop
from trainstopdb import Base, TrainstopDb

def load_trainstops_from_url(url):
    data = pd.read_csv(url,sep=';',encoding='utf-8')
    trainstop_list = []
    count = 0
    for row in data.to_dict(orient="records"):
        try:
            trainstop_list.append(Trainstop(row))
        except ValueError as e:
            count=count+1
        except Exception as e:
            count=count+1
    print("Amount of rows rejected: " + str(count))
    print("Amount of valid rows: " + str(len(trainstop_list)))
    return trainstop_list

def to_trainstopsdb(trainstop_list:[]):
    trainstopdb_list = []
    for item in trainstop_list:
        trainstopdb_list.append(TrainstopDb(item))
    return trainstopdb_list

def to_db(conn_string, trainstopdb_list):
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)#creates all tables
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(trainstopdb_list)
    session.commit()

if __name__ == '__main__':
    trainstop_list = load_trainstops_from_url('https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV')
    trainstopdb_list = to_trainstopsdb(trainstop_list)
    to_db('sqlite:///trainstops.sqlite', trainstopdb_list)

