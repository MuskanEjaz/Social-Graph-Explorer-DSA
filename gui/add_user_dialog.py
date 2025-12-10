# gui/add_user_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AddUserDialog(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Add New User")
        self.setMinimumWidth(380)
        self.setFixedHeight(240)

        # =========================================================
        # MODERN LAVENDER THEME
        # =========================================================
        self.setStyleSheet("""
            QDialog {
                background-color: #F4EEFF;         /* soft lavender */
            }

            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: #4A3C8C;                    /* royal purple */
                margin-bottom: 6px;
            }

            QLineEdit {
                background: #FFFFFF;
                padding: 12px;
                border-radius: 12px;
                border: 2px solid #D7C8FF;
                font-size: 16px;
            }

            QLineEdit:focus {
                border: 2px solid #B79BFF;
                background: #FAF7FF;
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

        label = QLabel("Enter a new username:")
        layout.addWidget(label)

        # -------------------------
        # Text field (with shadow)
        # -------------------------
        self.user_field = QLineEdit()
        self.user_field.setPlaceholderText("e.g. Alice")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setXOffset(1)
        shadow.setYOffset(2)
        shadow.setColor(Qt.gray)
        self.user_field.setGraphicsEffect(shadow)

        layout.addWidget(self.user_field)

        # -------------------------
        # Button (with shadow)
        # -------------------------
        add_btn = QPushButton("Add User")

        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(20)
        btn_shadow.setXOffset(1)
        btn_shadow.setYOffset(3)
        btn_shadow.setColor(Qt.gray)
        add_btn.setGraphicsEffect(btn_shadow)

        add_btn.clicked.connect(self.add_user)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    # =========================================================
    # LOGIC — unchanged
    # =========================================================
    def add_user(self):
        username = self.user_field.text().strip()

        # Empty username
        if not username:
            QMessageBox.warning(self, "Invalid Input", "Username cannot be empty.")
            return

        # Duplicate user
        if self.graph.has_user(username):
            QMessageBox.warning(self, "Duplicate User",
                                f"'{username}' already exists in the graph.")
            return

        # Add user
        self.graph.add_user(username)

        # Inform main window
        self.accept()

        QMessageBox.information(self, "Success",
                                f"User '{username}' added successfully!")
