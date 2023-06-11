from cassandra.cluster import Cluster
import os
import time

from utils import *


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

def show_movies(session):
    rows = get_all_movies(session)
    print(f'MOVIE, \tTIME')
    for row in rows:
        print(f'{row.movie_name}, \t{row.show_timestamp}')
    return rows

def select_seat(session, movie_name):
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
    return seat

def get_new_reservation_details(username, session):
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
    # Select seat
    seat = select_seat(session, movie_name)
    return movie_name, seat

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

def get_existent_resvation_details(username, session):
    all_reservations = get_all_reservations(username, session)
    
    # Check if user has any reservations
    if not all_reservations:
        print("You don't have any reservations yet.")
        return
    
    # Select the reservation for the update
    reservation_ids = {str(row.reservation_id): [row.movie_name, int(row.seat_number)] for row in all_reservations}
    while True:
        print("Provide id of reservation you want to delete:\n")
        res_id = input("\nRES_ID: ")
        if res_id in reservation_ids:
            break
        else:
            print("Wrong reservation id was provided. Please try again:")
    movie_name, seat = reservation_ids[res_id]

    # display_title_bar()
    return res_id, movie_name, seat


if __name__ == "__main__":
    #Connect to Cassandra
    keyspace = 'cinema'
    #TODO Error Handling
    clstr = Cluster() 
    session = clstr.connect(keyspace)
    
    display_title_bar()
    user = login_to_database()
    
    display_title_bar()
    while True:
        # display_title_bar()
        choice = get_user_choice()
        # Respond to the user's choice.
        
        # Add
        if choice == '1':
            movie_name, seat = get_new_reservation_details(user, session)
            try:
                add_reservation(user, session, movie_name, seat)
                time.sleep(1)
                print("Successfully added your reservation!")
            except Exception as e:
                print('Exception', e)
                
        # Show all
        elif choice == '2':
            rows = get_all_reservations(user, session)
            if not rows:
                print("You don't have any reservations yet.")
            else:
                print("Reservation ID, \tMovie name, \tSeat")
                for row in rows:
                    print(f'{row.reservation_id}, \t{row.movie_name}, \t{row.seat_number}')
        
        # Show one
        elif choice == '3':
            row = get_one_reservation(session, user)
            print("Movie name, \tSeat, \tReservation timestamp")
            print(f'{row.movie_name}, \t{row.seat_number}, \t{row.reservation_timestamp}')
        
        # Update
        elif choice == '4':
            # Select new seat
            res_id, movie_name, current_seat = get_existent_resvation_details(user, session)
            new_seat = select_seat(session, movie_name)
            update_reservation(user, session, res_id, movie_name, current_seat, new_seat)
            time.sleep(1)
            print("Successfully updated your reservation!")
        
        # Cancel
        elif choice == '5':
            print("Warning! It can't be undone. The cancellation is irreversible.")
            if input("Press 'q' to go back or press any other key to continue:") == 'q':
                continue
            res_id, movie_name, seat = get_existent_resvation_details(user, session)
            delete_reservation(user, session, res_id, movie_name, seat)
            time.sleep(1)
            print("Successfully deleted your reservation!")
        
        # Quit
        elif choice == 'q':
            quit_database(session)
            break
        
        # Retry
        else:
            print("\nI don't understand that choice. Please try again:\n")