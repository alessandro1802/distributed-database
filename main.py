from cassandra.cluster import Cluster
import datetime
import os
import time

### FUNCTIONS ###

def display_title_bar():
    os.system('clear')
    print("\t*************************")
    print("\t***  Cinema Database  ***")
    print("\t*************************")

def login_to_database():
    return input("Provide your unique username: ")

def quit_database(session):
    print("\nGood bye.")

def get_user_choice():
    print("\n[1] Add reservation.")
    print("[2] Show your reservations.")
    print("[3] Show specific reservation")
    print("[4] Update reservation")
    print("[5] Delete reservation")
    print("[q] Quit.")
    return input("What would you like to do? ")

def get_all_movies(session):
    query = f"SELECT * FROM cinema.movies"
    return list(session.execute(query))

def show_movies(session):
    rows = get_all_movies(session)
    print(f'MOVIE, \tTIME')
    for row in rows:
        print(f'{row.movie_name}, \t{row.show_timestamp}')
    return rows

def avaiable_seats(session, movie_name):
    query = f"SELECT taken_seats FROM movies WHERE movie_name = '{movie_name}';"
    row = session.execute(query).one()
    all_seats = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
    return all_seats.difference(row.taken_seats)

def add_reservation(session, username):
    # Show movies for selection
    rows = show_movies(session)
    movie_names = [row.movie_name for row in rows]

    # Select a movie
    while True:
        movie_name = input("\nMovie name: ")
        if movie_name in movie_names:
            break
        else:
            print("\nWrong movie title was provided. Please try again:")

    # Get available seats
    free_seats = avaiable_seats(session, movie_name)
    if len(free_seats) == 0:
        print("\nThere are no more free seats. Please, select another movie.")
        return
    print(f"\nCurrently avaiable seats: {free_seats}")

    # Select a seat
    while True:
        try: 
            seat = int(input("\nPick a seat number: "))
        except ValueError:
            print("\nThe Seat number must be an integer. Try again:")
        if seat in free_seats:
            break
        else:
            print("\nPlease take an another seat.")

    # Add reservation
    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), '{username}', '{movie_name}', toTimestamp(now()), {seat});"
    session.execute(query)
    # Remove the seat from available
    query = f"UPDATE cinema.movies SET taken_seats = taken_seats + {{{seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)

    time.sleep(1)
    print("Successfully added your reservation!")
    return

def get_all_reservations(username, session):
    query = f"SELECT * FROM cinema.reservations WHERE name = '{username}';"
    return list(session.execute(query))

def get_one_reservation(session, username):
    all_reservations = get_all_reservations(username, session)
    # Select the reservation for the update
    reservation_ids = [str(row.reservation_id) for row in all_reservations]
    while True:
        print("Provide id of reservation you want to update:\n")
        res_id = input("\nRES_ID: ")
        if res_id in reservation_ids:
            break
        else:
            print("Wrong reservation id was provided. Please try again:")
    
    query = f"SELECT * FROM cinema.reservations WHERE name = '{username}' and reservation_id = {res_id};"
    return session.execute(query).one()

def update_reservation(session, username):
    all_reservations = get_all_reservations(username, session)
    
    # Check if user has any reservations
    if not all_reservations:
        print("You don't have any reservations yet.")
        return
    
    # Select the reservation for the update
    reservation_ids = {str(row.reservation_id): [row.movie_name, int(row.seat_number)] for row in all_reservations}
    while True:
        print("Provide id of reservation you want to update:\n")
        res_id = input("\nRES_ID: ")
        if res_id in reservation_ids:
            break
        else:
            print("Wrong reservation id was provided. Please try again:")
    movie_name, current_seat = reservation_ids[res_id]
    
    # Select new seat
    free_seats = avaiable_seats(session, movie_name)
    if len(free_seats) == 0:
        print("\nThere are no more free seats. You can't change a seat.")
        time.sleep(1)
        return
    display_title_bar()
    print(f"\nCurrently avaiable seats: {free_seats}")
    while True:
        try: 
            new_seat = int(input("Provide new seat number: "))
        except ValueError:
            print("The Seat number must be an integer. Try again:")
        if new_seat not in free_seats:
            print("\nPlease take an another seat.")
        else:
            break
    
    # Update reservation
    query = f"UPDATE reservations SET seat_number = {new_seat}, reservation_timestamp = currentTimestamp() WHERE name = '{username}' and reservation_id = {res_id};"
    session.execute(query)
    # Remove old seat from taken
    query = f"UPDATE movies SET taken_seats = taken_seats - {{{current_seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)
    # Add new seat to taken
    query = f"UPDATE movies SET taken_seats = taken_seats + {{{new_seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)
    
    time.sleep(1)
    print("Successfully updated your reservation!")
    return 

def delete_reservation(session, username):
    all_reservations = get_all_reservations(username, session)
    
    # Check if user has any reservations
    if not all_reservations:
        print("You don't have any reservations yet.")
        return
    
    # Select the reservation for the update
    reservation_ids = {str(row.reservation_id): [row.movie_name, int(row.seat_number)] for row in all_reservations}
    while True:
        print("Provide id of reservation you want to delete:\n")
        print("Warning! It can't be undone. The cancellation is irreversible.")
        res_id = input("\nRES_ID: ")
        if res_id in reservation_ids:
            break
        else:
            print("Wrong reservation id was provided. Please try again:")
    movie_name, current_seat = reservation_ids[res_id]

    # display_title_bar()
    
    # Remove the reservation
    query = f"DELETE FROM cinema.reservations WHERE name = '{username}' AND reservation_id = {res_id};"
    rows = session.execute(query)
    # Free the seat
    query = f"UPDATE cinema.movies SET taken_seats = taken_seats - {{{current_seat}}} WHERE movie_name = '{movie_name}';"
    session.execute(query)

    time.sleep(1)
    print("Successfully deleted your reservation!")
    return


### MAIN ###

#Connect to Cassandra
keyspace = 'cinema'
#TODO Error Handling
clstr = Cluster() 
session = clstr.connect(keyspace)

### APPLICATION ###

display_title_bar()
user = login_to_database()

display_title_bar()
choice = ''
while True:
    # display_title_bar()
    choice = get_user_choice()
    # Respond to the user's choice.
    if choice == '1':
        add_reservation(session, user)
    elif choice == '2':
        rows = get_all_reservations(user, session)
        if not rows:
            print("You don't have any reservations yet.")
        else:
            print("Reservation ID, \tMovie name, \tSeat")
            for row in rows:
                print(f'{row.reservation_id}, \t{row.movie_name}, \t{row.seat_number}')
    elif choice == '3':
        row = get_one_reservation(session, user)
        print("Movie name, \tSeat, \tReservation timestamp")
        print(f'{row.movie_name}, \t{row.seat_number}, \t{row.reservation_timestamp}')
    elif choice == '4':
        update_reservation(session, user)
    elif choice == '5':
        delete_reservation(session, user)
    elif choice == 'q':
        quit_database(session)
        break
    else:
        print("\nI don't understand that choice. Please try again:\n")