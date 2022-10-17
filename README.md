# Kafka topics

```
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic block
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic transaction
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic contractlog
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic contractevent
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic solidity
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic solidityevent
kafka-topics.sh --create --replication-factor 1 --bootstrap-server kafka:9092 --partitions 1 --topic soliditylog
```

## delete

```
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic block
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic transaction
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic contractlog
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic contractevent
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic solidity
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic solidityevent
kafka-topics.sh --delete --bootstrap-server kafka:9092 --topic soliditylog
```

# Kafka

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install kafka \
    --atomic \
    --set persistence.storageClass=local-storage \
    --set persistence.size=400Gi \
    --set zookeeper.persistence.storageClass=local-storage \
    --set zookeeper.persistence.size=10Gi \
    --set deleteTopicEnable=true \
    --namespace tronql \
    bitnami/kafka
```
