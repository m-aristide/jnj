from crm import User, get_all_users
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage

@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    u = User(first_name="Patrick", last_name="Martin",
    address="1 rue du chemin, 75000 Paris", phone_number="0987654321")
    u.save()
    return u

def test_full_name(user):
    assert user.full_name == 'Patrick Martin'
    user.last_name='Paul'
    assert user.full_name == 'Patrick Paul'

def test_exists(user):
    assert user.exists() is True

def test_not_exists(setup_db):
    us = User(first_name="Patrick", last_name="Martin",
    address="1 rue du chemin, 75000 Paris", phone_number="0987654321")
    assert us.exists() is False

def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance['first_name'] == 'Patrick'
    assert user.db_instance['last_name'] == 'Martin'