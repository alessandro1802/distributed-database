CREATE KEYSPACE cinema WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
USE cinema;

CREATE TABLE reservations (reservation_id uuid, name text, movie_name text, reservation_timestamp timestamp, seat_number int, PRIMARY KEY (name, movie_name, reservation_id));

INSERT INTO reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), 'A B', 'X', currentTimestamp(), 1);
INSERT INTO reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), 'A B', 'Y', currentTimestamp(), 1);
