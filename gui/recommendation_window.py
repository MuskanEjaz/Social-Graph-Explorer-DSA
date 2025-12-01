from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt

from social_graph.graph import Graph


class RecommendationWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Friend Recommendations")
        self.setMinimumWidth(450)

        # ---------- Pastel Style ----------
        self.setStyleSheet("""
            QDialog {
                background-color: #f9fff3;
            }
            QLabel {
                font-size: 15px;
                color: #4b4b4b;
            }
            QComboBox {
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #b9f0c1;
                background: white;
            }
            QPushButton {
                background-color: #c8f7d0;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b0eab9;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #c8f7d0;
                border-radius: 8px;
                padding: 8px;
                color: #4b4b4b;
                font-size: 14px;
            }
        """)

        # ---------- Layout ----------
        layout = QVBoxLayout()

        title = QLabel("People You May Know")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # User selection
        layout.addWidget(QLabel("Select User:"))
        self.combo_user = QComboBox()
        self.combo_user.addItems(self.graph.get_all_users())
        layout.addWidget(self.combo_user)

        # Button
        btn = QPushButton("Show Recommendations")
        btn.clicked.connect(self.show_recommendations)
        layout.addWidget(btn)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def show_recommendations(self):
        user = self.combo_user.currentText()
        if not user:
            self.output.setText("Please choose a user.")
            return

        recommendations = self.compute_recommendations(user)

        if not recommendations:
            self.output.setText(f"No recommendations for {user}.")
        else:
            text = f"Recommended friends for {user}:\n\n" + "\n".join(
                f"• {name} ({mutuals} mutual friend(s))"
                for name, mutuals in recommendations
            )
            self.output.setText(text)

    def compute_recommendations(self, user: str):
        """
        Simple mutual-friends recommendation:
        Return: list of (username, mutual_friends_count)
        """
        user_friends = set(self.graph.get_friends(user))
        all_users = set(self.graph.get_all_users())

        recommendations = []

        for other in all_users:
            if other == user:
                continue
            if other in user_friends:
                continue

            # Count mutual friends
            other_friends = set(self.graph.get_friends(other))
            mutual = len(user_friends & other_friends)

            if mutual > 0:
                recommendations.append((other, mutual))

        # Sort by mutual friends DESC
        recommendations.sort(key=lambda x: -x[1])

        return recommendations
