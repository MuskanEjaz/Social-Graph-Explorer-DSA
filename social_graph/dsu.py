# class DSU:
#     def __init__(self, n: int):
#         # parent[i] = parent of node i
#         self.parent = list(range(n))
#         # rank optimization
#         self.rank = [0] * n

#     def find(self, x: int) -> int:
#         # Path compression
#         if self.parent[x] != x:
#             self.parent[x] = self.find(self.parent[x])
#         return self.parent[x]

#     def union(self, x: int, y: int) -> None:
#         rootX = self.find(x)
#         rootY = self.find(y)

#         if rootX == rootY:
#             return

#         # Union by rank
#         if self.rank[rootX] < self.rank[rootY]:
#             self.parent[rootX] = rootY
#         elif self.rank[rootX] > self.rank[rootY]:
#             self.parent[rootY] = rootX
#         else:
#             self.parent[rootY] = rootX
#             self.rank[rootX] += 1





"""
Disjoint Set Union (Union–Find) Module
--------------------------------------

This module provides an optimized implementation of the DSU (Union–Find)
data structure with:

    • path compression
    • union by rank
    • automatic dynamic resizing
    • community detection (connected components)
    • GUI-friendly API for grouping users

Used in the Social Graph Explorer project to detect friendship clusters.
"""

from typing import Dict, List


class DSU:
    """
    A fully optimized Union–Find structure supporting:

        find(x)               → returns representative of x
        union(x, y)           → merges two sets
        get_components()      → returns groups of connected users

    Internally uses:
        - path compression
        - union by rank
    """

    def __init__(self, n: int = 0):
        """
        Initialize DSU with `n` elements.

        Parameters:
            n (int): Number of elements. Users are mapped to indices externally.
        """
        self.parent = list(range(n))
        self.rank = [0] * n

    # ------------------------------------------------------------------
    # Core DSU Operations
    # ------------------------------------------------------------------

    def _ensure_capacity(self, x: int) -> None:
        """
        Expands DSU storage when new indices appear.

        This makes DSU *dynamic* so the graph can add users anytime.
        """
        current_size = len(self.parent)
        if x >= current_size:
            extend_size = x + 1 - current_size
            self.parent.extend(range(current_size, current_size + extend_size))
            self.rank.extend([0] * extend_size)

    def find(self, x: int) -> int:
        """
        Find the representative (root) of x with path compression.
        """
        self._ensure_capacity(x)

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """
        Merge the sets containing x and y using union-by-rank.
        """
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return  # already in the same set

        # Union by rank
        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

    # ------------------------------------------------------------------
    # Community Detection (Connected Components)
    # ------------------------------------------------------------------

    def get_components(self) -> Dict[int, List[int]]:
        """
        Returns groups of connected users.

        Returns:
            Dict[root_id → list_of_node_ids]
            Example:
                {0: [0, 2, 5], 3: [3, 7]}
        """
        components: Dict[int, List[int]] = {}

        for node in range(len(self.parent)):
            root = self.find(node)
            components.setdefault(root, []).append(node)

        return components

    def get_named_components(self, id_to_user: Dict[int, str]) -> Dict[str, List[str]]:
        """
        Convert numeric components into user-name components for GUI display.

        Parameters:
            id_to_user (dict): mapping of node_id → username

        Returns:
            Example:
                {
                    "A": ["A", "C", "D"],
                    "B": ["B", "F"]
                }
        """
        numeric_comps = self.get_components()
        named_comps = {}

        for root_id, group in numeric_comps.items():
            root_name = id_to_user[root_id]
            named_comps[root_name] = [id_to_user[x] for x in group]

        return named_comps
