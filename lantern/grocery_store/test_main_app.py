from .storage_app import app
from .fake_storage import FakeStorage
from . import fill_data
import pytest
import inject


def configure_test(binder):
    db = FakeStorage()
    binder.bind('DB', db)


@pytest.fixture
def app_run():
    app.config['TESTING'] = True
    inject.clear_and_configure(configure_test)
    with app.test_client() as client:
        return client


class TestUsers:
    def test_new_user_creation(self, app_run):
        post_response = app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        assert post_response.status_code == 201
        assert post_response.json == {'user_id': 1}
        post_response_2 = app_run.post(
            '/user',
            json={'name': 'Taras Tarasenko'},
        )
        assert post_response_2.json == {'user_id': 2}

    def test_successful_get_user(self, app_run):
        post_response = app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        user_id = post_response.json['user_id']
        get_response = app_run.get(f'/user/{user_id}')
        assert get_response.status_code == 201
        assert get_response.json['name'] == 'Dmytro Vizir'

    def test_get_unexistent_user(self, app_run):
        get_response = app_run.get(f'/user/1')
        assert get_response.status_code == 404
        assert get_response.json == {'error': 'No such user_id 1'}

    def test_successful_update_user(self, app_run):
        post_response = app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response_user_id = post_response.json['user_id']
        put_response = app_run.put(
            f'user/{post_response_user_id}',
            json={'name': 'Taras Tarasenko'},
        )
        assert put_response.status_code == 200
        assert put_response.json == {'status': 'success'}

    def test_update_unexistent_user(self, app_run):
        put_response = app_run.put(
            f'user/1',
            json={'name': 'Taras Tarasenko'},
        )
        assert put_response.status_code == 404
        assert put_response.json == {'error': 'No such user_id 1'}


class TestGoods:
    def test_goods_creation(self, app_run):
        post_response = app_run.post(
            '/goods',
            json=fill_data.GOODS,
        )
        assert post_response.status_code == 201
        assert post_response.json == {
            'numbers of items created': len(fill_data.GOODS)
        }

    def test_get_goods(self, app_run):
        app_run.post(
            '/goods',
            json=fill_data.GOODS,
        )
        get_response = app_run.get('/goods')
        assert get_response.status_code == 200
        assert get_response.json == fill_data.GOODS_WITH_ID

    def test_update_goods(self, app_run):
        app_run.post(
            '/goods',
            json=fill_data.GOODS,
        )
        put_response = app_run.put(
            '/goods',
            json=fill_data.GOODS_WITH_ID_2
        )
        assert put_response.status_code == 200
        assert put_response.json == {
            'successfully_updated': 3,
            'errors': {'no such id in goods': [4, 5]}
        }


class TestStores:
    def test_post_store(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response = app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        assert post_response.status_code == 201
        assert post_response.json == {'store_id': 1}

    def test_post_store_with_not_existing_manager_id(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response = app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        assert post_response.status_code == 404
        assert post_response.json == {'error': 'No such user_id 2'}

    def test_get_store(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response = app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        get_response = app_run.get(f'/store/{post_response.json["store_id"]}')
        assert get_response.status_code == 200
        assert get_response.json == {'name': 'Mad Cow',
                                     'location': 'Lviv', 'manager_id': 1}

    def test_get_store_with_not_existing_id(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response = app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        get_response = app_run.get(f'store/{post_response.json["store_id"]+1}')
        assert get_response.status_code == 404
        assert get_response.json == {
            'error': f'No such store_id {post_response.json["store_id"]+1}'
        }

    def test_update_store(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        put_response = app_run.put(
            '/store/1',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 1}
        )
        assert put_response.status_code == 200
        assert put_response.json == {'status': 'success'}

    def test_update_store_with_not_existing_store_id(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        post_response = app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        put_response = app_run.put(
            f'/store/{post_response.json["store_id"]+1}',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 1}
        )
        assert put_response.status_code == 404
        assert put_response.json == {
            'error': f'No such store_id {post_response.json["store_id"]+1}'
        }

    def test_update_store_with_not_existing_manager_id(self, app_run):
        app_run.post(
            '/user',
            json={'name': 'Dmytro Vizir'},
        )
        app_run.post(
            '/user',
            json={'name': 'Taras Tarasenko'},
        )
        app_run.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        )
        app_run.post(
            '/store',
            json={'name': 'McDonalds', 'location': 'Kyiv', 'manager_id': 2}
        )
        put_response = app_run.put(
            '/store/1',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 3}
        )
        assert put_response.status_code == 404
        assert put_response.json == {
            'error': 'No such manager_id 3'
        }





















