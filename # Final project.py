# Final project

import json
import os
import requests
import sqlite3

response = requests.get('# insert url of api')
data = response.text
in_dict = json.loads(data) # this line might do the same thing as dict_list

def json_try():
    try:
        source_dir = os.path.dirname(__file__)  # directory name
        full_path = os.path.join(source_dir, 'com.json')
        file = open(full_path, 'r') # try to read the data from the file
        contents = file.read() # get it into a string
        dict_list = json.loads(contents) # loads the data into a dictionary
        file.close() # close the file, we have the data
        data = json.loads(string)
    except:
        print("error reading from file")

def create_database():
    conn = sqlite3.connect('')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS api_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# def insert_data(data):