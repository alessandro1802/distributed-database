import unittest
from cassandra.cluster import Cluster

from utilts import *

class CassandraTests(unittest.TestCase):
    def setUp(self):
        self.cluster = Cluster()
        self.keyspace = 'cinema'

    def test_same_request(self):
        user = "User"
        session = self.__class__.cluster.connect(self.__class__.keyspace)
        
        result1 = add_reservation(session, user)
        result2 = add_reservation(session, user)
        
        self.assertTrue(result1 != None)
        self.assertTrue(result2 != None)
    
    def test_multiple_clients():        
        users = []
        sessions = []
        for uid in range(1,3):
            users.append("User" + str(uid))
            sessions.append(self.__class__.cluster.connect(self.__class__.keyspace))

        reservation = getReservations()
        #TODO select reservation

        for uid, user in enumerate(users):
            result = add_reservation(session[uid], user)
            self.assertTrue(result != None)
        
    def test_immediate_sold_out():
        pass
        
    def test_constant_cancellation_and_occupancy():
        pass

if __name__ == "__main__":
    unittest.main()