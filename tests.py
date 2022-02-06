from datetime import datetime, timedelta
import unittest
import uuid

from app import create_app, db
from app.models import User, Lookup
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'   # encore use of in-memory DB.

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()                     # Setup and create the DB tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hasing(self):
        u = User(username='test')
        u.set_password('test')

        result = u.check_password('test') 

        self.assertTrue(result)
        self.assertFalse('test' in u.password_hash)

    def test_password_validation(self):
        u = User(username='test')
        u.set_password('test')
        
        resultWrong = u.check_password('wrong') 
        resultGood = u.check_password('test') 

        self.assertFalse(resultWrong)
        self.assertTrue(resultGood)

    def test_get_token(self):
        u = User(username='test')
        u.set_password('test')
        
        token = u.get_token()
        
        self.assertTrue(32, len(token))

    def test_get_token_twice(self):
        u = User(username='test')
        u.set_password('test')
        token1 = u.get_token()
        db.session.commit()

        token2 = u.get_token()

        self.assertTrue(32, len(token1))
        self.assertTrue(32, len(token2))
        self.assertEqual(token1, token2)
       
    def test_check_token(self):
        u = User(username='test')
        u.set_password('test')
        token = u.get_token()
        db.session.commit()

        user = User.check_token(token)

        self.assertIsNotNone(user)

    def test_revoke_token(self):
        u = User(username='test')
        u.set_password('test')
        token = u.get_token()
        db.session.commit()
        userBeforeRevoke = User.check_token(token)
        
        userBeforeRevoke.revoke_token()
        db.session.commit()
        userAfterRevoke = User.check_token(token)

        self.assertIsNotNone(userBeforeRevoke)
        self.assertIsNone(userAfterRevoke)

class LookupModelCase (unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()                     # Setup and create the DB tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_lookup(self):
        ip = '127.0.0.1' 
        response = '127.0.0.10'

        l = Lookup.create_new(ip, response)
        db.session.commit()

        self.assertEqual(ip, l.ip_address)
        self.assertEqual(response, l.response_code)
        self.assertEqual(l.created_at, l.updated_at)
        self.assertTrue(isValidUUID(l.id))

    def test_update_lookup(self):
        updated_response = '127.0.0.1'
        l = Lookup.create_new('127.0.0.1', '127.0.0.10')
        db.session.commit()

        l.update(updated_response)

        self.assertEqual(updated_response, l.response_code)
        self.assertLess(l.created_at, l.updated_at)


def isValidUUID(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    unittest.main(verbosity=2)
