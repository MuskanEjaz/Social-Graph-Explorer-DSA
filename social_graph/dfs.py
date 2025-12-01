# social_graph/dfs.py

from typing import List
from social_graph.graph import Graph


class DFS:
    """Object-oriented DFS (kept for report clarity)."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def run(self, start_user: str) -> List[str]:
        if not self.graph.has_user(start_user):
            return []

        start_id = self.graph._user_to_id[start_user]

        visited = set()
        result: List[str] = []

        def dfs_recursive(node_id: int):
            visited.add(node_id)
            result.append(self.graph._id_to_user[node_id])

            for neighbor in sorted(self.graph._adj[node_id]):
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start_id)
        return result


# ---------- SIMPLE FUNCTION FOR WINDOWS ----------
def dfs_traversal(graph: Graph, start_user: str) -> List[str]:
    """Functional-style DFS (used by GUI)."""
    dfs = DFS(graph)
    return dfs.run(start_user)
