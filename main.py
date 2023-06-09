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

def get_user_choice():
    
    print("\n[1] Add reservation.")
    print("[2] Show your reservations.")
    print("[3] Show all reservations")
    print("[4] Update reservation")
    print("[5] Delete reservation")
    print("[q] Quit.")
    
    return input("What would you like to do? ")

def show_movies(session):
    query = f"SELECT * FROM cinema.movies"
    rows = session.execute(query)

    print(f'MOVIE\tTIME')
    for row in rows:
        print(f'{row.movie_name}\t{row.show_timestamp}')

def avaiable_seats(session, movie):
    all_seats = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
    return all_seats.difference(movie.taken_seats)

def add_reservation(session, username):
    name = f"'{username}'"

    show_movies(session)

    while True:
        try:
            movie = input("\nMovie name: ")
            movie = f"'{movie}'"
            name = f"'{username}'"
            query = f"SELECT * FROM cinema.movies WHERE movie_name = {movie} ALLOW FILTERING;"
            rows = session.execute(query)
            break
        except:
            print("\nWrong movie title was provided. Please try again:")

    free_seats = {}
    taken_seats = {}

    for row in rows:
        free_seats = avaiable_seats(session, row)
        taken_seats = row.taken_seats
    
    if len(free_seats) == 0:
        print("\nThere are no more free seats. Please, select another movie.")
        return
    
    print(f"'\nCurrently avaiable seats: {free_seats}'")

    while True:
        try: 
            seat = int(input("\nPick a seat number: "))
            if seat in free_seats:
                break
            else:
                print("\nPlease take an another seat.")
        except ValueError:
            print("\nThe Seat number must be an integer. Try again:")
    
    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), {name}, {movie}, toTimestamp(now()), {seat});"
    session.execute(query)

    query = f"UPDATE cinema.movies SET taken_seats = taken_seats + {{{seat}}} WHERE movie_name = {movie};"
    session.execute(query)

    print("Successfully added your reservation!")
    time.sleep(1)

def show_your_reservations(session, username):
    name = f"'{username}'"
    query = f"SELECT * FROM cinema.reservations WHERE name = {name} ALLOW FILTERING;"
    rows = session.execute(query)

    row_exist = False
    print(f'RES_ID\tMOVIE_TITLE\tSEAT')
    for row in rows:
        row_exist = True
        print(f'{row.reservation_id}\t{row.movie_name}\t{row.seat_number}')

    return row_exist

def show_all_reservations(session):
    query = f"SELECT * FROM cinema.reservations;"
    rows = session.execute(query)

    print(f'RES_ID\tNAME\tMOVIE_TITLE\tSEAT')
    for row in rows:
        print(f'{row.reservation_id}\t{row.name}\t{row.movie_name}\t{row.seat_number}')

def update_reservation(session, username):
    print("Provide id of reservation you want to update:\n")
    row_exist_check = show_your_reservations(session, username)

    if not row_exist_check:
        print("You don't have any reservations yet. Please add at first a reservation.")
        return

    while True:
        try:
            res_id = input("\nRES_ID: ")
            name = f"'{username}'"
            query = f"SELECT * FROM cinema.reservations WHERE name = {name} AND reservation_id = {res_id} ALLOW FILTERING;"
            rows = session.execute(query)
            break
        except:
            print("Wrong reservation id was provided. Please try again:")

    for row in rows:
        movie = row.movie_name
        seat = row.seat_number
    
    display_title_bar()

    while True:
        try: 
            seat = int(input("Provide new seat number: "))
            break
        except ValueError:
            print("The Seat number must be an integer. Try again:")

    movie = f"'{movie}'"

    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES ({res_id}, {name}, {movie}, toTimestamp(now()), {seat});"
    session.execute(query)

def delete_reservation(session, username):
    print("Provide id of reservation you want to delete:\n")
    row_exist_check = show_your_reservations(session, username)

    if not row_exist_check:
        print("You don't have any reservations yet. Please add at first a reservation.")
        return
    
    while True:
        try:
            res_id = input("\nRES_ID: ")
            name = f"'{username}'"
            query = f"SELECT * FROM cinema.reservations WHERE name = {name} AND reservation_id = {res_id} ALLOW FILTERING;"
            rows = session.execute(query)
            break
        except:
            print("Wrong reservation id was provided. Please try again:")

    movie = ''
    for row in rows:
        movie = row.movie_name
        movie = f"'{movie}'"
        seat = int(row.seat_number)

    
    display_title_bar()
    
    query = f"DELETE FROM cinema.reservations WHERE name = {name} AND movie_name = {movie} AND reservation_id = {res_id} IF EXISTS"
    rows = session.execute(query)

    query = f"UPDATE cinema.movies SET taken_seats = taken_seats - {{{seat}}} WHERE movie_name = {movie};"
    session.execute(query)

    print("Successfully deleted your reservation!")
    time.sleep(1)

def quit_database(session):
    print("\nGood bye.")


### MAIN ###

#Connect to Cassandra

clstr=Cluster()         #TODO Error Handling
session=clstr.connect() #TODO Error Handling

### APPLICATION ###

display_title_bar()
user = login_to_database()

choice = ''
display_title_bar()
while choice != 'q':
    
    choice = get_user_choice()

    # Respond to the user's choice.
    display_title_bar()
    if choice == '1':
        add_reservation(session, user)
    elif choice == '2':
        show_your_reservations(session, user)
    elif choice == '3':
        show_all_reservations(session)
    elif choice == '4':
        update_reservation(session, user)
    elif choice == '5':
        delete_reservation(session, user)
    elif choice == 'q':
        quit_database(session)
        break
    else:
        print("\nI don't understand that choice. Please try again:\n")


