import logging
import json
log = logging.getLogger(__name__)

try:
    import rethinkdb as r
    has_rethinkdb = True
except ImportError:
    log.error('fail to initialize rethinkdb_returner')
    has_rethinkdb = False

def __virtual__():
    if not has_rethinkdb:
        return False
    return 'rethinkdb'

def ext_pillar(minion_id, pillar, *args, **kwargs):
    options = __salt__['config.option']('rethinkdb')
    host_addr = options['host']
    log.error(host_addr)
    db_name = options['db']
    log.error(db_name)
    table_name = options['pillar']
    log.error(table_name)
    conn = r.connect(host=host_addr, db=db_name)
    if table_name not in r.table_list().run(conn):
        log.warning('do not exist table')
        r.table_create(table_name).run(conn)
        log.info('create new table')

    result = r.table(table_name).filter({'minion': minion_id})

    return result
