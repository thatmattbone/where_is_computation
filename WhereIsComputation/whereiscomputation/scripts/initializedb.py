import os
import sys
import transaction
from zope.sqlalchemy import mark_changed

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    MyModel,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

my_one_function = """
CREATE OR REPLACE FUNCTION my_one()
  RETURNS integer AS
$BODY$
one = 1
return one
$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
-- ALTER FUNCTION my_one()
--   OWNER TO whereiscomputation;
"""

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)


    session = DBSession()
    conn = session.connection()
    conn.execute(my_one_function)
    mark_changed(session)
    transaction.commit()

    #with transaction.manager:
    #    model = MyModel(name='one', value=1)
    #    DBSession.add(model)
    #    import pdb; pdb.set_trace()
