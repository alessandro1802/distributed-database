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

def add_reservation(session, username):
    name = f"'{username}'"

    movie = input("Movie name: ")
    movie = f"'{movie}'" 
    seat = input("Seat: ") #TODO Error Handling
    
    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES (uuid(), {name}, {movie}, toTimestamp(now()), {int(seat)});"
    session.execute(query)


def show_your_reservations(session, username):
    name = f"'{username}'"
    query = f"SELECT * FROM cinema.reservations WHERE name = {name} ALLOW FILTERING;"
    rows = session.execute(query)

    print(f'RES_ID\tMOVIE_TITLE\tSEAT')
    for row in rows:
        print(f'{row.reservation_id}\t{row.movie_name}\t{row.seat_number}')

def show_all_reservations(session):
    query = f"SELECT * FROM cinema.reservations;"
    rows = session.execute(query)

    print(f'RES_ID\tNAME\tMOVIE_TITLE\tSEAT')
    for row in rows:
        print(f'{row.reservation_id}\t{row.name}\t{row.movie_name}\t{row.seat_number}')

def update_reservation(session, username):
    print("Provide id of reservation you want to update:\n")
    show_your_reservations(session, username)
    res_id = input("\nRES_ID: ") #TODO Error Handling
    res_id = f'{res_id}'

    name = f"'{username}'"
    query = f"SELECT * FROM cinema.reservations WHERE name = {name} AND reservation_id = {res_id} ALLOW FILTERING;"
    rows = session.execute(query)

    seat = -1

    for row in rows:
        movie = row.movie_name
        seat = row.seat_number
    
    if seat < 0:
        print("Wrong res_id. Redirecting to the menu")
        time.sleep(1)
        return
    
    display_title_bar()

    seat = input("Provide new seat number: ") #TODO Error Handling
    movie = f"'{movie}'"

    query = f"INSERT INTO cinema.reservations(reservation_id, name, movie_name, reservation_timestamp, seat_number) VALUES ({res_id}, {name}, {movie}, toTimestamp(now()), {int(seat)});"
    session.execute(query)

def delete_reservation(session, username):
    print("Provide id of reservation you want to delete:\n")
    show_your_reservations(session, username)
    res_id = input("\nRES_ID: ") #TODO Error Handling
    res_id = f'{res_id}'

    name = f"'{username}'"
    query = f"SELECT * FROM cinema.reservations WHERE name = {name} AND reservation_id = {res_id} ALLOW FILTERING;"
    rows = session.execute(query)

    movie = ''
    for row in rows:
        movie = row.movie_name
        movie = f"'{movie}'"
    
    display_title_bar()
    
    query = f"DELETE FROM cinema.reservations WHERE name = {name} AND movie_name = {movie} AND reservation_id = {res_id}"
    rows = session.execute(query)


def quit_database(session):
    print("\nGood bye.")
    #query = "DROP TABLE Test;"
    #session.execute(query)


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
        print("\nI don't understand that choice.\n")

