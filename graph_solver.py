import heapq
import math
from typing import List, Tuple, Dict
from data_manager import Location

def haversine_distance(loc1: Location, loc2: Location) -> float:
    R = 6371.0  
    lat1, lon1 = math.radians(loc1.lat), math.radians(loc1.lon)
    lat2, lon2 = math.radians(loc2.lat), math.radians(loc2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class GraphSolver:
    def __init__(self, locations: List[Location]) -> None:
        self.locations = locations
        self.num_nodes = len(locations)
        self.adj_matrix: Dict[int, Dict[int, float]] = self._build_distance_matrix()

    def _build_distance_matrix(self) -> Dict[int, Dict[int, float]]:
        matrix: Dict[int, Dict[int, float]] = {i: {} for i in range(self.num_nodes)}
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j:
                    dist = haversine_distance(self.locations[i], self.locations[j])
                    matrix[i][j] = dist
                else:
                    matrix[i][j] = 0.0
        return matrix

    def dijkstra_shortest_path(self, start_id: int, end_id: int) -> Tuple[float, List[int]]:
        distances = {i: float('inf') for i in range(self.num_nodes)}
        distances[start_id] = 0.0
        predecessors: Dict[int, int] = {}
        pq: List[Tuple[float, int]] = [(0.0, start_id)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_node == end_id:
                break

            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.adj_matrix[current_node].items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        curr = end_id
        while curr in predecessors:
            path.append(curr)
            curr = predecessors[curr]
        path.append(start_id)
        path.reverse()

        return distances[end_id], path

    def solve_tsp_nearest_neighbor(self, start_id: int = 0) -> Tuple[List[Location], float]:
        unvisited = set(range(self.num_nodes))
        current_node = start_id
        unvisited.remove(current_node)

        route_ids = [current_node]
        total_distance = 0.0

        while unvisited:
            next_node = min(
                unvisited,
                key=lambda neighbor: self.adj_matrix[current_node][neighbor]
            )
            total_distance += self.adj_matrix[current_node][next_node]
            current_node = next_node
            route_ids.append(current_node)
            unvisited.remove(current_node)

        total_distance += self.adj_matrix[current_node][start_id]
        route_ids.append(start_id)

        ordered_locations = [self.locations[idx] for idx in route_ids]
        return ordered_locations, total_distance
