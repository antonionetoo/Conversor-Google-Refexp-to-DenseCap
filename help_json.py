import json

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)   

def get_json(file_name):
    data = None
    with open(file_name) as f:
        data = json.load(f)
    return data

        