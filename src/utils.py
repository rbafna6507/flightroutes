from collections import defaultdict
from haversine import haversine
from typing import List



class Graph:
    """
    Graph class. Maintains the graph data structure such that we can create an adjacency list (dictionary) to later traverse during pathfinding.
    """
    def __init__(self, source_list_, dest_list_, routes_, airports_):
        self.source_list = source_list_
        self.dest_list = dest_list_
        self.routes = routes_
        self.airports = airports_
        self.adj_list = defaultdict(list)
        

    def create_adjacency_list(self):
        # building edges
        for index, source in enumerate(self.source_list):
            source_airport = iata_to_airport(source, self.airports)
            dest_airport = iata_to_airport(self.dest_list[index], self.airports)
            if source_airport is None or dest_airport is None:
                continue
            distance = calculate_distance(source_airport, dest_airport)
            self.adj_list[source].append((dest_airport, distance))

                 
class Airport:
    """
    Simple Airport class to organize information related to a specific airport's IATA.
    """
    def __init__(self, name_, iata_, lat_, long_):
        self.name = name_
        self.iata = iata_
        self.lat = float(lat_)
        self.long = float(long_)
        self.distance_to_goal = float('inf')
    

class Route:
    """
    Simple Route class to organize the start and destination airports (IATAs) of a route.
    """
    def __init__(self, source_, dest_):
        self.source = source_
        self.dest = dest_


def create_source_list(routes: List[Route]) -> List[str]:
    """
    Helper function to create a list of just source airports of all routes. Corresponding destinations are located in create_dest_list().
    """
    source_list = []
    for route in routes:
        source_list.append(route.source)
    return source_list

                 
def create_dest_list(routes: List[Route]) -> List[str]:
    """
    Helper function to create a list of just destination airports of all routes. Corresponding destinations are located in create_source_list().
    """
    dest_list = []
    for route in routes:
        dest_list.append(route.dest)
    return dest_list
                 

def iata_to_airport(iata: str, airports: List[Airport]) -> Airport:
    """
    Converts an IATA string to the corresponding Airport object. Looks through the 'aiports' list of airports for a match. Returns None if it can't be found.
    """
    for airport in airports:
        # print(airport.iata)
        if airport.iata == iata:
            return airport
    return None
                 

def calculate_distance(source_airport: Airport, dest_airport: Airport) -> float:
    """
    Calculates haversine distance between two airports based on latitudes and longitudes.
    """
    source_lat_long = (source_airport.lat, source_airport.long)
    dest_lat_long = (dest_airport.lat, dest_airport.long)
    return haversine(source_lat_long, dest_lat_long)


def create_routes(routes_infile: str) -> List[Route]:
    """
    Reads in the routes data file and creates a corresponding list of all the Routes present.
    """
    routes_file = open(routes_infile, "r")
    routes = []
    for line in routes_file:
        splits = line.split(",")
        source = splits[2]
        dest = splits[4]
        route = Route(source, dest)
        routes.append(route)
    return routes

    
def create_airports(airports_infile: str) -> List[Airport]:
    """
    Reads in the airports data file and creates a corresponding list of all the Airports present.
    """
    airports_file = open(airports_infile, "r")
    airports = []
    for line in airports_file:
        splits = line.split(",")
        name = splits[1]
        iata = splits[4]
        iata = iata.replace('"', '')
        lat = splits[6]
        long = splits[7]
        airport = Airport(name, iata, lat, long)
        airports.append(airport)
    return airports


# clean the inputs from the API
def check_inputs(source: str, dest: str):
    """
    Validate the input source and destination IATA strings.
    """
    if len(source) != 3 or len(dest) != 3:
        raise InvalidRequest(
            source,
            dest,
            "Either the source or the destination airport IATAs given are invalid. Please check them and try again",
            400
        )
    
    if not source.isalpha() or not dest.isalpha():
        raise InvalidRequest(
            source,
            dest,
            "All the characters in the source or destination IATAs are not valid letters. Please recheck and try again with 3 letter IATA codes",
            400
        )
    

# Custom Error Handling Classes
class InvalidRequest(Exception):
    """
    General class to handle invalid API requests that can deliver custom messages to offer insight into what went wrong.
    """

    def __init__(self, source, dest, description, status_code):
        self.status_code = status_code
        self.source = source
        self.dest = dest
        self.description = description


class ProcessingError(Exception):
    """
    General class to handle processing errors that the API can't handle. This only delivers 500 error codes, with custom messages.
    """

    def __init__(self, source, dest, description, status_code):
        self.source = source
        self.dest = dest
        self.description = description
        self.status_code = 500
