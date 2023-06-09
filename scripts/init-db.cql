CREATE KEYSPACE cinema WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
USE cinema;

CREATE TABLE movies (movie_name text, show_timestamp timestamp, taken_seats set<int>, PRIMARY KEY (movie_name, show_timestamp));

INSERT INTO movies(movie_name, show_timestamp, taken_seats) VALUES ('X', '2023-06-13 08:00', {});
INSERT INTO movies(movie_name, show_timestamp, taken_seats) VALUES ('Y', '2023-06-13 10:00', {});

CREATE TABLE reservations (reservation_id uuid, name text, movie_name text, reservation_timestamp timestamp, seat_number int, PRIMARY KEY (name, movie_name, reservation_id));

INSERT INTO reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), 'A B', 'X', currentTimestamp(), 3);
INSERT INTO reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), 'A B', 'Y', currentTimestamp(), 5);

UPDATE movies SET taken_seats = taken_seats + {3} WHERE movie_name = 'X' AND show_timestamp = '2023-06-13 08:00';
UPDATE movies SET taken_seats = taken_seats + {5} WHERE movie_name = 'Y' AND show_timestamp = '2023-06-13 10:00';
