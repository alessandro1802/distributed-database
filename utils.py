import time

def get_all_movies(session):
    query = f"SELECT * FROM cinema.movies"
    return list(session.execute(query))

def avaiable_seats(session, movie_name):
    query = f"SELECT taken_seats FROM movies WHERE movie_name = '{movie_name}';"
    row = session.execute(query).one()
    all_seats = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
    if not (taken_seats := row.taken_seats):
        # raise Exception("AAAAAA")
        taken_seats = set()
    return all_seats.difference(taken_seats)

def add_reservation(username, session, movie_name, seat):
    if seat not in avaiable_seats(session, movie_name):
        raise Exception("The seat is not available.")
    # Remove the seat from available
    query = f"UPDATE cinema.movies SET taken_seats = taken_seats + {{{seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)
    # Add reservation
    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), '{username}', '{movie_name}', toTimestamp(now()), {seat});"
    session.execute(query)

def get_all_reservations(username, session):
    query = f"SELECT * FROM cinema.reservations WHERE name = '{username}';"
    return list(session.execute(query))

def update_reservation(username, session, res_id, movie_name, current_seat, new_seat): 
    # Add new seat to taken
    query = f"UPDATE movies SET taken_seats = taken_seats + {{{new_seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)
    # Update reservation
    query = f"UPDATE reservations SET seat_number = {new_seat}, reservation_timestamp = currentTimestamp() WHERE name = '{username}' and reservation_id = {res_id};"
    session.execute(query)
    # Remove old seat from taken
    query = f"UPDATE movies SET taken_seats = taken_seats - {{{current_seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)

def delete_reservation(username, session, res_id, movie_name, seat):
    # Remove the reservation
    query = f"DELETE FROM cinema.reservations WHERE name = '{username}' AND reservation_id = {res_id};"
    session.execute(query)
    # Free the seat
    query = f"UPDATE cinema.movies SET taken_seats = taken_seats - {{{seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)