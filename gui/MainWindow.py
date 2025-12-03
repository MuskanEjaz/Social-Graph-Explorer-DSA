# from PyQt5.QtWidgets import (
#     QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
# )
# from PyQt5.QtCore import Qt

# from social_graph.graph import Graph

# # Import windows
# from gui.add_user_dialog import AddUserDialog
# from gui.add_friend_dialog import AddFriendDialog
# from gui.bfs_window import BFSWindow
# from gui.dfs_window import DFSWindow
# from gui.community_window import CommunityWindow
# from gui.recommendation_window import RecommendationWindow
# from gui.graph_view_window import GraphViewWindow


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # ----- Window -----
#         self.setWindowTitle("🌐 Social Graph Explorer")
#         self.setMinimumSize(900, 700)
#         self.resize(1000, 750)

#         # ----- Vibrant Theme -----
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #eaf4ff;
#             }

#             QLabel#Title {
#                 font-size: 32px;
#                 font-weight: bold;
#                 color: #004b8d;
#                 margin-bottom: 20px;
#             }

#             QPushButton {
#                 background-color: #8fd3ff;
#                 color: #003352;
#                 font-size: 20px;
#                 padding: 14px;
#                 border-radius: 14px;
#                 border: 2px solid #64c0ff;
#             }

#             QPushButton:hover {
#                 background-color: #7ccbff;
#             }

#             QPushButton:pressed {
#                 background-color: #66baff;
#             }
#         """)

#         # Graph shared instance
#         self.graph = Graph()

#         # ----- Central Layout -----
#         central = QWidget()
#         layout = QVBoxLayout()
#         layout.setSpacing(25)
#         layout.setContentsMargins(70, 50, 70, 50)

#         # Title
#         title = QLabel("🌐 Social Graph Explorer")
#         title.setObjectName("Title")
#         title.setAlignment(Qt.AlignCenter)
#         layout.addWidget(title)

#         # Helper for button creation
#         def add_button(text, callback):
#             btn = QPushButton(text)
#             btn.setMinimumHeight(60)
#             btn.clicked.connect(callback)
#             layout.addWidget(btn)

#         # ----- Buttons (with Emojis + Vibrant Labels) -----
#         add_button("➕ Add User", self.open_add_user)
#         add_button("👥 Add Friendship", self.open_add_friend)
#         add_button("🔎 BFS Traversal", self.open_bfs)
#         add_button("🧭 DFS Traversal", self.open_dfs)
#         add_button("🌐 Community Detection (DSU)", self.open_community)
#         add_button("⭐ Friend Recommendations", self.open_recommendation)
#         add_button("📊 Visualize Graph", self.open_graph_view)

#         central.setLayout(layout)
#         self.setCentralWidget(central)

#     # ----- Open Windows -----
#     def open_add_user(self):
#         AddUserDialog(self.graph).exec_()

#     def open_add_friend(self):
#         AddFriendDialog(self.graph).exec_()

#     def open_bfs(self):
#         BFSWindow(self.graph).exec_()

#     def open_dfs(self):
#         DFSWindow(self.graph).exec_()

#     def open_community(self):
#         CommunityWindow(self.graph).exec_()

#     def open_recommendation(self):
#         RecommendationWindow(self.graph).exec_()

#     def open_graph_view(self):
#         GraphViewWindow(self.graph).exec_()














# gui/MainWindow.py
# gui/MainWindow.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt

from social_graph.graph import Graph

# Import windows
from gui.add_user_dialog import AddUserDialog
from gui.add_friend_dialog import AddFriendDialog
from gui.bfs_window import BFSWindow
from gui.dfs_window import DFSWindow
from gui.community_window import CommunityWindow
from gui.recommendation_window import RecommendationWindow
from gui.graph_view_window import GraphViewWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # -------------------------------------------------------
        # Window Setup
        # -------------------------------------------------------
        self.setWindowTitle("🌐 Social Graph Explorer")
        self.setMinimumSize(900, 700)
        self.resize(1100, 750)

        # -------------------------------------------------------
        # Graph instance (with load)
        # -------------------------------------------------------
        self.graph = Graph()
        self.graph.load()   # Load previous users + friendships

        # -------------------------------------------------------
        # BEAUTIFUL MODERN UI STYLE
        # -------------------------------------------------------
        self.setStyleSheet("""
            QMainWindow {
                background-color: #eef4ff;
            }

            QLabel#Title {
                font-size: 34px;
                font-weight: bold;
                color: #003a70;
                margin-bottom: 25px;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b8d9ff,
                    stop:1 #89c3ff
                );
                color: #003450;
                font-size: 20px;
                padding: 14px;
                border-radius: 14px;
                border: 2px solid #74b8ff;
                font-weight: 600;
            }

            QPushButton:hover {
                border: 2px solid #4fa4ff;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c7e4ff,
                    stop:1 #98d2ff
                );
            }

            QPushButton:pressed {
                background-color: #6fb6ff;
                border: 2px solid #3c8fe8;
            }
        """)

        # -------------------------------------------------------
        # Layout
        # -------------------------------------------------------
        central = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(70, 50, 70, 50)

        # Title
        title = QLabel("🌐 Social Graph Explorer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Helper function for cleaner code
        def add_button(text, callback):
            btn = QPushButton(text)
            btn.setMinimumHeight(60)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        # -------------------------------------------------------
        # MENU BUTTONS
        # -------------------------------------------------------
        add_button("➕ Add User", self.open_add_user)
        add_button("👥 Add Friendship", self.open_add_friend)
        add_button("🔎 BFS Traversal", self.open_bfs)
        add_button("🧭 DFS Traversal", self.open_dfs)
        add_button("🌐 Community Detection (DSU)", self.open_community)
        add_button("⭐ Friend Recommendations", self.open_recommendation)
        add_button("📊 Visualize Graph", self.open_graph_view)

        central.setLayout(layout)
        self.setCentralWidget(central)

    # =====================================================================
    # Save Graph Automatically After Any Modification
    # =====================================================================
    def _refresh_and_save(self):
        self.graph.save()

    # =====================================================================
    # Window Openers
    # =====================================================================
    def open_add_user(self):
        dlg = AddUserDialog(self.graph)
        if dlg.exec_():
            self._refresh_and_save()

    def open_add_friend(self):
        dlg = AddFriendDialog(self.graph)
        if dlg.exec_():
            self._refresh_and_save()

    def open_bfs(self):
        BFSWindow(self.graph).exec_()

    def open_dfs(self):
        DFSWindow(self.graph).exec_()

    def open_community(self):
        CommunityWindow(self.graph).exec_()

    def open_recommendation(self):
        RecommendationWindow(self.graph).exec_()

    def open_graph_view(self):
        GraphViewWindow(self.graph).exec_()

