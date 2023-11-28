import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from trainstop import Base, Trainstop

if __name__ == '__main__':
    url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'
    data = pd.read_csv(url,sep=';',encoding='utf-8')
    trainstop_list = [Trainstop(**rows) for rows in data.to_dict(orient='records')]#to_dict('records') transforms to [{'col1': 1, 'col2': 0.5}, {'col1': 2, 'col2': 0.75}]

    conn_string = 'sqlite:///trainstops.sqlite'
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)#creates all tables
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(trainstop_list)
    session.commit()

