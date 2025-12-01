from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox
)
from PyQt5.QtCore import Qt


class AddFriendDialog(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Add Friendship")
        self.setMinimumWidth(340)

        # -------- GLOBAL STYLE --------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 15px;
                color: #4b4b4b;
            }
            QComboBox {
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #c9bfff;
                background: white;
            }
            QPushButton {
                background-color: #c8e9ff;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b2ddff;
            }
            QPushButton:pressed {
                background-color: #9bd1ff;
            }
        """)

        # -------- UI ELEMENTS --------
        layout = QVBoxLayout()

        label1 = QLabel("Select User 1:")
        label2 = QLabel("Select User 2:")

        self.combo_user1 = QComboBox()
        self.combo_user2 = QComboBox()

        # Fill dropdown lists with current users
        users = self.graph.get_all_users()
        self.combo_user1.addItems(users)
        self.combo_user2.addItems(users)

        add_btn = QPushButton("Add Friendship")
        add_btn.clicked.connect(self.add_friendship)

        layout.addWidget(label1)
        layout.addWidget(self.combo_user1)

        layout.addWidget(label2)
        layout.addWidget(self.combo_user2)

        layout.addWidget(add_btn)

        self.setLayout(layout)

    def add_friendship(self):
        u = self.combo_user1.currentText()
        v = self.combo_user2.currentText()

        # Validation
        if u and v and u != v:
            self.graph.add_friendship(u, v)

        self.close()
