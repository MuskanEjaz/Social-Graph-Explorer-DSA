# from collections import deque
# from typing import List
# from .graph import Graph


# def bfs_shortest_path(graph: Graph, start_user: str, target_user: str) -> List[str]:
#     # Invalid cases
#     if not graph.has_user(start_user) or not graph.has_user(target_user):
#         return []

#     start_id = graph._user_to_id[start_user]
#     target_id = graph._user_to_id[target_user]

#     queue = deque([start_id])
#     visited = {start_id}
#     parent = {start_id: None}

#     while queue:
#         current = queue.popleft()

#         if current == target_id:
#             # Reconstruct the path
#             path = []
#             while current is not None:
#                 path.append(graph._id_to_user[current])
#                 current = parent[current]
#             return list(reversed(path))

#         for neighbor in sorted(graph._adj[current]):
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 parent[neighbor] = current
#                 queue.append(neighbor)

#     # No path -> return empty list
#     return []




"""
Enhanced BFS Shortest Path Module
---------------------------------

Fully optimized, deterministic and GUI-friendly BFS for Social Graph Explorer.

Features:
    • shortest path (guaranteed)
    • visited order
    • distance table
    • parent / exploration tree
    • error-safe behavior
    • optional performance metrics
    • deterministic output for visualization
"""

from collections import deque
from typing import Dict, List, Optional, Any
from time import perf_counter
from .graph import Graph


# =====================================================================
# Result Container (unchanged)
# =====================================================================
class BFSResult:
    """Structured result for BFS execution with GUI support."""

    def __init__(
        self,
        path: List[str],
        visited_order: List[str],
        distances: Dict[str, int],
        exploration_tree: Dict[str, Optional[str]],
        time_ms: float = 0.0,
        reachable: bool = True,
    ):
        self.path = path
        self.visited_order = visited_order
        self.distances = distances
        self.exploration_tree = exploration_tree
        self.time_ms = time_ms
        self.reachable = reachable  # False = no possible path

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to JSON-friendly dict."""
        return {
            "path": self.path,
            "visited_order": self.visited_order,
            "distances": self.distances,
            "exploration_tree": self.exploration_tree,
            "time_ms": self.time_ms,
            "reachable": self.reachable,
        }


# =====================================================================
# MAIN BFS FUNCTION
# =====================================================================
def bfs_shortest_path(
    graph: Graph,
    start_user: str,
    target_user: str,
    return_full_result: bool = True,
) -> BFSResult | List[str]:
    """
    Compute the BFS-based shortest path between two users.

    Parameters:
        graph           : Graph object
        start_user      : starting username
        target_user     : destination username
        return_full_result : True → BFSResult, False → path only

    Returns:
        BFSResult or List[str] (path only)
    """

    start_time = perf_counter()

    # --------------------------------------------------------
    # Validate inputs
    # --------------------------------------------------------
    if graph is None:
        raise ValueError("Graph cannot be None.")

    if not graph.has_user(start_user):
        return BFSResult([], [], {}, {}, reachable=False) if return_full_result else []

    if not graph.has_user(target_user):
        return BFSResult([], [], {}, {}, reachable=False) if return_full_result else []

    # Special case: same start & end
    if start_user == target_user:
        elapsed = (perf_counter() - start_time) * 1000
        return BFSResult(
            path=[start_user],
            visited_order=[start_user],
            distances={start_user: 0},
            exploration_tree={start_user: None},
            time_ms=elapsed,
        )

    # --------------------------------------------------------
    # Convert to internal IDs
    # --------------------------------------------------------
    start_id = graph.get_user_id(start_user)
    target_id = graph.get_user_id(target_user)

    queue = deque([start_id])
    visited = {start_id}
    parent: Dict[int, Optional[int]] = {start_id: None}
    distances: Dict[int, int] = {start_id: 0}
    visited_order_ids: List[int] = []

    # Faster local bindings
    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    # --------------------------------------------------------
    # BFS Loop
    # --------------------------------------------------------
    while queue:
        current = queue.popleft()
        visited_order_ids.append(current)

        if current == target_id:
            break

        # Deterministic sorted neighbors
        neighbors = sorted(get_neighbors(current), key=get_name)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # --------------------------------------------------------
    # Build results
    # --------------------------------------------------------
    path = _reconstruct_path(parent, target_id, get_name)
    visited_order = [get_name(n) for n in visited_order_ids]
    dist_named = {get_name(n): d for n, d in distances.items()}
    tree_named = {
        get_name(n): (None if parent[n] is None else get_name(parent[n]))
        for n in parent
    }

    elapsed = (perf_counter() - start_time) * 1000

    result = BFSResult(
        path=path,
        visited_order=visited_order,
        distances=dist_named,
        exploration_tree=tree_named,
        time_ms=elapsed,
        reachable=(len(path) > 0),
    )

    return result if return_full_result else path


# =====================================================================
# PATH RECONSTRUCTION HELPER
# =====================================================================
def _reconstruct_path(
    parent: Dict[int, Optional[int]],
    target_id: int,
    get_name,
) -> List[str]:
    """Reconstruct shortest path via parent pointers."""

    if target_id not in parent:
        return []

    result = []
    cur = target_id

    while cur is not None:
        result.append(cur)
        cur = parent[cur]

    result.reverse()
    return [get_name(n) for n in result]
