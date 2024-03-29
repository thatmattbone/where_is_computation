import os
import sys
import transaction
from zope.sqlalchemy import mark_changed

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import DBSession
from ..sieve import postgres_prime_sieve_function

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    session = DBSession()
    conn = session.connection()
    conn.execute(postgres_prime_sieve_function)
    mark_changed(session)
    transaction.commit()
