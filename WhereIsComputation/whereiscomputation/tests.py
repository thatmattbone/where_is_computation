import unittest
import transaction

from pyramid import testing

from .models import DBSession
from .sieve import sieve, ONE_HUNDRED_PRIMES

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views import index
        request = testing.DummyRequest()
        info = index(request)
        self.assertEqual(info, {})


class TestSieve(unittest.TestCase):
    def test_100_primes(self):

        self.assertEqual(ONE_HUNDRED_PRIMES, sieve(541))
