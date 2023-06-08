CREATE KEYSPACE cinema WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
USE cinema;
CREATE TABLE booking (id UUID PRIMARY KEY, first_name text, last_name text, movie_name text, reservation_timestamp timestamp, show_timestamp timestamp, room int, seat int);
