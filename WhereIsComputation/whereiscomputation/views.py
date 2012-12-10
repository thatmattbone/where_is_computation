from pyramid.view import view_config

from sqlalchemy import select, func

from .models import DBSession
from .sieve import sieve, ONE_HUNDRED_PRIMES, ONE_HUNDRED_PRIME_STRINGS

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    return {}


@view_config(route_name='precomputed', renderer="templates/primes.jinja2")
def precomputed(request):
    return {'name': 'Precomputed Primes',
            'primes': ", ".join(ONE_HUNDRED_PRIME_STRINGS)}


@view_config(route_name='serverside', renderer="templates/primes.jinja2")
def serverside(request):
    return {'name': 'Primes computed on the server-side',
            'primes': ", ".join([str(prime) for prime in sieve(ONE_HUNDRED_PRIMES[-1])])}


@view_config(route_name='clientside', renderer="templates/primes_clientside.jinja2")
def clientside(request):
    return {'name': 'Primes computed on the client-side'}


@view_config(route_name='server-and-clientside', renderer="templates/primes_clientside.jinja2")
def server_and_clientside(request):
    return {'name': 'Primes computed on the client and server-side',
            'primes': ", ".join([str(prime) for prime in sieve(100)])}


@view_config(route_name='database-layer', renderer="templates/primes.jinja2")
def database_layer(request):
    session = DBSession()
    primes = session.execute(select([func.prime_sieve(ONE_HUNDRED_PRIMES[-1])])).fetchall()[0][0]
    return {'name': 'Primes computed in the database layer',
            'primes': ", ".join([str(prime) for prime in primes])}
