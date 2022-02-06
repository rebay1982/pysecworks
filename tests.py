from datetime import datetime, timedelta
import unittest
import uuid

from app import create_app, db
from app.models import User, Lookup
from app.lookup import is_valid_ip, reverse_ip, lookup_worker
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


    def test_get(self):
        lookup = Lookup.get('random_ip')

        self.assertIsNone(lookup)

    def test_valid_ip_get(self):
        ip = "127.0.0.1"
        response_code = "response_code"
        Lookup.create_new(ip, response_code)
        db.session.commit()

        lookup = Lookup.get(ip)
        self.assertIsNotNone(lookup)
        self.assertEqual(ip, lookup.ip_address)
        self.assertEqual(response_code, lookup.response_code)


# Should MOCK the dns.resolve lookup -- if service disappears, tests will start
# failing :(
class LookupWorkerCase (unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()                     # Setup and create the DB tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_reverse_ip(self):
        ip = "1.2.3.4"
        rev_ip = "4.3.2.1"

        result = reverse_ip(ip)

        self.assertEqual(rev_ip, result)

    def test_is_valid_ip_good_ip(self):
        ip = "127.0.0.1"
        
        result = is_valid_ip(ip)

        self.assertTrue(result)

    def test_is_valid_ip_bad_ip(self):
        bad_ip = "300.0.0.1"

        result = is_valid_ip(bad_ip)

        self.assertFalse(result)
    
    def test_is_valid_ip_reject_ipv6(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

        result = is_valid_ip(ipv6)

        self.assertFalse(result)

    def test_lookup_good(self):
        ips = ["127.0.0.2"]
        expected_response_codes = ["127.0.0.10", "127.0.0.4", "127.0.0.2"]

        lookup_worker(ips)
        lookup = Lookup.get(ips[0])
        
        self.assertEqual(ips[0], lookup.ip_address)
        self.assertEqual(lookup.created_at, lookup.updated_at)

        for expected_code in expected_response_codes:
            self.assertTrue(expected_code in lookup.response_code)

    def test_lookup_bad(self):
        ips = ["127.0.0.1"]
        expected_response_codes = ["No Response"]

        lookup_worker(ips)
        lookup = Lookup.get(ips[0])
        
        self.assertEqual(ips[0], lookup.ip_address)
        self.assertEqual(lookup.created_at, lookup.updated_at)

        for expected_code in expected_response_codes:
            self.assertTrue(expected_code in lookup.response_code)

    def test_lookup_multiple(self):
        ips = ["127.0.0.1", "127.0.0.2"]
        expected_response_codes = [["No Response"], ["127.0.0.10", "127.0.0.4", "127.0.0.2"]]

        lookup_worker(ips)
        lookupA = Lookup.get(ips[0])
        lookupB = Lookup.get(ips[1])

        self.assertEqual(ips[0], lookupA.ip_address)
        self.assertEqual(ips[1], lookupB.ip_address)

        for expected_code in expected_response_codes[0]:
            self.assertTrue(expected_code in lookupA.response_code)

        for expected_code in expected_response_codes[1]:
            self.assertTrue(expected_code in lookupB.response_code)

    def test_lookup_update(self):
        ips = ["127.0.0.1"]
        
        lookup_worker(ips)
        lookup_worker(ips)
        
        lookup = Lookup.get(ips[0])

        self.assertLess(lookup.created_at, lookup.updated_at)


def isValidUUID(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False



if __name__ == '__main__':
    unittest.main(verbosity=2)
