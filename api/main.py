from flask import Flask, jsonify
from config import repo, init_repo

app = Flask(__name__)

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(repo.get_items_list())

@app.route('/api/<string:item_name>', methods=['GET'])
def get_rtvalue(item_name):
    return jsonify(repo.get_value_by_item(item_name))

if __name__ == '__main__':
    init_repo()
    app.run()