TAG='latest'
name_app1="some-cassandra"
name_app2="some-cassandra2"
# Ports to publish
PUB_PORT='9042'


if docker ps | awk -v name_app1="name_app1" 'NR>1{  ($(NF) == name_app1 )  }'; then
    docker stop "$name_app1"
    docker rm -f "$name_app1"
fi
if docker ps | awk -v name_app2="name_app2" 'NR>1{  ($(NF) == name_app2 )  }'; then
    docker stop "$name_app2"
    docker rm -f "$name_app2"
fi

echo "Starting container 1"
docker run --name $name_app1 -p $PUB_PORT -d cassandra:$TAG
echo "sleeping ..."
sleep 3
echo "Starting container 2"
#docker run --name $name_app2 -d --link $name_app1:cassandra cassandra:$TAG
docker run --name $name_app2 -p $PUB_PORT -d -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' $name_app1)" cassandra:$TAG
