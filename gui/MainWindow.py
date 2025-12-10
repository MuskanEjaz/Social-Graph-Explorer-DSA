# gui/MainWindow.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


from social_graph.graph import Graph

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

        # =======================================================
        # Window Setup
        # =======================================================
        self.setWindowTitle("🌐 Social Graph Explorer")
        self.resize(900, 600)
        self.setMinimumSize(750, 500)

        # Load graph
        self.graph = Graph()
        self.graph.load()

        # =======================================================
        # COMPLETELY NEW THEME (Lavender & Purple)
        # =======================================================
        self.setStyleSheet("""

            QMainWindow {
                background-color: #F4EEFF;             /* lavender mist */
            }

            QLabel#Title {
                background-color: #FFFFFF;
                padding: 18px;
                font-size: 33px;
                font-weight: 800;
                color: #4A3C8C;                        /* royal purple */
                border-radius: 16px;
                border: 2px solid #D3C2FF;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8D9FF,
                    stop:1 #C5A8FF
                );
                color: #3B2E6D;
                font-size: 19px;
                padding: 14px 20px;
                border-radius: 16px;
                font-weight: 600;
                border: none;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F3E8FF,
                    stop:1 #D5B9FF
                );
            }

            QPushButton:pressed {
                background-color: #B798FF;
            }
        """)

        # =======================================================
        # MAIN CONTAINER
        # =======================================================
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 50)
        layout.setSpacing(25)

        # Top Spacer
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Title
        title = QLabel("🌐 Social Graph Explorer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(25)

        # =======================================================
        # Button Column
        # =======================================================
        button_column = QVBoxLayout()
        button_column.setSpacing(18)
        button_column.setAlignment(Qt.AlignCenter)

        def add_button(text, callback):
            btn = QPushButton(text)
            btn.setMinimumWidth(360)
            btn.setMinimumHeight(47)
            btn.clicked.connect(callback)

            # Remove teammate styles
            btn.setStyleSheet("")

            # REAL SHADOW EFFECT
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setXOffset(2)
            shadow.setYOffset(3)
            shadow.setColor(Qt.gray)
            btn.setGraphicsEffect(shadow)

            button_column.addWidget(btn)


        add_button("➕ Add User", self.open_add_user)
        add_button("👥 Add Friendship", self.open_add_friend)
        add_button("🔎 BFS Traversal", self.open_bfs)
        add_button("🧭 DFS Traversal", self.open_dfs)
        add_button("🌐 Community Detection (DSU)", self.open_community)
        add_button("⭐ Friend Recommendations", self.open_recommendation)
        add_button("📊 Visualize Graph", self.open_graph_view)

        # Centering wrapper
        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(40, 0, 40, 0)
        wrapper.addStretch()
        wrapper.addLayout(button_column)
        wrapper.addStretch()
        layout.addLayout(wrapper)

        # Bottom spacer
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        container.setLayout(layout)
        self.setCentralWidget(container)

    def _refresh_and_save(self):
        self.graph.save()

    # =======================================================
    # Button Handlers
    # =======================================================
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

