#!/usr/bin/env bash
TAG='latest'
# Ports to publish
CQL_PORT='9042'
INTER_NODE_PORT='7000'
#vars
CONTAINER_NAME=""
IP=""
CLUSTER_PARTNER_IP=""
ENV_VARS=""

# Set variables by hostname
case $(hostname -s) in
     *1) # Controller 1 runs this script
        CONTAINER_NAME="cassandra1"
        IP='10.0.0.1'
        CLUSTER_PARTNER_IP='10.0.0.2'
        ENV_VARS="-e CASSANDRA_BROADCAST_ADDRESS="${IP}
     ;;
     *2) # Controller 2
         CONTAINER_NAME="cassandra2"
         IP='10.0.0.2'
         CLUSTER_PARTNER_IP='10.0.0.1'
         ENV_VARS='-e CASSANDRA_BROADCAST_ADDRESS='${IP}' -e CASSANDRA_SEEDS='${CLUSTER_PARTNER_IP}
     ;;
esac



# TODO fix this if
if docker ps | awk 'NR>1{  ($(NF) == '${CONTAINER_NAME}' )  }'; then
    docker stop "$CONTAINER_NAME"
    docker rm -f "$CONTAINER_NAME"
    docker network disconnect bridge "$CONTAINER_NAME"
fi

echo "Starting container "${CONTAINER_NAME}
#echo "docker run --name "${CONTAINER_NAME}" -d "${ENV_VARS}" -p "${IP}"::"${CQL_PORT}" -p "${IP}"::"${INTER_NODE_PORT}" cassandra:"${TAG}
docker run --name ${CONTAINER_NAME} -d ${ENV_VARS} -p ${CQL_PORT}:${CQL_PORT} -p ${INTER_NODE_PORT}:${INTER_NODE_PORT} cassandra:${TAG}
