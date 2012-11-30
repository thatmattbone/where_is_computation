from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )
from .sieve import sieve, ONE_HUNDRED_PRIMES, ONE_HUNDRED_PRIME_STRINGS

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one':one, 'project':'WhereIsComputation'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_WhereIsComputation_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='precomputed', renderer="templates/primes.jinja2")
def precomputed(request):
    return {'name': 'Precomputed Primes',
            'primes': ", ".join(ONE_HUNDRED_PRIME_STRINGS)}


@view_config(route_name='serverside', renderer="templates/primes.jinja2")
def serverside(request):
    return {'name': 'Primes computed on the server-side',
            'primes': ", ".join([str(prime) for prime in sieve(ONE_HUNDRED_PRIMES[-1])])}


@view_config(route_name='serverside-with-cache', renderer="templates/primes.jinja2")
def serverside_with_cache(request):
    return {'name': 'Primes computed on the server-side with a caching layer'}


@view_config(route_name='clientside', renderer="templates/primes.jinja2")
def clientside(request):
    return {'name': 'Primes computed on the client-side'}


@view_config(route_name='server-and-clientside', renderer="templates/primes.jinja2")
def server_and_clientside(request):
    return {'name': 'Primes computed on the client and server-side'}


@view_config(route_name='database-layer', renderer="templates/primes.jinja2")
def database_layer(request):
    return {'name': 'Primes computed in the database layer'}
