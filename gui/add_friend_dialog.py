# gui/add_friend_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AddFriendDialog(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Add Friendship")
        self.setMinimumWidth(380)
        self.setFixedHeight(280)

        # =========================================================
        # LAVENDER THEME (matches MainWindow & AddUserDialog)
        # =========================================================
        self.setStyleSheet("""

            QDialog {
                background-color: #F4EEFF;         /* soft lavender */
            }

            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #4A3C8C;                    /* deep purple */
                margin-bottom: 4px;
            }

            QComboBox {
                background: #FFFFFF;
                padding: 10px;
                border-radius: 12px;
                border: 2px solid #D7C8FF;
                font-size: 15px;
                color: #3B2E6D;
            }

            QComboBox:hover {
                border: 2px solid #B79BFF;
                background-color: #FAF7FF;
            }

            QComboBox QAbstractItemView {
                selection-background-color: #DCC9FF;
                background-color: white;
                border-radius: 8px;
                border: 1px solid #C8B3FF;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8D9FF,
                    stop:1 #C5A8FF
                );
                padding: 12px;
                border-radius: 14px;
                font-size: 17px;
                font-weight: bold;
                color: #3B2E6D;
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

        # =========================================================
        # UI LAYOUT
        # =========================================================
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(25, 25, 25, 25)

        # -------------------------
        # User 1
        # -------------------------
        label1 = QLabel("Select User 1:")
        layout.addWidget(label1)

        self.combo_user1 = QComboBox()
        layout.addWidget(self.combo_user1)

        # Shadow effect
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(18)
        shadow1.setXOffset(1)
        shadow1.setYOffset(2)
        self.combo_user1.setGraphicsEffect(shadow1)

        # -------------------------
        # User 2
        # -------------------------
        label2 = QLabel("Select User 2:")
        layout.addWidget(label2)

        self.combo_user2 = QComboBox()
        layout.addWidget(self.combo_user2)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(18)
        shadow2.setXOffset(1)
        shadow2.setYOffset(2)
        self.combo_user2.setGraphicsEffect(shadow2)

        # Load users
        users = sorted(self.graph.get_all_users())
        self.combo_user1.addItems(users)
        self.combo_user2.addItems(users)

        # -------------------------
        # Add Button
        # -------------------------
        btn = QPushButton("Add Friendship")

        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(18)
        btn_shadow.setXOffset(1)
        btn_shadow.setYOffset(3)
        btn.setGraphicsEffect(btn_shadow)

        btn.clicked.connect(self.add_friendship)

        layout.addWidget(btn)

        self.setLayout(layout)

    # =========================================================
    # LOGIC (unchanged)
    # =========================================================
    def add_friendship(self):
        u = self.combo_user1.currentText()
        v = self.combo_user2.currentText()

        if not u or not v:
            QMessageBox.warning(self, "Invalid Selection",
                                "Both users must be selected.")
            return

        if u == v:
            QMessageBox.warning(self, "Invalid Friendship",
                                "A user cannot befriend themselves.")
            return

        if self.graph.are_friends(u, v):
            QMessageBox.warning(self, "Already Friends",
                                f"{u} and {v} are already friends.")
            return

        self.graph.add_friendship(u, v)

        self.accept()

        QMessageBox.information(self, "Success",
                                f"{u} and {v} are now friends!")
