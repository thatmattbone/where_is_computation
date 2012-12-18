from pyramid.view import view_config

from sqlalchemy import select, func

import redis

from .models import DBSession
from .sieve import sieve, sieve_lua, ONE_HUNDRED_PRIME_STRINGS, LAST_PRIME


def redis_connection():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r


@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    return {}


@view_config(route_name='precomputed', renderer="templates/precomputed.jinja2")
def precomputed(request):
    return {'name': 'Precomputed Primes'}


@view_config(route_name='serverside', renderer="templates/primes.jinja2")
def serverside(request):
    return {'name': 'Primes computed on the server-side',
            'primes': ", ".join([str(prime) for prime in sieve(LAST_PRIME)])}


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
    primes = session.execute(select([func.prime_sieve(LAST_PRIME)])).fetchall()[0][0]
    return {'name': 'Primes computed in Postgres',
            'primes': ", ".join([str(prime) for prime in primes])}


@view_config(route_name='redis-script', renderer="templates/primes.jinja2")
def redis_script(request):
    r = redis_connection()
    sieve = r.register_script(sieve_lua)
    primes = sieve(args=[LAST_PRIME])
    return {'name': 'Primes computed with a Redis script',
            'primes': ", ".join([str(prime) for prime in primes])}


@view_config(route_name='redis-compiled', renderer="templates/primes.jinja2")
def redis_compiled(request):
    r = redis_connection()
    primes = r.execute_command("primes", LAST_PRIME)
    return {'name': 'Primes computed with a Redis command',
            'primes': ", ".join([prime.decode() for prime in primes])}
