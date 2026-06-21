from graph_validation import bidirectional_graph, validate_station_input, get_valid_station
import csv
import time
import heapq



# Rebuild the path from start to end using the previous nodes dictionary
def build_path(start, end, previous):
    """Reconstruct the path from start to end using previous nodes dictionary"""
    
    path = []
    current = end
    
    # Move backwards from end to start
    while current in previous:
        path.append(current)
        current = previous[current]
    
    # Add start station
    path.append(start)
    
    # Reverse path to correct order
    path.reverse()
    
    return path


# Dijkstra algorithm to find shortest path between two stations
def dijkstra(graph, start, end, avoid_stations=None):
    """Find shortest path between two stations using Dijkstra with a priority queue"""
    
    if avoid_stations is None:
        avoid_stations = set()
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}
    
    # Priority queue: stores (distance, node)
    heap = [(0, start)]
    visited = set()
    
    while heap:
        current_dist, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        visited.add(current)
        
        # Stop if destination reached
        if current == end:
            break
        
        for neighbour, cost in graph[current].items():
            if neighbour in visited or neighbour in avoid_stations:
                continue
            
            new_cost = current_dist + cost
            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                previous[neighbour] = current
                heapq.heappush(heap, (new_cost, neighbour))
    
    # If no route was found, return empty path and infinite cost
    if distances[end] == float('inf'):
        return [], float('inf')
    
    path = build_path(start, end, previous)
    return path, distances[end]


# Select the next station to visit from the remaining list
def get_next_station(graph, current, remaining, start, end):
    """Determine the next optimal station to visit from current position"""
    
    next_station = None
    next_path = []
    next_cost = float('inf')

    # Check each remaining station
    for station in remaining:
        
        # Calculate shortest path
        # Do not block previously visited stations here,
        # because intermediate transit stations are allowed to repeat
        avoid = set()
        
        short_path, short_cost = dijkstra(graph, current, station, avoid)
        
        # Choose station with lowest cost
        if short_cost < next_cost:
            next_cost = short_cost
            next_station = station
            next_path = short_path

    return next_station, next_path, next_cost


# Add a new path segment to the final route
def add_path_to_route(full_path, path):
    """Add new path segments to the full route while avoiding duplicates"""
    
    for node in path[1:]:
        full_path.append(node)


# Plan a full route including required stations
def full_route(graph, start, visit_list, end):
    """Plan complete route including all mandatory visit stations"""
    
    remaining = visit_list.copy()  
    
    current = start
    full_path = [start]
    total_cost = 0

    # Visit all required stations
    while remaining:
        next_station, next_path, next_cost = get_next_station(graph, current, remaining, start, end)
        
        # If no valid path was found to the next required station
        if next_cost == float('inf'):
            return [], float('inf')
        
        # Add the selected path to route
        add_path_to_route(full_path, next_path)
        
        total_cost += next_cost
        current = next_station
        remaining.remove(next_station)

    # Calculate final path to destination
    # Intermediate transit stations are allowed to repeat where necessary
    path, cost = dijkstra(graph, current, end)

    # If no valid final path was found
    if cost == float('inf'):
        return [], float('inf')

    # Add final path
    add_path_to_route(full_path, path)
    
    total_cost += cost

    return full_path, total_cost



# -----------------------------
# Main program
# -----------------------------
if __name__ == "__main__":
    start_time = time.time()

    
    # Load graph from CSV file
    graph = bidirectional_graph('activity1_3_railnetwork_data.csv')
    
    # Get starting station from user
    start = get_valid_station("Please enter your starting station: ", graph)
    
    # Get final destination
    end = get_valid_station("Please enter your final destination station: ", graph)
    
    # Ask user for stations to visit
    visit_input = input("Enter stations to visit, separated by commas: ").strip()
    
    # Format input into list
    visit_list_raw = [x.strip().title() for x in visit_input.split(",") if x.strip()]
    
    # Validate each station
    visit_list = []
    seen_visits = set()
    
    for station in visit_list_raw:
        validated = validate_station_input(station, graph)
        
        if validated:
            if validated in seen_visits:
                print(f"Station '{validated}' is repeated and will be skipped.")
            elif validated == start or validated == end:
                print(f"Station '{validated}' will be skipped because start/end cannot be repeated in the visit list.")
            else:
                visit_list.append(validated)
                seen_visits.add(validated)
        else:
            print(f"Station '{station}' not found and will be skipped.")
    
    # Calculate route
    path, cost = full_route(graph, start, visit_list, end)
    
    # Save output to file
    with open("route_output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["Station Order", "Total Cost"])
        # Row: route as a string, cost
        if cost == float('inf') or not path:
            writer.writerow(["Not Found", "Not Found"])
        else:
            writer.writerow([" -> ".join(path), cost])
    end_time = time.time()
    print("Execution time:", end_time - start_time, "seconds")