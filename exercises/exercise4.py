import csv
import os
import sqlite3
import zipfile

import pandas as pd

def download_file(url):
    print("Downloading url ", url)
    from urllib import request
    import zipfile
    fn, _ = request.urlretrieve(URL)    
    return fn

def extract_file(zip_file, file, path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract(file, path)

def read_columns(file, cols):
    with open(file,'rt', encoding='utf-8') as f:
        lines = list(csv.reader(f, delimiter=";"))
    headers, values =lines[0],lines[1:]
    max_length = max(map(len, lines))
    if (len(headers) < max_length):
        new_headers = ['NA']*max_length
        for i in range(max_length):
            name = str(i)
            if (i < len(headers)):
                name = headers[i]
            if (any(name in x for x in headers[0:i])):
                name = name + "_1"#TODO only duplicates non tripple...
            new_headers[i] = name
    df = pd.DataFrame(values,columns=new_headers)
    return pd.DataFrame(df, columns=cols)

def loadToSink(path: str, data, tablename):
        con = sqlite3.connect(path)
        con.execute('drop table if exists {}'.format(tablename))
        df = pd.DataFrame(data)
        df.to_sql(tablename, con, if_exists='fail', index=False)
        con.commit()
        con.close()

def transform(data):
    data['Geraet'] = data['Geraet'].astype(int)
    data['Hersteller'] = data['Hersteller'].astype(str)
    data['Model'] = data['Model'].astype(str)
    data['Monat'] = data['Monat'].astype(int)
    data['Temperatur'] = data['Temperatur'].str.replace(',', '.')
    data['Temperatur'] = data['Temperatur'].astype(float)
    data['Batterietemperatur'] = data['Batterietemperatur'].str.replace(',', '.')
    data['Batterietemperatur'] = data['Batterietemperatur'].astype(float)
    data['Geraet aktiv'] = data["Geraet aktiv"].astype(str)
    data['Temperatur'] = data['Temperatur']*9/5 + 32
    data['Batterietemperatur'] = data['Batterietemperatur']*9/5 + 32
    data.drop(data[data['Geraet'] <= 0].index)
    return data

if __name__ == '__main__':
    URL = 'https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip'
    zip_file = download_file(URL)
    extract_file(zip_file, "data.csv", "data")
    data = read_columns(os.path.join("data", "data.csv"), ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])
    data = data.rename(columns={'Temperatur in °C (DWD)': 'Temperatur', 'Batterietemperatur in °C': 'Batterietemperatur'})
    data = transform(data)
    loadToSink("temperatures.sqlite", data, "temperatures")
    print(data)