from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('index', '/')
    config.add_route('precomputed', '/precomputed')
    config.add_route('serverside', '/serverside')
    config.add_route('serverside-with-cache', '/serverside-with-cache')
    config.add_route('clientside', '/clientside')
    config.add_route('server-and-clientside', 'server-and-clientside')
    config.add_route('database-layer', '/database-layer')

    config.scan()
    return config.make_wsgi_app()

