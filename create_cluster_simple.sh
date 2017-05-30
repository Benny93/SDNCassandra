TAG='latest'
echo "Starting container 1"
docker run --name some-cassandra -d cassandra:$TAG
echo "Starting container 2"
docker run --name some-cassandra2 -d --link some-cassandra:cassandra cassandra:$TAG
