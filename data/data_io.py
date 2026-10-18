import json


class DataIO:
    @staticmethod  # khong can tao object van dung duoc ham (def)
    def read_json(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # json -> python dict
        return data

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # python object -> json

        print(f"Data written to {file_path} successfully.")
