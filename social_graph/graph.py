# social_graph/graph.py

import json
import os
from typing import Dict, List, Set


GRAPH_FILE = "graph_data.json"   # persistent storage file


class Graph:
    def __init__(self) -> None:
        self._user_to_id: Dict[str, int] = {}
        self._id_to_user: List[str] = []
        self._adj: List[Set[int]] = []

    # =====================================================================
    # USER MANAGEMENT
    # =====================================================================
    def add_user(self, username: str) -> None:
        username = username.strip()
        if not username:
            return

        if username in self._user_to_id:
            return

        new_id = len(self._id_to_user)
        self._user_to_id[username] = new_id
        self._id_to_user.append(username)
        self._adj.append(set())

    def has_user(self, username: str) -> bool:
        return username in self._user_to_id

    def get_all_users(self) -> List[str]:
        return list(self._user_to_id.keys())

    # =====================================================================
    # FRIENDSHIPS
    # =====================================================================
    def add_friendship(self, u: str, v: str) -> None:
        if u == v:
            return

        if not self.has_user(u):
            self.add_user(u)

        if not self.has_user(v):
            self.add_user(v)

        uid = self._user_to_id[u]
        vid = self._user_to_id[v]

        self._adj[uid].add(vid)
        self._adj[vid].add(uid)

    def get_friends(self, username: str) -> List[str]:
        if not self.has_user(username):
            return []

        uid = self._user_to_id[username]
        return sorted(self._id_to_user[n] for n in self._adj[uid])

    def are_friends(self, u: str, v: str) -> bool:
        if not self.has_user(u) or not self.has_user(v):
            return False
        return self._user_to_id[v] in self._adj[self._user_to_id[u]]

    def remove_friendship(self, u: str, v: str) -> None:
        if not self.are_friends(u, v):
            return
        uid = self._user_to_id[u]
        vid = self._user_to_id[v]
        self._adj[uid].discard(vid)
        self._adj[vid].discard(uid)

    # =====================================================================
    # INTERNAL ACCESS HELPERS FOR BFS/DFS/Canvas
    # =====================================================================
    def get_user_id(self, username: str) -> int:
        return self._user_to_id[username]

    def get_user_name(self, uid: int) -> str:
        return self._id_to_user[uid]

    def get_neighbors(self, uid: int) -> List[int]:
        return list(self._adj[uid])

    # =====================================================================
    # ADJACENCY REPRESENTATIONS
    # =====================================================================
    def adjacency_list(self) -> Dict[str, List[str]]:
        result = {}
        for username, uid in self._user_to_id.items():
            result[username] = sorted(self._id_to_user[v] for v in self._adj[uid])
        return result

    def adjacency_matrix(self) -> List[List[int]]:
        n = len(self._id_to_user)
        matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in self._adj[u]:
                matrix[u][v] = 1
                matrix[v][u] = 1
        return matrix

    def users_in_order(self) -> List[str]:
        return list(self._id_to_user)

    def print_adjacency_list(self) -> str:
        lines = []
        adj = self.adjacency_list()
        for user in sorted(adj.keys()):
            friends = ", ".join(adj[user]) if adj[user] else "No friends"
            lines.append(f"{user}: {friends}")
        return "\n".join(lines)

    def print_adjacency_matrix(self) -> str:
        matrix = self.adjacency_matrix()
        users = self.users_in_order()
        n = len(users)
        header = "    " + "  ".join(f"{i:2d}" for i in range(n))
        lines = [header, ""]
        for i in range(n):
            row = "  ".join(str(val) for val in matrix[i])
            lines.append(f"{i:2d} | {row}   ({users[i]})")
        return "\n".join(lines)

    # =====================================================================
    # PERSISTENCE (SAVE & LOAD)
    # =====================================================================
    def save(self):
        data = {
            "users": self._id_to_user,
            "adj": [list(neigh) for neigh in self._adj]
        }
        with open(GRAPH_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(GRAPH_FILE):
            return  # first run → no saved data

        with open(GRAPH_FILE, "r") as f:
            data = json.load(f)

        # restore users
        self._id_to_user = data["users"]
        self._user_to_id = {name: idx for idx, name in enumerate(self._id_to_user)}

        # restore adjacency
        self._adj = [set(neigh) for neigh in data["adj"]]
