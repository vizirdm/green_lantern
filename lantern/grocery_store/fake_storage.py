from itertools import count
from .custom_errors import NoSuchUserError, NoSuchStoreError, \
    NoSuchManagerError


class StorageObject:
    def __init__(self):
        self._objects = {}
        self._id_counter = count(1)


class FakeStorage:
    def __init__(self):
        self._users = FakeUsers()
        self._goods = FakeGoods()
        self._stores = FakeStores(users_id=self._users.get_all_users_id())

    @property
    def users(self):
        return self._users

    @property
    def goods(self):
        return self._goods

    @property
    def stores(self):
        return self._stores


class FakeUsers(StorageObject):

    def add(self, user):
        user_id = next(self._id_counter)
        self._objects[user_id] = user
        return user_id

    def get_user_by_id(self, user_id):
        if not self._objects.get(user_id):
            raise NoSuchUserError(user_id)
        else:
            return self._objects.get(user_id)

    def update_user_by_id(self, user_id, user):
        if user_id in self._objects:
            self._objects[user_id] = user
        else:
            raise NoSuchUserError(user_id)

    def get_all_users_id(self):
        return self._objects.keys()


class FakeGoods(StorageObject, FakeStorage):

    def add_goods(self, goods):
        for item in goods:
            self._objects[next(self._id_counter)] = item
        return len(goods)

    def get_goods(self):
        response = []
        for goods in self._objects.items():
            temp = goods[1]
            _id = {'id': goods[0]}
            temp.update(_id)
            response.append(temp)
        return response

    def update_goods(self, goods):
        not_found_ids = []
        successfully_updated = 0
        for item in goods:
            if not self._objects.get(item['id']):
                not_found_ids.append(item['id'])
                continue
            item_id = item['id']
            del item['id']
            self._objects[item_id] = item
            successfully_updated += 1
        return successfully_updated, not_found_ids


class FakeStores(StorageObject):
    def __init__(self, users_id):
        self.users_id = users_id
        super().__init__()

    def add_store(self, store):
        if store['manager_id'] not in self.users_id:
            raise NoSuchUserError(store['manager_id'])
        store_id = next(self._id_counter)
        self._objects[store_id] = store
        return store_id

    def get_store(self, store_id):
        if not self._objects.get(store_id):
            raise NoSuchStoreError(store_id)
        return self._objects[store_id]

    def update_store(self, store_id, new_data):
        if store_id not in self.users_id:
            raise NoSuchStoreError(store_id)
        if new_data['manager_id'] not in self.get_managers_ids():
            raise NoSuchManagerError(new_data['manager_id'])
        self._objects[store_id] = new_data
        return 'success'

    def get_managers_ids(self):
        return [i['manager_id'] for i in self._objects.values()]






















