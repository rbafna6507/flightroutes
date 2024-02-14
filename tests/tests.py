from src.utils import iata_to_airport, create_routes, create_airports, create_dest_list, create_source_list, Graph
from src.a_star import a_star
from haversine import haversine
import unittest


"""
This is a simple API testing file. To run this file, run the command below in the root directory.
Combination of unit tests and full API tests.

python -m unittest discover -s say_yes
"""

# parsing functions for data, to turn into a graph
routes_infile = '../flightroutes/data/routes.dat'
# routes_infile = 'data/routetesting.dat'
airports_infile = '../flightroutes/data/airports.dat'

print("Building flight routes graph...")
routes = create_routes(routes_infile)
airports = create_airports(airports_infile)

source_list = create_source_list(routes)
dest_list = create_dest_list(routes)


graph = Graph(source_list, dest_list, routes, airports)
graph.create_adjacency_list()
print("Graph building completed. Running tests...")


class direct_connection(unittest.TestCase):
    """
    Tests several calls where the goal airport is a direct connection, requiring no intermediate airports.
    
    Verifies the number of elements in path, the path itself, and that haversine works correctly for the same elements.
    """
    def setUp(self):
        self.path = a_star(dict(graph.adj_list), 'AER', 'DME', graph.airports)
        self.random1 = a_star(dict(graph.adj_list), 'JFK', 'LAX', graph.airports)
        self.random2 = a_star(dict(graph.adj_list), 'LAX', 'SFO', graph.airports)
        self.random3 = a_star(dict(graph.adj_list), 'GSP', 'ATL', graph.airports)
        
    def test_russia(self):
        assert(len(self.path['paths'][0]) == 2)
        assert(self.path['paths'][0] == ['AER', 'DME'])
        
    
    def test_check_haversine_itself(self):
        # check haversine distance from an airport to itself if 0
        airport1 = iata_to_airport('AER', graph.airports)
        airport2 = iata_to_airport('AER', graph.airports)
        lat_long_1 = (airport1.lat, airport1.long)
        lat_long_2 = (airport2.lat, airport2.long)
        assert(haversine(lat_long_1, lat_long_2) == 0)
        
    
    def test_random_direct(self):
        assert(len(self.random1['paths'][0]) == 2)
        assert(len(self.random2['paths'][0]) == 2)
        assert(len(self.random3['paths'][0]) == 2)
        assert(self.random1['paths'][0] == ['JFK', 'LAX'])
        assert(self.random2['paths'][0] == ['LAX', 'SFO'])
        assert(self.random3['paths'][0] == ['GSP', 'ATL'])
        

class connecting_airports(unittest.TestCase):
    """
    Test several calls where the goal airport is not a direct connection, and requires intermediate airports. Routes were verified by hand.
    
    Some of these calls are hand picked with a specific correct path in mind, some are random.
    """
    def setUp(self):
        self.path = a_star(dict(graph.adj_list), 'AER', 'ASF', graph.airports)
        self.path1  = a_star(dict(graph.adj_list), 'BGM', 'GSP', graph.airports)
        self.path2  = a_star(dict(graph.adj_list), 'LAX', 'GSP', graph.airports)
    # just need to pick some paths out from the routes file + i'll be using that as my source data, constricting paths to only a few airports
    # in russia that can go between each other, but not directly to their goals.
    def test_check(self):
        assert(len(self.path['paths'][0]) == len(["AER","EVN","MRV","ASF"]))
        assert(self.path['paths'][0] == ["AER","EVN","MRV","ASF"])
        assert(self.path1['paths'][0] == ["BGM","IAD", "GSP"])
        assert(len(self.path1['paths'][0]) == len(["BGM","IAD", "GSP"]))
        assert(self.path2['paths'][0] == ["LAX","BNA", "GSP"])
        assert(len(self.path2['paths'][0]) == len(["LAX","BNA", "GSP"]))
