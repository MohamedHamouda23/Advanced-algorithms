import csv
from difflib import get_close_matches

# -----------------------------
# Graph construction function
# -----------------------------
def bidirectional_graph(filename):
    """Create a bidirectional graph from CSV file data"""
    
    graph = {}  # Dictionary that will store the graph structure
    
    # Open the CSV file that contains station connections
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        
        # Read each row in the CSV file
        for row in reader:
            s1, s2, cost = row[0], row[1], int(row[2])  # Extract station1, station2, and cost
            
            # If station 1 does not exist in the graph, create it
            if s1 not in graph:
                graph[s1] = {}
            
            # If station 2 does not exist in the graph, create it
            if s2 not in graph:
                graph[s2] = {}
            
            # Add the connection from station1 → station2
            graph[s1][s2] = cost
            
            # Add the reverse connection station2 → station1
            # This makes the graph bidirectional (two-way travel)
            graph[s2][s1] = cost 
    
    # Return the completed graph dictionary
    return graph


# -----------------------------
# Station validation function
# -----------------------------
def validate_station_input(station_input, graph):
    """
    Validate station input and return the correct station name
    """
    
    # Get all station names from the graph
    stations = list(graph.keys())
    
    # Convert station names to lowercase for case-insensitive comparison
    stations_lower = [s.lower() for s in stations]
    
    # -----------------------------
    # Exact match check
    # -----------------------------
    
    # Check if the user input matches any station name (case insensitive)
    if station_input.lower() in stations_lower:
        
        # Return the correctly capitalized station name from the original list
        return stations[stations_lower.index(station_input.lower())]
    
    # -----------------------------
    # Fuzzy matching check
    # -----------------------------
    
    # Find similar station names using fuzzy matching
    matches = get_close_matches(station_input.lower(), stations_lower, n=3, cutoff=0.6)
    
    if matches:
        # Convert lowercase matches back to the original station names
        suggestions = [stations[stations_lower.index(m)] for m in matches]
        
        # Show suggestions to the user
        print(f"\nStation '{station_input}' not found. Did you mean:")
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {suggestion}")
        
        # Ask the user to enter a new station name
        new_input = input("\nPlease enter station name: ").strip().title()
        
        # Validate the new input again (recursive call)
        return validate_station_input(new_input, graph)
    
    # -----------------------------
    # No match found
    # -----------------------------
    
    # If no similar station names exist
    print(f"\nStation '{station_input}' not found.")
    
    # Ask the user to try again
    new_input = input("Please enter station name: ").strip().title()
    
    # Validate again recursively
    return validate_station_input(new_input, graph)


# -----------------------------
# User input function
# -----------------------------
def get_valid_station(prompt, graph):
    """
    Get a valid station from user input with continuous validation
    """
    
    # Keep asking until a valid station is entered
    while True:
        
        # Take user input and format it
        station_input = input(prompt).strip().title()
        
        # Validate the station name
        validated = validate_station_input(station_input, graph)
        
        # If validation succeeds, return the correct station name
        if validated:
            return validated
        
        # Otherwise ask the user to try again
        else:
            print(f"Station '{station_input}' not found. Please try again.")