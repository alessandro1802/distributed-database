from cassandra.cluster import Cluster
import datetime
import os

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
    print("[q] Quit.")
    
    return input("What would you like to do? ")

def add_reservation(session, username):
    name = f"'{username}'"

    query = f"SELECT max(reservation_id) FROM Test WHERE name = {name} ALLOW FILTERING;"
    agg_max = session.execute(query)
    maxi = None
    for row in agg_max:
        maxi = row.system_max_reservation_id

    reservation_id = 0 if maxi is None else (maxi + 1)

    movie = input("Movie name: ")
    movie = f"'{movie}'"
    room = input("Room: ")
    seat = input("Seat: ")
    
    query = f"INSERT INTO Test(timestamp, reservation_id, name, movie_name, room, seat) VALUES (toTimestamp(now()), {int(reservation_id)}, {name}, {movie}, {int(room)}, {int(seat)});"
    session.execute(query)


def show_your_reservations(session, username):
    name = f"'{username}'"
    query = f"SELECT * FROM Test WHERE name = {name} ALLOW FILTERING;"
    rows = session.execute(query)

    print(f'RES_ID\tMOVIE_TITLE\tROOM\tSEAT')
    for row in rows:
        print(f'{row.reservation_id}\t{row.movie_name}\t{row.room}\t{row.seat}')

def show_all_reservations(session):
    query = f"SELECT * FROM Test;"
    rows = session.execute(query)

    print(f'TIMESTAMP\t\tRES_ID\tUSERNAME\tMOVIE_TITLE\tROOM\tSEAT')
    for row in rows:
        print(f'{row.timestamp}\t{row.reservation_id}\t{row.name}\t{row.movie_name}\t{row.room}\t{row.seat}')

def update_reservation(session, username):
    print("Provide id of reservation you want to update:\n")
    show_your_reservations(session, username)
    res_id = input("\nRES_ID: ")
    
    timestamp = 0
    movie_name = ''
    room = -1
    seat = -1

    name = f"'{username}'"
    query = f"SELECT * FROM Test WHERE name = {name} AND reservation_id = {int(res_id)} ALLOW FILTERING;"
    rows = session.execute(query)

    for row in rows:
        timestamp = row.timestamp
        movie_name = row.movie_name
        room = row.room
        seat = row.seat
    
    if room < 0:
        print("Wrong res_id")
        return
    
    display_title_bar()

    answer = input("\nDo you want to update movie name? [y/n]: ")
    if(answer.lower() == 'y'):
        movie_name = input("Provide new movie name: ")
        movie_name = f"'{movie_name}'"

    answer = input("\nDo you want to update room? [y/n]: ")
    if(answer.lower() == 'y'):
        room = input("Provide new room: ")

    answer = input("\nDo you want to update seat? [y/n]: ")
    if(answer.lower() == 'y'):
        seat = input("Provide new seat: ")

    #query = f"INSERT INTO Test(timestamp, reservation_id, name, movie_name, room, seat) VALUES ({toTimestamp(timestamp)}, {int(res_id)}, {name}, {movie_name}, {int(room)}, {int(seat)});"
    #session.execute(query)


def quit_database(session):
    print("\nGood bye.")
    query = "DROP TABLE Test;"
    session.execute(query)


### MAIN ###

#Connect to Cassandra
clstr=Cluster(['172.19.0.2', '172.19.0.3', '172.19.0.4'])
session=clstr.connect()

#Create keyspace
query0_1 = "USE cinema;"
session.execute(query0_1)

#Create table
query1_1 = "CREATE TABLE IF NOT EXISTS Test (timestamp timestamp, reservation_id int, name text, movie_name text, room int, seat int, PRIMARY KEY(timestamp));"
query1_2 = "INSERT INTO Test(timestamp, reservation_id, name, movie_name, room, seat) VALUES (toTimestamp(now()), 99, 'test_user', 'Bee Movie', 1, 23);"
session.execute(query1_1)
session.execute(query1_2)

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
    elif choice == 'q':
        quit_database(session)
        break
    else:
        print("\nI didn't understand that choice.\n")


