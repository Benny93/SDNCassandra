#!/usr/bin/env python
import sys
import time
from cassandra.cluster import Cluster

# constants
KEY_SPACE = 'keyspace_sdn'


def prepare_queries():
    global query_create_keyspace, create_table_switch_stmt, delete_table_switches_stmt, insert_into_switches_stmt, select_all_from_switches_stmt
    # Queries
    create_table_switch_stmt = session.prepare(
        "CREATE TABLE Switches (ip_addr VARCHAR PRIMARY KEY, is_managed BOOLEAN, table_name VARCHAR);")
    delete_table_switches_stmt = session.prepare("DROP TABLE Switches;")
    insert_into_switches_stmt = session.prepare(
        "INSERT INTO Switches (ip_addr, is_managed, table_name) VALUES (?, ?, ?);")
    select_all_from_switches_stmt = session.prepare("SELECT * FROM Switches;")


def manage_keyspace():
    global keyspaces
    query_create_keyspace = ('CREATE KEYSPACE {} WITH REPLICATION =' +
                             ' {{ {} : {}, {} : {} }};').format(
        KEY_SPACE, "'class'", "'SimpleStrategy'",
        "'replication_factor'", 3)
    keyspaces = cluster.metadata.keyspaces
    if KEY_SPACE in keyspaces:
        print 'Keyspace found {0}'.format(KEY_SPACE)
    else:
        print(query_create_keyspace)
        session.execute(query_create_keyspace)
    session.set_keyspace(KEY_SPACE)


def manage_table_switches():
    # Create table switches, delete if existing
    ks = keyspaces.get("keyspace_sdn")
    table = ks.tables.get("mytable")
    if table:
        # clear table
        session.execute(delete_table_switch_stmst)
    session.execute(create_table_switch_stmt)


# MAIN
if __name__ == '__main__':
    # CONNECT TO SESSION
    cluster = Cluster(['172.17.0.3', '172.17.0.2'])
    session = cluster.connect()
    # manage keyspace
    manage_keyspace()
    # prepare queries
    prepare_queries()
    manage_table_switches()
    # insert DATA
    session.execute(insert_into_switches_stmt, ('2017:db8::f102', True, 'f102_db'))
    # read out DATA
    try:
        while True:
            print(str(select_all_from_switches_stmt))
            stable = session.execute(select_all_from_switches_stmt)
            print stable
            print "Sleeping for 2 seconds"
            time.sleep(2)
    except KeyboardInterrupt:
        print "Warning: Caught KeyboardInterrupt"
        sys.exit(0)
