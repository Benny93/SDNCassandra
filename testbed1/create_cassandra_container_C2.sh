#!/usr/bin/env bash
TAG='latest'
name_app1="cassandra2"
# Ports to publish
PUB_PORT='9042'
CLUSTER_PARTNER_IP='172.17.0.10'

if docker ps | awk 'NR>1{  ($(NF) == '${name_app1}' )  }'; then
    docker stop "$name_app1"
    docker rm -f "$name_app1"
    docker network disconnect bridge "$name_app1"
fi

echo "Starting container "${name_app1}
docker run --name ${name_app1} -p ${PUB_PORT} -d -e CASSANDRA_SEEDS="'$CLUSTER_PARTNER_IP'" cassandra:${TAG}
