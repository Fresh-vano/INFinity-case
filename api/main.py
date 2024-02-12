from flask import Flask
from config import repo, init_repo

app = Flask(__name__)

@app.route('/categories', methods=['GET'])
def get_categories():
    return repo.get_categories_list()

@app.route('/categories/<string:category>', methods=['GET'])
def get_category_content(category):
    return repo.get_category_content(category)

@app.route('/categories/<string:category>/<string:name>', methods=['GET'])
def get_price(category, name):
    return {"price": repo.get_value_by_params(category, [name])}

if __name__ == '__main__':
    init_repo()
    app.run()