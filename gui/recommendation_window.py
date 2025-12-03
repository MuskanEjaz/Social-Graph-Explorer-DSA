# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QPushButton,
#     QComboBox, QTextEdit
# )
# from PyQt5.QtCore import Qt

# from social_graph.graph import Graph


# class RecommendationWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("Friend Recommendations")
#         self.setMinimumWidth(450)

#         # ---------- Pastel Style ----------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f9fff3;
#             }
#             QLabel {
#                 font-size: 15px;
#                 color: #4b4b4b;
#             }
#             QComboBox {
#                 padding: 8px;
#                 border-radius: 8px;
#                 border: 1px solid #b9f0c1;
#                 background: white;
#             }
#             QPushButton {
#                 background-color: #c8f7d0;
#                 padding: 10px;
#                 border-radius: 10px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #b0eab9;
#             }
#             QTextEdit {
#                 background-color: #ffffff;
#                 border: 1px solid #c8f7d0;
#                 border-radius: 8px;
#                 padding: 8px;
#                 color: #4b4b4b;
#                 font-size: 14px;
#             }
#         """)

#         # ---------- Layout ----------
#         layout = QVBoxLayout()

#         title = QLabel("People You May Know")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 12px;")
#         layout.addWidget(title)

#         # User selection
#         layout.addWidget(QLabel("Select User:"))
#         self.combo_user = QComboBox()
#         self.combo_user.addItems(self.graph.get_all_users())
#         layout.addWidget(self.combo_user)

#         # Button
#         btn = QPushButton("Show Recommendations")
#         btn.clicked.connect(self.show_recommendations)
#         layout.addWidget(btn)

#         # Output
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#     def show_recommendations(self):
#         user = self.combo_user.currentText()
#         if not user:
#             self.output.setText("Please choose a user.")
#             return

#         recommendations = self.compute_recommendations(user)

#         if not recommendations:
#             self.output.setText(f"No recommendations for {user}.")
#         else:
#             text = f"Recommended friends for {user}:\n\n" + "\n".join(
#                 f"• {name} ({mutuals} mutual friend(s))"
#                 for name, mutuals in recommendations
#             )
#             self.output.setText(text)

#     def compute_recommendations(self, user: str):
#         """
#         Simple mutual-friends recommendation:
#         Return: list of (username, mutual_friends_count)
#         """
#         user_friends = set(self.graph.get_friends(user))
#         all_users = set(self.graph.get_all_users())

#         recommendations = []

#         for other in all_users:
#             if other == user:
#                 continue
#             if other in user_friends:
#                 continue

#             # Count mutual friends
#             other_friends = set(self.graph.get_friends(other))
#             mutual = len(user_friends & other_friends)

#             if mutual > 0:
#                 recommendations.append((other, mutual))

#         # Sort by mutual friends DESC
#         recommendations.sort(key=lambda x: -x[1])

#         return recommendations



















# gui/recommendation_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt

from gui.graph_canvas import GraphCanvas
from social_graph.bfs import bfs_shortest_path


class RecommendationWindow(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("⭐ Friend Recommendations")
        self.setMinimumSize(1100, 600)

        # --------------------------------------------------------------------
        # THEME
        # --------------------------------------------------------------------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 16px;
                color: #4b4b4b;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcd2ff;
                border-radius: 8px;
                padding: 10px;
                color: #333;
                font-size: 14px;
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

        # --------------------------------------------------------------------
        # LAYOUT (LEFT = OPTIONS + RESULTS | RIGHT = GRAPH VIEW)
        # --------------------------------------------------------------------
        root = QHBoxLayout()

        left = QVBoxLayout()
        left.setSpacing(12)

        title = QLabel("Friend Recommendation System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        left.addWidget(title)

        # User selector
        left.addWidget(QLabel("Select User:"))
        self.combo_user = QComboBox()
        self.combo_user.addItems(sorted(self.graph.get_all_users()))
        left.addWidget(self.combo_user)

        # Run button
        btn = QPushButton("Generate Recommendations")
        btn.clicked.connect(self.run_recommendations)
        left.addWidget(btn)

        # Output display
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        left.addWidget(self.output)
        left.addStretch()

        # Right: Graph visualization
        self.canvas = GraphCanvas(self.graph)

        root.addLayout(left, 2)
        root.addWidget(self.canvas, 3)

        self.setLayout(root)

    # ======================================================================
    # MAIN RECOMMENDATION LOGIC
    # ======================================================================
    def run_recommendations(self):
        username = self.combo_user.currentText()
        if not username:
            self.output.setText("Please select a user.")
            return

        recommendations = self.get_recommendations(username)

        # --------------------------------------------------------------
        # Display results
        # --------------------------------------------------------------
        self.output.clear()
        self.output.append(f"Recommendations for {username}:\n")

        if not recommendations:
            self.output.append("No recommendations found.")
            return

        for idx, (user, score, mutual_count, distance) in enumerate(recommendations, 1):
            self.output.append(
                f"{idx}. {user}  |  Score={score:.3f} "
                f"(Mutual={mutual_count}, Distance={distance})"
            )

        # --------------------------------------------------------------
        # Highlight recommended users on canvas
        # --------------------------------------------------------------
        self.highlight_recommendations([rec[0] for rec in recommendations])

    # ======================================================================
    # COMPUTE RECOMMENDATIONS
    # ======================================================================
    def get_recommendations(self, user):
        """Returns list of tuples: (username, final_score, mutual_friends, bfs_distance)"""

        all_users = set(self.graph.get_all_users())
        friends = set(self.graph.get_friends(user))

        # Candidates = everyone except user and user's friends
        candidates = all_users - friends - {user}

        recommendations = []

        for other in candidates:
            # -------------------------------
            # 1. Mutual friends score
            # -------------------------------
            f_other = set(self.graph.get_friends(other))
            mutual = friends.intersection(f_other)
            mutual_count = len(mutual)

            # -------------------------------
            # 2. Distance score (via BFS shortest path)
            # -------------------------------
            bfs_res = bfs_shortest_path(
                self.graph, user, other, return_full_result=True
            )
            distance = bfs_res.distances.get(other, None)

            if distance is None:
                distance_score = 0
            else:
                distance_score = 1 / (1 + distance)

            # -------------------------------
            # Weighted final score
            # -------------------------------
            final_score = (mutual_count * 0.7) + (distance_score * 0.3)

            recommendations.append(
                (other, final_score, mutual_count, distance)
            )

        # sort by score decreasing
        recommendations.sort(key=lambda x: -x[1])
        return recommendations

    # ======================================================================
    # CANVAS HIGHLIGHTING
    # ======================================================================
    def highlight_recommendations(self, recommended_users):
        self.canvas.reset_colors()

        # pastel green recommendation color
        from PyQt5.QtGui import QColor
        rec_color = QColor("#b8f5c4")

        for u in recommended_users:
            uid = self.graph.get_user_id(u)
            self.canvas.nodes[uid].item.setBrush(rec_color)
