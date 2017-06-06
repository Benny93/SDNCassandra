#!/usr/bin/env bash
TAG='latest'
name_app1="cassandra1"
# Ports to publish
PUB_PORT='9042'
IP='10.0.0.1'
CLUSTER_PARTNER_IP='10.0.0.2'

if docker ps | awk 'NR>1{  ($(NF) == '${name_app1}' )  }'; then
    docker stop "$name_app1"
    docker rm -f "$name_app1"
    docker network disconnect bridge "$name_app1"
fi

echo "Starting container "${name_app1}
# docker run --name ${name_app1} -p ${PUB_PORT} -d -e CASSANDRA_SEEDS="'$CLUSTER_PARTNER_IP'" cassandra:${TAG}
# docker run --name ${name_app1} -p ${PUB_PORT} -d  cassandra:${TAG}
# docker run --name ${name_app1} --publish-all=true -d  cassandra:${TAG}

docker run --name ${name_app1} -d -e CASSANDRA_BROADCAST_ADDRESS=${IP} -p 7000:7000 cassandra:${TAG}

