from flask import Flask, jsonify, request
import inject


app = Flask(__name__)


# Routes for USER
@app.route('/user', methods=['POST'])
def create_user():
    db = inject.instance('DB')
    user_id = db.users.add(request.json)
    return jsonify({'user_id': user_id}), 201


@app.route('/user/<int:user_id>')
def get_user(user_id):
    db = inject.instance('DB')
    user = db.users.get_user_by_id(user_id)
    return jsonify(user), 201


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db = inject.instance('DB')
    db.users.update_user_by_id(user_id, request.json)
    return jsonify({'status': 'success'})


# Routes for GOODS
@app.route('/goods', methods=['POST'])
def create_goods():
    db = inject.instance('DB')
    result = db.goods.add_goods(request.json)
    return jsonify({'numbers of items created': result}), 201


@app.route('/goods')
def get_goods():
    db = inject.instance('DB')
    goods = db.goods.get_goods()
    return jsonify(goods), 200


@app.route('/goods', methods=['PUT'])
def update_goods():
    db = inject.instance('DB')
    update_info = db.goods.update_goods(request.json)
    return jsonify({
            'successfully_updated': update_info[0],
            'errors': {"no such id in goods": update_info[1]}
        }), 200


# Routes for STORES
@app.route('/store', methods=['POST'])
def create_store():
    db = inject.instance('DB')
    store_id = db.stores.add_store(request.json)
    return jsonify({'store_id': store_id}), 201


@app.route('/store/<int:store_id>')
def get_store(store_id):
    db = inject.instance('DB')
    store = db.stores.get_store(store_id)
    return jsonify(store), 200


@app.route('/store/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    db = inject.instance('DB')
    status = db.stores.update_store(store_id, request.json)
    return jsonify({'status': status}), 200




























