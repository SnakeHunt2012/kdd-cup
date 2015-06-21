import json
import psycopg2
import pickle

# database tools
def db_connect():
    '''
    connect to database
    '''
    database_setting = None
    with open("../setting/general.json", 'r') as file_setting:
        json_setting = json.loads(file_setting.read())
        database_setting = json_setting["database_setting"]
    if "AskForPassword" in database_setting:
        password = raw_input("PostgreSQL Password: ")
        database_setting.replace("##AskForPassword##", password)
    conn = psycopg2.connect(database_setting)
    return conn

def db_query(conn, query):
    '''
    query from database
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# feature tools
def get_features():
    '''
    '''
    
# model tools
def save_model(model):
    '''
    '''
    pickle.dump(model, open("../model/benchmark.pickle", "w"))

def load_model(path_model):
    '''
    '''
    model = None
    with open(path_model, 'r') as file_model:
        model = pickle.load(file_model)
    return model

# sql tools
def load_sql(file):
    sql = None
    with open(file, 'r') as file_sql:
        sql = file_sql.read().strip()
    return sql

# submission tools
def save_submission():
    '''
    '''
