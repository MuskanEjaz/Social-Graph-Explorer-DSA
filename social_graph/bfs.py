from collections import deque
from typing import List
from .graph import Graph


def bfs_shortest_path(graph: Graph, start_user: str, target_user: str) -> List[str]:
    # Invalid cases
    if not graph.has_user(start_user) or not graph.has_user(target_user):
        return []

    start_id = graph._user_to_id[start_user]
    target_id = graph._user_to_id[target_user]

    queue = deque([start_id])
    visited = {start_id}
    parent = {start_id: None}

    while queue:
        current = queue.popleft()

        if current == target_id:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(graph._id_to_user[current])
                current = parent[current]
            return list(reversed(path))

        for neighbor in sorted(graph._adj[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # No path -> return empty list
    return []
