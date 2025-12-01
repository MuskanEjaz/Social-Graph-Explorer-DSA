from typing import Dict, List, Set

class Graph:
    def __init__(self) -> None:
        self._user_to_id: Dict[str, int] = {}  # username -> internal index
        self._id_to_user: List[str] = []  # index -> username (list index is the id)
        self._adj: List[Set[int]] = []  # adjacency list: list[id] -> set of neighbor ids

    # ---------- User Management ----------

    def add_user(self, username: str) -> None:
        # Basic validation
        if not username or not username.strip():
            return

        # Already exists
        if username in self._user_to_id:
            return
    
        # Add new user
        new_id = len(self._id_to_user)
        self._user_to_id[username] = new_id
        self._id_to_user.append(username)
        self._adj.append(set())

    def has_user(self, username: str) -> bool:
        return username in self._user_to_id
    
    def get_all_users(self) -> List[str]:
        # Return all usernames
        return list(self._user_to_id.keys())
    
    # ---------- Friendships (Edges) ----------
    def add_friendship(self, u: str, v: str) -> None:
        # Add an undirected edge between users u and v. Automatically add users if they do not exist
        if u == v:
            return  # Same user
        
        if not self.has_user(u):
            self.add_user(u)

        if not self.has_user(v):
            self.add_user(v)
        
        u_id = self._user_to_id[u]
        v_id = self._user_to_id[v]

        self._adj[u_id].add(v_id)
        self._adj[v_id].add(u_id)

    def get_friends(self, username: str) -> List[str]:
        if not self.has_user(username):
            return []
        
        u_id = self._user_to_id[username]
        neighbors_ids = self._adj[u_id]
        return sorted(self._id_to_user[v_id] for v_id in neighbors_ids)
    
    def are_friends(self, u: str, v: str) -> bool:
        # Check if both users exist
        if not self.has_user(u) or not self.has_user(v):
            return False
        
        u_id = self._user_to_id[u]
        v_id = self._user_to_id[v]
        return v_id in self._adj[u_id]
    def remove_friendship(self, u: str, v: str) -> None:
        # Remove an undirected edge if it exists
        if not self.are_friends(u, v):
            return
        
        u_id = self._user_to_id[u]
        v_id = self._user_to_id[v]

        self._adj[u_id].remove(v_id)
        self._adj[v_id].remove(u_id)

    # ---------- Adjacency Matrix ----------
    def adjacency_list(self) -> Dict[str, List[str]]:
        # Return List like
        # {Alice: [Bob, Charlie], .....}

        result: Dict[str, List[str]] = {}
        for username, id in self._user_to_id.items():
            neighbors_ids = self._adj[id]
            result[username] = sorted(self._id_to_user[v_id] for v_id in neighbors_ids)
        return result
    
    def adjacency_matrix(self) -> List[List[int]]:
        n = len(self._id_to_user)  # number of users
        matrix = [[0] * n for _ in range(n)]

        for u_id in range(n):  # for each user
            for v_id in self._adj[u_id]:  #  friends of the user
                matrix[u_id][v_id] = 1
                matrix[v_id][u_id] = 1
        return matrix
    
    def users_in_order(self) -> List[str]:
        # Return names in same order as in rows/cols of adjacency matrix
        return list(self._id_to_user)
    

    # ---------- Print Functions ----------
    def print_adjacency_list(self) -> str:
        lines = []
        adj = self.adjacency_list()
        for user in sorted(adj.keys()):
            friends_str = ", ".join(adj[user]) if adj[user] else "No friends"
            lines.append(f"{user}: {friends_str}")
        return "\n".join(lines)
    
    def print_adjacency_matrix(self) -> str:
        users = self.users_in_order()
        matrix = self.adjacency_matrix()
        n = len(users)  # number of users

        header = "    " + "  ".join(f"{i:2d}" for i in range(n))
        lines = [header, ""]

        for i in range(n):
            row_vals = "  ".join(str(matrix[i][j]) for j in range(n))
            lines.append(f"{i:2d} | {row_vals}  ({users[i]})")
        return "\n".join(lines)
    
