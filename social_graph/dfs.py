from typing import Dict, List, Optional, Any
from time import perf_counter
from .graph import Graph


# =====================================================================
# DFSResult: structured data container
# =====================================================================
class DFSResult:
    def __init__(
        self,
        order: List[str],
        parent: Dict[str, Optional[str]],
        depth: Dict[str, int],
        tin: Dict[str, int],
        tout: Dict[str, int],
        time_ms: float = 0.0
    ):
        self.order = order
        self.parent = parent
        self.depth = depth
        self.tin = tin
        self.tout = tout
        self.time_ms = time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order": self.order,
            "parent": self.parent,
            "depth": self.depth,
            "tin": self.tin,
            "tout": self.tout,
            "time_ms": self.time_ms,
        }


# =====================================================================
# MAIN DFS FUNCTION
# =====================================================================
def dfs_traversal(
    graph: Graph,
    start_user: str,
    return_full: bool = True
) -> DFSResult | List[str]:

    #Perform DFS on the graph starting from a given user.

    #Parameters:
        #graph (Graph): the social graph
        #start_user (str): the root of the DFS
        #return_full (bool): return DFSResult or only traversal order

    #Returns:
        #DFSResult or List[str]

    start_time = perf_counter()

    # -----------------------------------------------------
    # Validate
    # -----------------------------------------------------
    if graph is None:
        raise ValueError("Graph cannot be None.")

    if not graph.has_user(start_user):
        return DFSResult([], {}, {}, {}, {}, 0) if return_full else []

    # -----------------------------------------------------
    # Convert to internal ID
    # -----------------------------------------------------
    start_id = graph.get_user_id(start_user)

    # Local fast references
    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    visited = set()
    parent: Dict[int, Optional[int]] = {}
    depth: Dict[int, int] = {}
    order_ids: List[int] = []

    # Timestamps (optional advanced learning feature)
    tin: Dict[int, int] = {}
    tout: Dict[int, int] = {}
    timer = [1]  # using list so it is mutable in nested function

    # -----------------------------------------------------
    # DFS RECURSION
    # -----------------------------------------------------
    def dfs(u: int, d: int):
        visited.add(u)
        depth[u] = d
        order_ids.append(u)
        tin[u] = timer[0]
        timer[0] += 1

        # deterministic sorted traversal
        for v in sorted(get_neighbors(u), key=get_name):
            if v not in visited:
                parent[v] = u
                dfs(v, d + 1)

        tout[u] = timer[0]
        timer[0] += 1

    parent[start_id] = None
    dfs(start_id, 0)

    # -----------------------------------------------------
    # Build named output
    # -----------------------------------------------------
    order_names = [get_name(n) for n in order_ids]
    parent_named = {
        get_name(node): (
            None if par is None else get_name(par)
        )
        for node, par in parent.items()
    }
    depth_named = {get_name(n): depth[n] for n in depth}
    tin_named = {get_name(n): tin[n] for n in tin}
    tout_named = {get_name(n): tout[n] for n in tout}

    elapsed = (perf_counter() - start_time) * 1000

    result = DFSResult(
        order=order_names,
        parent=parent_named,
        depth=depth_named,
        tin=tin_named,
        tout=tout_named,
        time_ms=elapsed,
    )

    return result if return_full else order_names


# =====================================================================
# DFS PATH FINDER (Used for DFSWindow)
# =====================================================================

class DFSPathResult:
    def __init__(self, path, visited_order, distances):
        self.path = path
        self.visited_order = visited_order
        self.distances = distances


def dfs_shortest_path(graph, start_user, target_user, return_full_result=True):
    #Attempts to find a path from start_user to target_user using DFS.
    #Returns DFSPathResult compatible with BFSWindow/DFSWindow expectations.

    if not graph.has_user(start_user) or not graph.has_user(target_user):
        return DFSPathResult([], [], {})

    start = graph.get_user_id(start_user)
    target = graph.get_user_id(target_user)

    visited = set()
    visited_order = []
    parent = {}
    distances = {start_user: 0}

    found = [False]

    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    # ---------------------------------------------------------
    # DFS SEARCH
    # ---------------------------------------------------------
    def dfs(u):
        if found[0]:
            return

        visited.add(u)
        visited_order.append(get_name(u))

        if u == target:
            found[0] = True
            return

        for v in sorted(get_neighbors(u), key=get_name):
            if v not in visited:
                parent[v] = u
                distances[get_name(v)] = distances[get_name(u)] + 1
                dfs(v)
                if found[0]:
                    return

    parent[start] = None
    dfs(start)

    # ---------------------------------------------------------
    # Build Path
    # ---------------------------------------------------------
    if not found[0]:
        return DFSPathResult([], visited_order, distances)

    path = []
    cur = target
    while cur is not None:
        path.append(get_name(cur))
        cur = parent.get(cur)

    path.reverse()

    return DFSPathResult(path, visited_order, distances)
