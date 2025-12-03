# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
# )
# from PyQt5.QtCore import Qt

# from social_graph.graph import Graph

# # Import DSU if it exists — optional
# try:
#     from social_graph.dsu import DSU
#     DSU_AVAILABLE = True
# except ImportError:
#     DSU_AVAILABLE = False


# class CommunityWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("Community Detection")
#         self.setMinimumWidth(450)

#         # ------------ Pastel Theme ------------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #fff9f9;
#             }
#             QLabel {
#                 font-size: 15px;
#                 color: #4b4b4b;
#             }
#             QPushButton {
#                 background-color: #ffd4d4;
#                 padding: 10px;
#                 border-radius: 10px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #ffbcbc;
#             }
#             QTextEdit {
#                 background-color: white;
#                 border: 1px solid #ffcccc;
#                 border-radius: 8px;
#                 padding: 8px;
#                 color: #4b4b4b;
#                 font-size: 14px;
#             }
#         """)

#         # ------------ Layout ------------
#         layout = QVBoxLayout()

#         title = QLabel("Detected Communities")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

#         layout.addWidget(title)

#         btn_find = QPushButton("Find Communities")
#         btn_find.clicked.connect(self.find_communities)
#         layout.addWidget(btn_find)

#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#     # ------------ Community Detection Logic ------------
#     def find_communities(self):
#         if not self.graph.get_all_users():
#             self.output.setText("No users in graph.")
#             return

#         if DSU_AVAILABLE:
#             result = self._find_components_dsu()
#         else:
#             result = self._find_components_dfs()

#         # Format output
#         text = ""
#         for i, group in enumerate(result, 1):
#             users_str = ", ".join(group)
#             text += f"Group {i}: {users_str}\n"

#         self.output.setText(text.strip())

#     # ------------ DFS-Based Community Detection ------------
#     def _find_components_dfs(self):
#         users = self.graph.get_all_users()
#         visited = set()
#         components = []

#         def dfs(user):
#             stack = [user]
#             group = []

#             while stack:
#                 u = stack.pop()
#                 if u in visited:
#                     continue
#                 visited.add(u)
#                 group.append(u)

#                 for friend in self.graph.get_friends(u):
#                     if friend not in visited:
#                         stack.append(friend)

#             return group

#         for user in users:
#             if user not in visited:
#                 components.append(dfs(user))

#         return components

#     # ------------ DSU-Based Community Detection ------------
#     def _find_components_dsu(self):
#         users = self.graph.get_all_users()
#         n = len(users)

#         # Create DSU with n elements
#         dsu = DSU(n)

#         # Union all friendships
#         for u in users:
#             for v in self.graph.get_friends(u):
#                 dsu.union(self.graph._user_to_id[u], self.graph._user_to_id[v])

#         # Build groups by root
#         groups = {}

#         for user in users:
#             root = dsu.find(self.graph._user_to_id[user])
#             groups.setdefault(root, []).append(user)

#         return list(groups.values())

















# gui/community_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from social_graph.dsu import DSU
from social_graph.graph import Graph
from gui.graph_canvas import GraphCanvas
from PyQt5.QtGui import QColor


class CommunityWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("🌐 Community Detection (Connected Components)")
        self.setMinimumSize(1100, 600)

        # -------------------------------------------------------
        # Style
        # -------------------------------------------------------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcd2ff;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: #c8e9ff;
                padding: 10px;
                border-radius: 10px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #b2ddff;
            }
        """)

        # -------------------------------------------------------
        # Layout (Left = summary, Right = GraphCanvas)
        # -------------------------------------------------------
        root = QHBoxLayout()

        left = QVBoxLayout()
        left.setSpacing(10)

        title = QLabel("Community Detection Using DSU")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        left.addWidget(title)

        # Summary output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        left.addWidget(self.output)

        # Button to refresh communities
        btn_refresh = QPushButton("Refresh Communities")
        btn_refresh.clicked.connect(self.show_communities)
        left.addWidget(btn_refresh)

        left.addStretch()
        root.addLayout(left, 1)

        # Graph Canvas (color communities)
        self.canvas = GraphCanvas(graph)
        root.addWidget(self.canvas, 2)

        self.setLayout(root)

        # Compute and display communities
        self.show_communities()

    # -------------------------------------------------------
    # Community detection logic (DSU)
    # -------------------------------------------------------
    def show_communities(self):
        users = self.graph.get_all_users()
        n = len(users)
        user_to_id = {u: self.graph.get_user_id(u) for u in users}

        # Run DSU over all friendships
        dsu = DSU(n)

        for u in users:
            for v in self.graph.get_friends(u):
                dsu.union(user_to_id[u], user_to_id[v])

        # Group users by root
        communities = {}
        for u in users:
            root = dsu.find(user_to_id[u])
            communities.setdefault(root, []).append(u)

        # ---------------------------------------------------
        # Display community info (left panel)
        # ---------------------------------------------------
        self.output.clear()

        self.output.append(f"Total Users: {n}")
        self.output.append(f"Total Communities: {len(communities)}\n")

        sorted_comms = sorted(communities.values(), key=lambda x: -len(x))

        for i, group in enumerate(sorted_comms, 1):
            self.output.append(f"Community {i}  (size = {len(group)})")
            self.output.append("Members: " + ", ".join(sorted(group)))
            self.output.append("")

        # ---------------------------------------------------
        # Color communities on GraphCanvas (right panel)
        # ---------------------------------------------------
        self._color_communities(sorted_comms)

    # -------------------------------------------------------
    # Color nodes by community group
    # -------------------------------------------------------
    def _color_communities(self, communities):
        # soft pastel colors
        palette = [
            QColor("#b8e1ff"), QColor("#ffd580"), QColor("#d4ffb2"),
            QColor("#ffb2d8"), QColor("#e3b2ff"), QColor("#b2ffc8"),
            QColor("#ffdfba"), QColor("#bae1ff")
        ]

        self.canvas.reset_colors()

        for idx, group in enumerate(communities):
            color = palette[idx % len(palette)]

            for username in group:
                uid = self.graph.get_user_id(username)
                self.canvas.nodes[uid].item.setBrush(color)
