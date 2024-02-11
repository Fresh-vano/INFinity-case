from flask import Flask
from config import repo, init_repo

app = Flask(__name__)

@app.route('/api/items', methods=['GET'])
def get_items():
    return repo.get_items_list()

@app.route('/api/item_name', methods=['GET'])
def get_rtvalue(item_name):
    return repo.get_value_by_item(item_name)

if __name__ == '__main__':
    init_repo()
    print("Hello")
    app.run()