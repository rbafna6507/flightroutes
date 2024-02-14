## Optimal Flight Routes



This repository contains two main parts: a Flask API and a React frontend.

This is an path finding experiment using A* and historical flight and airport information. Specifically, this repository uses the OpenFlights dataset (both Routes and Airports), as seed data for airport locations and airport routes. I'll get deeper into the technical details below, but the tldr: this is an interesting (and relevant) experiment in graph theory and finding the shortest path between two specified points (airports), after generating a weighted map (airplane routes). 


## Installation
To start, make sure you have python version 3.9.7 (or newer) and the latest version of this repository cloned locally. 

Next, cd into the `/flightroutes` directory, where the Flask server's code lives:

Once in the directory, execute the following command to create a python virtual environment:

`python -m venv venv`

Once the virtual environment is created, run the following commands while in the solution directory to activate the virtual environment, and install the necessary packages to run the API.
```
. venv/bin/activate
pip install -r requirements.txt
Now that all the necessary packages are installed, you're ready to run the API locally.
```
To start the API on a local development server on http://127.0.0.1:5000 (port 5000) run:

`flask --app main run`

To enable debug mode (to have the server restart with new changes), add the --debug flag, making the command:

`flask --app main run --debug`


Next you'll want to start the React app to interface with the API.

To start, jump into the `/frontend` folder, where the React code lives. Here you'll want to install all the related npm packages using:

`npm install`

And to finally run the react app on http://127.0.0.1:3000 (port 3000), you can run:

`npm start`


You now have a fully set up environment, and will be able to use both the Flask API and the React frontend.


## Usage

### Flask API

The Flask API supports one endpoint: `/route/source=<sourceIATA>&dest=<destIATA>`. This endpoint takes in two strings of 3 letter IATA codes: the source and desintination IATA airport codes. It returns a JSON object containing three optimal paths that can be taken from the source to the destination, the total distance for each path, and the time it will take to traverse each path.

Example testing the API with `curl` to query `AER` as the source airport and `ASF` as the destination airport:

`curl http://127.0.0.1:5000/route/source=AER&dest=ASF`

Example response:

```json
{
  "distances": [
    1434.0580092172415,
    1503.756630398541,
    2547.2674426566205
  ],
  "paths": [
    [
      "AER",
      "EVN",
      "MRV",
      "ASF"
    ],
    [
      "AER",
      "KRR",
      "SCO",
      "ASF"
    ],
    [
      "AER",
      "KZN",
      "ASF"
    ]
  ],
  "times": [
    1.5933977880191572,
    1.6708407004428232,
    2.830297158507356
  ]
}
```

The API is equipped to handle invalid input queries and internal errors. In the case of no path existing, which is rare, it will return a helpful message instead of an array holding the path.

<b>Note: The graph of airports is calculated and loaded into memory on startup of the Flask app. </b>


### React Frontend
The frontend built in React is a very simple page containing two input boxes and a submit button - no fancy bells and whistles here. Simply input your desired airports to find a path between, and hit submit.

From there, the app will ping the Flask API to return three optimal routes. You'll see all three routes, and their related total distances and time to travel.


## Extra notes

## Data
This repository utilizes the OpenFlights Airports dataset, with information about hundreds of thousands of airports. In particular, this dataset provides latitude and longitude of airports, which is necessary to calculate distance between them for the weighted graph. Second, I'm using the OpenFlights Routes dataset. This dataset is important for creating edges between the airport nodes. It is a historical record of where airplanes have connected from, which means the route planning will be historically accurate to the most optimal flight routes, when optimizing for distance.


## Implementation

### Backend (A* + Airport Graph)
To start, everytime the code is ran (and on startup of the Flask app), we must calculate the graph of airports. This is done by reading in the Routes data, and the Airports data, and consolidating them. After separating, parsing, and then combining flights, their sources, and their longitudes + latitudes, we then create an adjacency list (because the graph will not be dense). This is made by iterating over routes and logging every outgoing connection to a specific airport, as well as the distance that connection takes.

Once the adjacency list is created, we can begin the A* algorithm. This works by evaluating each path it encounters based on the cost it took to get there, and the cost it will take to get to the final destination (huersitic cost). In this implementation, I calculate the hueristic cost as I need it. The algorithm then expands the least cost node using a heap, and repeats the process until the current node is the destination, or the heap is empty (no path found). 

This runs three times to find three unique routes from the source to the destination.

### React
The React app is simple - with two input boxes, it collects the user's desired source and destination airports. After inputs have been substituted, we fetch the Flask API with the proper parameters. On response, we parse the paths into separate strings and display them as `h3` elements. We also display relevant metadata such as distance and time.

### Visualizer
This part of the repo, was by far the hardest and worst one to implement. Specifically, none of the issues I faced were logical issues, but semantic and library related. I ended up using `networkx` as my plotting and organization library of the graph. From there, it was getting a list of edges generally, that were visited during A*, and that lie on the optimal route. I plot each of those accordingly in a for loop to create an animated visualization.


## Thoughts, drawbacks, and next steps
- This implementation uses distance as its optimization metric because of how easy it was to find and use. Real optimizations use other metrics including fuel use, cost, carbon output, and distance. None of the other metrics were as accessible as distance, but I would love to see how paths change based on the metric.
- This was hacked together in just a few days, so I wasn't able to extensively test the algorithm (but I did come up with a few testing strategies). So with more time, I'd definitely like to prove the correctness of this implementation using more tests. 
- I'd like to expand the functionality of the visualizer by bringing it onto the React app. Its something I considered, but wasn't able to fully execute on this time due to time constraints.


Extra note: I intentionally left out some other really nice to have things (specific to the API and React app eg. styling, custom errors, input validations) because I was hacking this together over the weekend.