import json 

class DataIO:
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod 
    def write_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


#test drive
if __name__ == "__main__":
    path = "JSON/test.json"
    #viet file
    user_list = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]
    DataIO.write_json(path, user_list)
