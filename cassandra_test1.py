#!/usr/bin/env python

from cassandra.cluster import Cluster
# from cassandra.policies import DCAwareRoundRobinPolicy

# constants
KEY_SPACE = 'keyspace_sdn'

# CONNECT TO SESSION
cluster = Cluster(['172.17.0.3', '172.17.0.2'])
session = cluster.connect()

# Queries
query_create_keyspace = ('CREATE KEYSPACE {} WITH REPLICATION =' +
                         ' {{ {} : {}, {} : {} }};').format(
                             KEY_SPACE, "'class'", "'SimpleStrategy'",
                             "'replication_factor'", 3)
create_table_switch_stmt = session.prepare("CREATE TABLE Switches (ip_addr VARCHAR PRIMARY KEY, is_managed BOOLEAN, table_name VARCHAR);")
delete_table_switch_stmst = session.prepare("DROP TABLE Switches;")
insert_into_tswitch_stmt = session.prepare("INSERT INTO Switches (ip_addr, is_managed, table_name) VALUES (?, ?, ?);")
# check keyspace
keyspaces = cluster.metadata.keyspaces
if KEY_SPACE in keyspaces:
    print('Keyspace found {0}').format(KEY_SPACE)
else:
    print(query_create_keyspace)
    session.execute(query_create_keyspace)

session.set_keyspace(KEY_SPACE)
# Create table switches, delete if existing
ks = keyspaces.get("keyspace_sdn")
table = ks.tables.get("mytable")
if table:
    #clear table
    session.execute(delete_table_switch_stmst);
session.execute(create_table_switch_stmt);

#insert DATA


