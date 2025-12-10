from typing import Dict, List


class DSU:
    def __init__(self, n: int = 0):
        self.parent = list(range(n))
        self.rank = [0] * n

    # ------------------------------------------------------------------
    # Core DSU Operations
    # ------------------------------------------------------------------

    def _ensure_capacity(self, x: int) -> None:
        current_size = len(self.parent)
        if x >= current_size:
            extend_size = x + 1 - current_size
            self.parent.extend(range(current_size, current_size + extend_size))
            self.rank.extend([0] * extend_size)

    def find(self, x: int) -> int:
        self._ensure_capacity(x)

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:

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
        components: Dict[int, List[int]] = {}

        for node in range(len(self.parent)):
            root = self.find(node)
            components.setdefault(root, []).append(node)

        return components

    def get_named_components(self, id_to_user: Dict[int, str]) -> Dict[str, List[str]]:
        numeric_comps = self.get_components()
        named_comps = {}

        for root_id, group in numeric_comps.items():
            root_name = id_to_user[root_id]
            named_comps[root_name] = [id_to_user[x] for x in group]

        return named_comps
