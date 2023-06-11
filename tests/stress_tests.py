import unittest
from cassandra.cluster import Cluster

import sys
import os
sys.path.append(os.path.abspath('../'))
from utils import *

class CassandraTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.cluster = Cluster()
        cls.keyspace = 'cinema'

    def test_same_request(self):
        # Create a user with session
        user = "TestUser"
        session = self.cluster.connect(self.keyspace)
        
        # Select movie, seat
        rows = get_all_movies(session)
        movie_name = [row.movie_name for row in rows][0]
        seat = list(avaiable_seats(session, movie_name))[0]
        
        # Make the same reservation twice
        success = True
        add_reservation(user, session, movie_name, seat)
        try:
            add_reservation(user, session, movie_name, seat)
        except:
            success = False
        
        self.assertFalse(success)
    
    def test_multiple_clients(self):      
        # Create users and their sessions
        users = []
        sessions = []
        for uid in range(1,3):
            users.append("TestUser" + str(uid))
            sessions.append(self.cluster.connect(self.keyspace))
        
        # Select a movie and get available seats
        rows = get_all_movies(sessions[0])
        movie_name = [row.movie_name for row in rows][0]
        seats = list(avaiable_seats(sessions[0], movie_name))
        
        # Make a reservaion from every user
        success = True
        for uid, user in enumerate(users):                
            try:
                add_reservation(user, sessions[uid], movie_name, seats[uid])
            except:
                success = False
                break
        
        self.assertTrue(success)
        
    def test_immediate_sold_out(self):
        movieName = "TestMovie"
        showTime = "2023-06-13 08:00"
        
        # Add test movie
        sessionAdmin = self.cluster.connect(self.keyspace)        
        query = f"INSERT INTO movies(movie_name, show_timestamp, taken_seats) VALUES ('{movieName}', '{showTime}', {{}});"
        sessionAdmin.execute(query)

        all_seats = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        query = f"UPDATE movies SET taken_seats = taken_seats + {all_seats} WHERE movie_name = '{movieName}';"
        
        # Get the movie details for user
        user = "TestUser"
        session = self.cluster.connect(self.keyspace)
        seats = list(avaiable_seats(session, movieName))[0]

        success = True
        # Make all seats unavailable
        sessionAdmin.execute(query)
        # Add a user reservation
        try:
            add_reservation(user, session, movie_name, seat)
        except:
            success = False

        query = f"DELETE FROM movies WHERE movie_name = '{movieName}';"
        sessionAdmin.execute(query)
        self.assertFalse(success)
        
    def test_constant_cancellation_and_occupancy(self):
        movieName = "TestMovie"
        showTime = "2023-06-13 08:00"
        
        # Add test movie with a dummy taken seat
        sessionAdmin = self.cluster.connect(self.keyspace) 
        query = f"INSERT INTO movies(movie_name, show_timestamp, taken_seats) VALUES ('{movieName}', '{showTime}', {{}});"
        sessionAdmin.execute(query)
        query = f"UPDATE movies SET taken_seats = taken_seats + {{5}} WHERE movie_name = '{movieName}';"
        sessionAdmin.execute(query)
        
        # Get the movie details for user
        user = "TestUser"
        session = self.cluster.connect(self.keyspace)
        seat = list(avaiable_seats(session, movieName))[0]

        success = True
        for i in range(100):
            try:
                add_reservation(user, session, movieName, seat)
                query = f"SELECT * FROM cinema.reservations WHERE name = '{user}';"
                res_id =  str(session.execute(query).one().reservation_id)
                delete_reservation(user, session, res_id, movieName, seat)
            except Exception as e:
                success = False
                print(e)
                break
                
        query = f"DELETE FROM movies WHERE movie_name = '{movieName}';"
        sessionAdmin.execute(query)
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()