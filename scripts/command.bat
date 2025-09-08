# run kafka broker
docker run -d -p 9092:9092 --name broker apache/kafka:latest

# network for elastic and kibana
docker network create elastic-network

# run mongo db
docker run -d -p 27017:27017 --name mongo mongodb/mongodb-community-server:latest

# run elasticsearch
docker run -d --name es -p 9200:9200 --network=elastic-network -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" docker.elastic.co/elasticsearch/elasticsearch:8.15.0

# run kibana
docker run -d --name kibana --network=elastic-network -p 5601:5601  -e "ELASTICSEARCH_HOSTS=http://es:9200" docker.elastic.co/kibana/kibana:8.15.0