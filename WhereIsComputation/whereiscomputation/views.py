from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

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

@view_config(route_name='precomputed', renderer="templates/stub.jinja2")
def precomputed(request):
    return {}


@view_config(route_name='serverside', renderer="templates/stub.jinja2")
def serverside(request):
    return {}


@view_config(route_name='serverside-with-cache', renderer="templates/stub.jinja2")
def serverside_with_cache(request):
    return {}


@view_config(route_name='clientside', renderer="templates/stub.jinja2")
def clientside(request):
    return {}


@view_config(route_name='server-and-clientside', renderer="templates/stub.jinja2")
def server_and_clientside(request):
    return {}

@view_config(route_name='database-layer', renderer="templates/stub.jinja2")
def database_layer(request):
    return {}
