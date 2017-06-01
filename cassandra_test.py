#!/usr/bin/env python

from cassandra.cluster import Cluster
# from cassandra.policies import DCAwareRoundRobinPolicy

# constants
KEY_SPACE = 'keyspace_sdn'

# CONNECT TO SESSION

# cluster = Cluster(
#         ['172.17.0.3', '172.17.0.2'],
#         load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='US_EAST'),
#         port=9042)

cluster = Cluster(['172.17.0.3', '172.17.0.2'])
session = cluster.connect()

# session.execute(
#         """
#         INSERT INTO switches (name, IP)
#         VALUES (%s, %s)
#         """,
#         ("John O'Reilly", "192.168.0.1")
# )
#

keyspaces = cluster.metadata.keyspaces
if KEY_SPACE in keyspaces:
    print('Keyspace found {0}').format(KEY_SPACE)
else:
    query_create_keyspace = ('CREATE KEYSPACE {} WITH REPLICATION ='
    + ' {{ {} : {}, {} : {} }};').format(
        KEY_SPACE, "'class'", "'SimpleStrategy'", "'replication_factor'", 3)
    print(query_create_keyspace)
    session.execute(query_create_keyspace)

session.set_keyspace(KEY_SPACE)
