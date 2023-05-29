# Wait for Cassandra to initilize
until printf "" 2>>/dev/null >>/dev/tcp/cassandra/9042; do 
    sleep 5;
    echo "Waiting for Cassandra...";
done

# Create a keyspace
cqlsh -e "CREATE KEYSPACE cinema WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};"
# Create a table
cqlsh -e "USE cinema; CREATE TABLE booking (id UUID PRIMARY KEY, data text);"
