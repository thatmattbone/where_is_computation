from pyramid.view import view_config

from sqlalchemy import select, func

import redis

from .models import DBSession
from .sieve import sieve, sieve_lua, ONE_HUNDRED_PRIME_STRINGS, LAST_PRIME
from .decorators import update_with_func_info

def redis_connection():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r


@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    return {}


@view_config(route_name='precomputed', renderer="templates/precomputed.jinja2")
@update_with_func_info
def precomputed(request):
    """
    Because finding primes (especially the first 100 primes) has been
    done many times before, we can simply lookup the answer and
    hardcode it into a template. While this doesn't really count as
    'computation,' it still can be useful by serving as an acceptance
    test for the other techniques.
    """

    return {'name': 'Precomputed Primes'}


@view_config(route_name='serverside', renderer="templates/primes.jinja2")
@update_with_func_info
def serverside(request):
    """
    Using a [sieve implementation in
    python](https://github.com/thatmattbone/where_is_computation/blob/master/WhereIsComputation/whereiscomputation/sieve.py#L8)
    we can perform the computation on the server-side and send the
    results over the wire. While performing computations on the
    server-side increases the burden on servers, it can increase
    responsiveness and make the use of lighter-weight clients
    possible.
    """

    return {'name': 'Primes computed on the server-side',
            'primes': ", ".join([str(prime) for prime in sieve(LAST_PRIME)])}


@view_config(route_name='clientside', renderer="templates/primes_clientside.jinja2")
@update_with_func_info
def clientside(request):
    """
    Using a [sieve implementation in
    javascript](https://github.com/thatmattbone/where_is_computation/blob/master/WhereIsComputation/whereiscomputation/static/js/sieve.js)
    it's fairly simple to perform the computation of the first 100
    primes on the client-side. This has the advantage of farming out
    the work to each client loading the page.
    """

    return {'name': 'Primes computed on the client-side'}


@view_config(route_name='server-and-clientside', renderer="templates/primes_clientside.jinja2")
@update_with_func_info
def server_and_clientside(request):
    """
    Combining the server-side and client-side examples, we can perform
    the computation in both places.  In this particular example, we
    only calculate a subset of the results on the serve-side and then
    re-do the entire computation on the client-side. While not an
    exceedlingly practical example, performing computations in both
    places can be useful when considering trade-offs between server
    and client resources.
    """

    return {'name': 'Primes computed on the client and server-side',
            'primes': ", ".join([str(prime) for prime in sieve(100)])}


@view_config(route_name='database-layer', renderer="templates/primes.jinja2")
@update_with_func_info
def database_layer(request):
    """
    The data layer of web applications is also capable of performing
    computation. Using
    [plpython3u](http://www.postgresql.org/docs/9.2/static/plpython.html)
    in postgres we can create a [postgres function in
    python](https://github.com/thatmattbone/where_is_computation/blob/master/WhereIsComputation/whereiscomputation/sieve.py#L51)
    and compute our primes.
    """

    session = DBSession()
    primes = session.execute(select([func.prime_sieve(LAST_PRIME)])).fetchall()[0][0]

    return {'name': 'Primes computed in Postgres',
            'primes': ", ".join([str(prime) for prime in primes])}


@view_config(route_name='redis-script', renderer="templates/primes.jinja2")
@update_with_func_info
def redis_script(request):
    """
    Not all web applictions use a relational database as their data
    layer, but many nosql databases are also capable of performing
    computations. Using redis' support for lua scripts we can
    [implement our sieve in
    lua](https://github.com/thatmattbone/where_is_computation/blob/master/WhereIsComputation/whereiscomputation/sieve.py#L27)
    and compute the first 100 primes.
    """

    r = redis_connection()
    sieve = r.register_script(sieve_lua)
    primes = sieve(args=[LAST_PRIME])

    return {'name': 'Primes computed with a Redis script',
            'primes': ", ".join([str(prime) for prime in primes])}


@view_config(route_name='redis-compiled', renderer="templates/primes.jinja2")
@update_with_func_info
def redis_compiled(request):
    """
    For the truly absurd, we can forgo scripting our nosql database
    and [simply hack
    it](https://github.com/thatmattbone/where_is_computation/blob/master/redis/sieve.patch)
    to do what we want. Here our primes are computed by implementing a
    custom redis command called `PRIMES` in C.
    """

    r = redis_connection()
    primes = r.execute_command("primes", LAST_PRIME)

    return {'name': 'Primes computed with a Redis command',
            'primes': ", ".join([prime.decode() for prime in primes])}
