import ast
import json

from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException, QueryException


class MacToPortDB(Model):
    """
    Used to store dictionary mac_to_port
    Example: {1234: {44: 7, 55: 6}}

    """
    # TODO: consider using UUID again
    # id = columns.UUID(primary_key=True)
    dpid = columns.Integer(primary_key=True)
    port_by_src = columns.Map(columns.Text, columns.Text)


def drop_dict():
    """
Drops dictionary
    """
    drop_table(MacToPortDB)


class VState(object):
    """
Abstraction of cassandra db access. Represents global network state
    """
    # class constants
    KEY_SPACE = 'keyspace_sdn'
    TABLE_NAME = 'dict'

    def __init__(self):
        # CONNECT TO SESSION
        connection.setup(['10.0.0.1', '10.0.0.2'], 'cqlengine')
        manage_keyspace(self.KEY_SPACE, connection.cluster, connection.session)
        self.model = MacToPortDB()
        MacToPortDB.__keyspace__ = self.KEY_SPACE
        # ...and create your CQL table
        self.model.update()
        sync_table(MacToPortDB)

    def update_dict(self, dpid, dictionary):
        """
Saves dictionary in cassandra db
        :param dictionary:
        """
        try:
            self.model.objects(dpid=dpid).if_exists().update(port_by_src=dictionary)
            # switches = self.model.if_exists().update(**dictionary)
            # switches.save()
        except LWTException as e:
            print e.message
            pass

    def get_dict(self, dpid):
        """
Returns dictionary
        """
        # check if dict is available
        try:
            dict_res = dict(self.model.objects.get(dpid=dpid))
            # TODO: Fix unicode problems. This is a quickfix
            return ast.literal_eval(json.dumps(dict_res['port_by_src']))
        #            return dict_res['port_by_src']
        except QueryException as e:
            # try to create table
            try:
                dict_res = self.model.if_not_exists().create(dpid=dpid, port_by_src={})
                dict_res.save()
                return dict_res['port_by_src']
            except LWTException as e:
                # handle failure case
                print e.existing  # existing object
        # return empty
        return {}


# End of class

def manage_keyspace(key_space, cluster, session):
    # Special KEYSPACE query
    """
Set sdn namespace to current namespace. If namespace does not exist -> create
    :param key_space: Name of the keyspace
    :param cluster: Cluster of this session
    :param session: Session
    """
    query_create_keyspace = ('CREATE KEYSPACE {} WITH REPLICATION =' +
                             ' {{ {} : {}, {} : {} }};').format(
        key_space, "'class'", "'SimpleStrategy'",
        "'replication_factor'", 3)
    # Keyspaces
    keyspaces = cluster.metadata.keyspaces
    if key_space in keyspaces:
        print 'Keyspace found {0}'.format(key_space)
    else:
        print(query_create_keyspace)
        session.execute(query_create_keyspace)
    session.set_keyspace(key_space)


def prepare_queries(session, query_by_name, table_name):
    # Queries for creation and drop
    """

    :param session:
    :param query_by_name:
    :param table_name:
    """
    query_by_name.setdefault('create_table', {})
    query_by_name['create_table'] = session.prepare(
        "CREATE TABLE " + table_name +
        " (" + "dict" + " VARCHAR PRIMARY KEY);")
    query_by_name.setdefault('delete_table', {})
    query_by_name['delete_table'] = session.prepare("DROP TABLE " + table_name + ";")

# Test and Debug area
# mystate = VState()
# res = mystate.get_dict(1)
# res['a'] = 'b'
# mystate.update_dict(1, res)
# res = mystate.get_dict(1)
