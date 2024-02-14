from src.utils import check_inputs, create_routes, create_airports, create_dest_list, create_source_list, Graph, InvalidRequest, ProcessingError
from src.a_star import a_star
from flask import Flask, jsonify
import json
# from flask_caching import Cache


# parsing functions for data, to turn into a graph
routes_infile = 'data/routes.dat'
airports_infile = 'data/airports.dat'

app = Flask(__name__)

with app.app_context():
    # calculate the graph at the start of the flask app's life, so each request doesn't recalculate it.
    print("Building flight routes graph...")
    routes = create_routes(routes_infile)
    airports = create_airports(airports_infile)

    source_list = create_source_list(routes)
    dest_list = create_dest_list(routes)

    graph = Graph(source_list, dest_list, routes, airports)
    graph.create_adjacency_list()
    print("Graph building completed, initializing Flask App")
    

@app.route("/route/source=<source>&dest=<dest>", methods=["GET"])
def calculate_route(source, dest):
    source = source.upper()
    dest = dest.upper()
    
    check_inputs(source, dest)
    
    # separated error handling to offer more specific error messages as to which IATA code is the issue.
    if source not in graph.adj_list:
        raise InvalidRequest(
            source,
            dest,
            "Unfortunately, our data source does not support any route or airport for the source IATA.",
            400
        )
    if dest not in graph.adj_list:
        raise InvalidRequest(
            source,
            dest,
            "Unfortunately, our data source does not support any route or airport for destination IATA.",
            400
        )
        
    data = a_star(dict(graph.adj_list), source, dest, graph.airports)
    response = jsonify({'paths': data['paths'], 'distances': data['distance'], 'times':data['time']})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    
    
@app.route("/")
def instructions_landing_page():
    """
    Landing page with instructions on how to use this API.
    """
    return "Query for an optimal flight route using this API. To query, enter in a start and destination airport IATA id in the following endpoint and format: https://127.0.0.1:5000/route/sourceIATA/destIATA"



# Error Handling for Invalid ICAO IDs
@app.errorhandler(InvalidRequest)
def invalid_icao(e):
    """
    Error handling for the InvalidRequest error to deliver  the status code, description, and ICAO that caused the InvalidRequest.
    """
    response = {"status": e.status_code, "description": e.description, "source": e.source, "dest": e.dest}
    return json.dumps(response), e.status_code


@app.errorhandler(ProcessingError)
def internal_error(e):
    """
    Error handling for a ProcessingError if the API runs into an issue it can't process. This is for cases that should not be possible.
    """
    response = {"status": e.status_code, "description": e.description, "source": e.source, "dest": e.dest}
    return json.dumps(response), e.status_code
