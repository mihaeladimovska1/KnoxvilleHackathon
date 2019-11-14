import requests, json

import networkx as nx
from itertools import permutations

# Google API URL
url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
# Google Dev API key
api_key = 'AIzaSyBfYHLkwRPSbY1MucNJL30FtJo7Er-kXTY'


# Helper methods
def next_permutation(arr):
    # Find non-increasing suffix
    i = len(arr) - 1
    while i > 0 and arr[i - 1] >= arr[i]:
        i -= 1
    if i <= 0:
        return False

    # Find successor to pivot
    j = len(arr) - 1
    while arr[j] <= arr[i - 1]:
        j -= 1
    arr[i - 1], arr[j] = arr[j], arr[i - 1]

    # Reverse suffix
    arr[i:] = arr[len(arr) - 1: i - 1: -1]
    return True


def calculate_tour_cost(G, source, potholes_tour):
    cost = G[source][potholes_tour[0]]["weight"] + G[source][potholes_tour[-1]]["weight"]
    for i in range(len(potholes_tour) - 1):
        cost += G[potholes_tour[i]][potholes_tour[i + 1]]["weight"]

    return cost


# optimized over distance or duration
def calculate_optimal_tours(trucks_start_location, pothole_locations):
    locations = [trucks_start_location] + pothole_locations

    # Create distance and duration graphs (vertices are locations)
    distanceG = nx.Graph()
    durationG = nx.Graph()

    # Adding the weighted edges of the graphs
    # Note that we assume symmetric pairwise distances (we model locations using an undirected graph)
    for i in range(len(locations) - 1):
        loc_i = locations[i]
        for j in range(i + 1, len(locations)):
            loc_j = locations[j]
            # retreive the distance and duration information from Google
            resp_obj = requests.get(url + 'origins=' + loc_i +
                                    '&destinations=' + loc_j +
                                    '&key=' + api_key)
            dist_obj = resp_obj.json()
            distance_mts = dist_obj["rows"][0]["elements"][0]["distance"]["value"]
            duration_scs = dist_obj["rows"][0]["elements"][0]["duration"]["value"]

            distanceG.add_edge(loc_i, loc_j, weight=distance_mts)
            durationG.add_edge(loc_i, loc_j, weight=duration_scs)

    best_distance_cost = float("inf")
    best_distance_tour = []
    best_duration_cost = float("inf")
    best_duration_tour = []
    # Explore all possible tours that include all unfilled potholes
    # Note: since all tours must start and end with the trucks_start_location, we only need to explore all permutations of pothole_locations
    int_potholes_tour = list(range(len(pothole_locations)))
    while True:
        potholes_tour = [pothole_locations[int_potholes_tour[i]] for i in range(len(pothole_locations))]
        # costs to first pothole and from last pothole
        distance_cost = distanceG[trucks_start_location][potholes_tour[0]]["weight"] + \
                        distanceG[trucks_start_location][potholes_tour[-1]]["weight"]
        duration_cost = durationG[trucks_start_location][potholes_tour[0]]["weight"] + \
                        durationG[trucks_start_location][potholes_tour[-1]]["weight"]
        # costs in between potholes
        for i in range(len(potholes_tour) - 1):
            distance_cost += distanceG[potholes_tour[i]][potholes_tour[i + 1]]["weight"]
            duration_cost += durationG[potholes_tour[i]][potholes_tour[i + 1]]["weight"]
        # if we have found a better tour, update
        if distance_cost < best_distance_cost:
            best_distance_cost = distance_cost
            best_distance_tour = potholes_tour
        if duration_cost < best_duration_cost:
            best_duration_cost = duration_cost
            best_duration_tour = potholes_tour

        # generate the (lexicographically) next potholes tour
        if not next_permutation(int_potholes_tour):
            # if the current int_potholes_tour was the lexicographically largest one, exit loop
            break

    distance_based = {"tour": best_distance_tour, "cost": best_distance_cost}
    duration_based = {"tour": best_duration_tour, "cost": best_duration_cost}
    optimal = {"distance": distance_based, "duration": duration_based}
    return optimal

