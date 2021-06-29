from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Convert graph to data model
def dataModel(graph, nbVehicules, meta):
    data = {}
    data["graph"] = graph
    data["nbVehicules"] = nbVehicules
    data["startPoint"] = 0
    data["meta"] = meta
    return data

def getRoutes(nbVehicules, manager, routing, solution):
    routes = {}
    for vehicle_id in range(nbVehicules):
        routes[vehicle_id] = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            routes[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
        routes[vehicle_id].append(manager.IndexToNode(index))
    return routes

# Get and print solution
def getSolution(nbVehicules, manager, routing, solution, doPrint = False):
    worstDistance = 0
    for vehicle_id in range(nbVehicules):
        index = routing.Start(vehicle_id)
        plan_output = "Route for vehicle {}:\n".format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += " {} -> ".format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += "{}\n".format(manager.IndexToNode(index))
        plan_output += "Cost of the route: {}\n".format(route_distance)
        if(doPrint): print(plan_output)
        worstDistance = max(route_distance, worstDistance)
    if(doPrint): print("Maximum route cost: {}".format(worstDistance))
    return worstDistance

def findSolution(data, manager, routing):      
    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["graph"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint
    dimension_name = "Distance"
    flattened_graph = [i for j in data["graph"] for i in j]
    max_travel_distance = 2 * max(flattened_graph)

    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_travel_distance,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # First solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        
    # Metaheuristics
    search_parameters.local_search_metaheuristic = (getattr(
        routing_enums_pb2.LocalSearchMetaheuristic, data["meta"]))

    # Timeout in seconds
    search_parameters.time_limit.seconds = 30 + len(data["graph"])

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    return solution

def googleORTools(graph, nbVehicules, meta = "AUTOMATIC"):
    # Instantiate the data problem
    data = dataModel(graph, nbVehicules, meta)

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data["graph"]), data["nbVehicules"], data["startPoint"])

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Solve the problem
    solution = findSolution(data, manager, routing)
    
    if solution:
        sol = getSolution(nbVehicules, manager, routing, solution)
        routes = getRoutes(nbVehicules, manager, routing, solution)
        return (routes, sol)
    else:
        print("!!! No solution found")
        return ([], 0)