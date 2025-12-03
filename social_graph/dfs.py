# # social_graph/dfs.py

# from typing import List
# from social_graph.graph import Graph


# class DFS:
#     """Object-oriented DFS (kept for report clarity)."""

#     def __init__(self, graph: Graph) -> None:
#         self.graph = graph

#     def run(self, start_user: str) -> List[str]:
#         if not self.graph.has_user(start_user):
#             return []

#         start_id = self.graph._user_to_id[start_user]

#         visited = set()
#         result: List[str] = []

#         def dfs_recursive(node_id: int):
#             visited.add(node_id)
#             result.append(self.graph._id_to_user[node_id])

#             for neighbor in sorted(self.graph._adj[node_id]):
#                 if neighbor not in visited:
#                     dfs_recursive(neighbor)

#         dfs_recursive(start_id)
#         return result


# # ---------- SIMPLE FUNCTION FOR WINDOWS ----------
# def dfs_traversal(graph: Graph, start_user: str) -> List[str]:
#     """Functional-style DFS (used by GUI)."""
#     dfs = DFS(graph)
#     return dfs.run(start_user)










"""
DFS Traversal Module
--------------------

This file implements a clean, deterministic, GUI-friendly Depth-First Search
for your Social Graph Explorer project.

Features:
    • DFS traversal order
    • parent tree (DFS tree)
    • node depth levels
    • timestamps (tin / tout)
    • structured result (for GUI + animator)
    • deterministic sorted traversal
    • execution time measurement
"""

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
    """
    Perform DFS on the graph starting from a given user.

    Parameters:
        graph (Graph): the social graph
        start_user (str): the root of the DFS
        return_full (bool): return DFSResult or only traversal order

    Returns:
        DFSResult or List[str]
    """

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