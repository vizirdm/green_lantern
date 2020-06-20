from flask import jsonify
from .storage_app import app


class NoSuchUserError(Exception):
    def __init__(self, user_id):
        self.message = f'No such user_id {user_id}'


class NoSuchStoreError(Exception):
    def __init__(self, store_id):
        self.message = f'No such store_id {store_id}'


class NoSuchManagerError(Exception):
    def __init__(self, manager_id):
        self.message = f'No such manager_id {manager_id}'


@app.errorhandler(NoSuchUserError)
def no_such_user(error):
    return jsonify({'error': error.message}), 404


@app.errorhandler(NoSuchStoreError)
def no_such_store(error):
    return jsonify({'error': error.message}), 404


@app.errorhandler(NoSuchManagerError)
def no_such_manager(error):
    return jsonify({'error': error.message}), 404
