# # gui/add_user_dialog.py
# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt

# class AddUserDialog(QDialog):
#     def __init__(self, graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("Add New User")
#         self.setMinimumWidth(320)

#         # -------- STYLE --------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f8f5ff;     /* pastel lavender */
#             }
#             QLabel {
#                 font-size: 15px;
#                 color: #4b4b4b;
#             }
#             QLineEdit {
#                 padding: 8px;
#                 border-radius: 8px;
#                 border: 1px solid #c9bfff;
#                 background: white;
#             }
#             QPushButton {
#                 background-color: #b4e1ff;     /* pastel blue */
#                 padding: 8px;
#                 border-radius: 8px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #9ad4ff;
#             }
#             QPushButton:pressed {
#                 background-color: #7bc7ff;
#             }
#         """)

#         # -------- UI Layout --------
#         layout = QVBoxLayout()

#         label = QLabel("Enter a new username:")
#         self.user_field = QLineEdit()
#         self.user_field.setPlaceholderText("e.g. Alice")

#         add_btn = QPushButton("Add User")
#         add_btn.clicked.connect(self.add_user)

#         layout.addWidget(label)
#         layout.addWidget(self.user_field)
#         layout.addWidget(add_btn)

#         self.setLayout(layout)

#     def add_user(self):
#         username = self.user_field.text().strip()

#         if username:
#             self.graph.add_user(username)

#         self.close()











# gui/add_user_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class AddUserDialog(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Add New User")
        self.setMinimumWidth(340)

        # -------- STYLE --------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 15px;
                color: #4b4b4b;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #c9bfff;
                background: white;
            }
            QPushButton {
                background-color: #b4e1ff;
                padding: 10px;
                border-radius: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #9ad4ff;
            }
            QPushButton:pressed {
                background-color: #7bc7ff;
            }
        """)

        # -------- UI Layout --------
        layout = QVBoxLayout()
        layout.setSpacing(12)

        label = QLabel("Enter a new username:")
        self.user_field = QLineEdit()
        self.user_field.setPlaceholderText("e.g. Alice")

        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.add_user)

        layout.addWidget(label)
        layout.addWidget(self.user_field)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    # ----------------------------------------------------
    # Add User Logic
    # ----------------------------------------------------
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

        # Add the new user
        self.graph.add_user(username)

        # Return success to MainWindow
        self.accept()    # <--- VERY IMPORTANT (used by MainWindow)

        QMessageBox.information(self, "Success",
                                f"User '{username}' added successfully!")
