from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt

from social_graph.graph import Graph

# Import DSU if it exists — optional
try:
    from social_graph.dsu import DSU
    DSU_AVAILABLE = True
except ImportError:
    DSU_AVAILABLE = False


class CommunityWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Community Detection")
        self.setMinimumWidth(450)

        # ------------ Pastel Theme ------------
        self.setStyleSheet("""
            QDialog {
                background-color: #fff9f9;
            }
            QLabel {
                font-size: 15px;
                color: #4b4b4b;
            }
            QPushButton {
                background-color: #ffd4d4;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffbcbc;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ffcccc;
                border-radius: 8px;
                padding: 8px;
                color: #4b4b4b;
                font-size: 14px;
            }
        """)

        # ------------ Layout ------------
        layout = QVBoxLayout()

        title = QLabel("Detected Communities")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        layout.addWidget(title)

        btn_find = QPushButton("Find Communities")
        btn_find.clicked.connect(self.find_communities)
        layout.addWidget(btn_find)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    # ------------ Community Detection Logic ------------
    def find_communities(self):
        if not self.graph.get_all_users():
            self.output.setText("No users in graph.")
            return

        if DSU_AVAILABLE:
            result = self._find_components_dsu()
        else:
            result = self._find_components_dfs()

        # Format output
        text = ""
        for i, group in enumerate(result, 1):
            users_str = ", ".join(group)
            text += f"Group {i}: {users_str}\n"

        self.output.setText(text.strip())

    # ------------ DFS-Based Community Detection ------------
    def _find_components_dfs(self):
        users = self.graph.get_all_users()
        visited = set()
        components = []

        def dfs(user):
            stack = [user]
            group = []

            while stack:
                u = stack.pop()
                if u in visited:
                    continue
                visited.add(u)
                group.append(u)

                for friend in self.graph.get_friends(u):
                    if friend not in visited:
                        stack.append(friend)

            return group

        for user in users:
            if user not in visited:
                components.append(dfs(user))

        return components

    # ------------ DSU-Based Community Detection ------------
    def _find_components_dsu(self):
        users = self.graph.get_all_users()
        n = len(users)

        # Create DSU with n elements
        dsu = DSU(n)

        # Union all friendships
        for u in users:
            for v in self.graph.get_friends(u):
                dsu.union(self.graph._user_to_id[u], self.graph._user_to_id[v])

        # Build groups by root
        groups = {}

        for user in users:
            root = dsu.find(self.graph._user_to_id[user])
            groups.setdefault(root, []).append(user)

        return list(groups.values())
