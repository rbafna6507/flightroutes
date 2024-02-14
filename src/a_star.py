from src.utils import calculate_distance, iata_to_airport, InvalidRequest, Airport
from collections import defaultdict
from typing import List, Dict, Tuple
import heapq


def distance_to(current_airport: Airport, goal_airport: Airport) -> float:
    """
    Semantic Wrapper around the calculate_distance function. Uses haversine distance formula to find the actual distance between airports.
    """
    return calculate_distance(current_airport, goal_airport)


def reconstruct_path(came_from, current) -> List[str]:
    """
    Function to rebuild the path that was taken during the A* algorithm.
    
    came_from: dictionary holding 'current_IATA': 'came_from_IATA', where the start IATA appears only as a value.
    current: a tuple of (cost, 'IATA')
    """
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]





# start/goal are the airport iata codes
def a_star(adj_list: Dict[str, Tuple[Airport, int]], start: str, goal: str, airports: List[Airport]) -> List[List[str]]:
    """
    A* pathfinding algorithm. Path cost is the distance from airport to airport (weight edge). Heuristic cost is the distance from that node to the goal.
    f_score, which is the total cost (path cost + hueristic cost), is used as the metric for the priority queue where we select the next airport to expand.
    
    Algorithm works by expanding the start node, and picking the least cost node that we find. We continue to expand the least cost node until no nodes
    are left in the priority queue, or when the current node is the goal airport. Then, we use the came_from dictionary to recreate the path we took.
    
    Returns a dictionary with the top 3 paths, their distances, and the time it would take to travel them at an average speed of 900 kmh.
    """
    
    start_airport = iata_to_airport(start, airports)
    goal_airport = iata_to_airport(goal, airports)
    
    # separated error checking for more specific error messages as to which IATA is the issue. Redundant error checking.
    if start_airport is None:
        raise InvalidRequest(
            start,
            goal,
            "Could not find start_airport in data.",
            400
        )
        
    if goal_airport is None:
        raise InvalidRequest(
            start,
            goal,
            "Could not find destination_airport in data.",
            400
        )
        
    top_n = 0
    top_paths = {'paths':[], 'distance':[], 'time':[]}
    while top_n != 3:
        heap = []
        came_from = {}
        visited_edges = []
        found = False
        
        # cost of the cheapest path from the start to n
        g_score = defaultdict(lambda: float('inf'))
        g_score[start] = 0
        f_score = defaultdict(lambda: float('inf'))
        f_score[start] = distance_to(start_airport, goal_airport)
        heapq.heappush(heap, (f_score[start], start))
        while heap:
            current = heapq.heappop(heap)
            if current[1] == goal:
                found = True
                path =reconstruct_path(came_from, current[1])
                top_paths['paths'].append(path)
                top_paths['distance'].append(f_score[goal])
                # considering an average speed of 900 kmh, we divide teh distance by that speed to get time
                top_paths['time'].append(f_score[goal] / 900)
                top_n = top_n + 1
                if path[1] in adj_list:  
                    adj_list.pop(path[1])
                break
            
            if current[1] not in adj_list:
                continue
                
            for connection in adj_list[current[1]]:
                potential_g_score = g_score[current[1]] + connection[1]

                if potential_g_score < g_score[connection[0].iata]:
                    came_from[connection[0].iata] = current[1]
                    g_score[connection[0].iata] = potential_g_score
                    f_score[connection[0].iata] = potential_g_score + distance_to(connection[0], goal_airport)
                    if (f_score[connection[0].iata], connection[0].iata, g_score[connection[0].iata], distance_to(connection[0], goal_airport)) not in heap:
                        heapq.heappush(heap, (f_score[connection[0].iata], connection[0].iata))
                        visited_edges.append((current[1], connection[0].iata))
        if not found:
            top_paths['paths'].append(None)
            top_n = top_n + 1
    return top_paths