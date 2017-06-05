#!/usr/bin/env python
import sys
import time
from cassandra.cluster import Cluster
import util_functions
# constants
KEY_SPACE = 'keyspace_sdn'
SWITCH_TABLE_NAME = 'switches'
SWITCH_TABLE_ATTR1_NAME = 'ip_addr'
SWITCH_TABLE_ATTR2_NAME = 'controller_ip'
SWITCH_TABLE_ATTR3_NAME = 'table_name'

# CONNECT TO SESSION
#cluster = Cluster(['172.17.0.3', '172.17.0.2'])
cluster = Cluster(['172.17.0.3'])
session = cluster.connect()

# Special KEYSPACE query
query_create_keyspace = ('CREATE KEYSPACE {} WITH REPLICATION =' +
                         ' {{ {} : {}, {} : {} }};').format(
    KEY_SPACE, "'class'", "'SimpleStrategy'",
    "'replication_factor'", 3)

# Keyspaces
keyspaces = cluster.metadata.keyspaces
if KEY_SPACE in keyspaces:
    print 'Keyspace found {0}'.format(KEY_SPACE)
else:
    print(query_create_keyspace)
    session.execute(query_create_keyspace)
session.set_keyspace(KEY_SPACE)

# Queries for creation and drop
query_create_table_switch = session.prepare(
    "CREATE TABLE " + SWITCH_TABLE_NAME +
    " (" + SWITCH_TABLE_ATTR1_NAME + " VARCHAR PRIMARY KEY, " +
    SWITCH_TABLE_ATTR2_NAME + " VARCHAR, " +
    SWITCH_TABLE_ATTR3_NAME + " VARCHAR);")
query_delete_table_switches = session.prepare("DROP TABLE " + SWITCH_TABLE_NAME + ";")


# manage_table_switches():
# Create table switches, delete if existing
ks = keyspaces.get(KEY_SPACE)
table = ks.tables.get(SWITCH_TABLE_NAME)

if table:
    # clear table
    print "Table "+SWITCH_TABLE_NAME+" already exists"
    session.execute(query_delete_table_switches)
session.execute(query_create_table_switch)

# Queries for modification
query_insert_into_switches = session.prepare(
    "INSERT INTO " + SWITCH_TABLE_NAME + " (" + SWITCH_TABLE_ATTR1_NAME + ", " +
    SWITCH_TABLE_ATTR2_NAME + ", " +
    SWITCH_TABLE_ATTR3_NAME + ") " +
    "VALUES (?, ?, ?);")
query_select_all_from_switches = session.prepare("SELECT * FROM " + SWITCH_TABLE_NAME + ";")


# insert DATA
session.execute(query_insert_into_switches, ('2017:db8::f102', '2017:db8::f201', 'f102_db'))
session.execute(query_insert_into_switches, ('2017:db8::f103', '2017:db8::f201', 'f103_db'))
# read out DATA
try:
    while True:
        print(str(query_select_all_from_switches))
        table_switches = session.execute(query_select_all_from_switches)
        print util_functions.pprinttable(table_switches.current_rows)
        """
        for row in table_switches:
            row_formatted = "{}:{}, {}:{}, {}:{}".format(SWITCH_TABLE_ATTR1_NAME,getattr(row,SWITCH_TABLE_ATTR1_NAME),
                                                         SWITCH_TABLE_ATTR2_NAME, getattr(row, SWITCH_TABLE_ATTR2_NAME),
                                                         SWITCH_TABLE_ATTR3_NAME, getattr(row, SWITCH_TABLE_ATTR3_NAME),
                                                         )
            print row_formatted
        """
        print "Sleeping for 2 seconds"
        time.sleep(2)
except KeyboardInterrupt:
    print "Warning: Caught KeyboardInterrupt"
    #sys.exit(0)
