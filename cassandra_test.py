from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

cluster = Cluster(
        ['172.17.0.3', '172.17.0.2'],
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='US_EAST'),
        port=9042)
session = cluster.connect()
session.set_keyspace('keyspace_sdn')

session.execute(
        """
        INSERT INTO switches (name, IP)
        VALUES (%s, %s)
        """,
        ("John O'Reilly", "192.168.0.1")
)
