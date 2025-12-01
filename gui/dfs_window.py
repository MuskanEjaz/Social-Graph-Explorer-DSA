from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from social_graph.graph import Graph
from social_graph.dfs import dfs_traversal


class DFSWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("DFS Traversal")
        self.setMinimumWidth(400)

        # -------- PASTEL THEME --------
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
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b2ddff;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcd2ff;
                border-radius: 8px;
                padding: 8px;
                color: #4b4b4b;
                font-size: 14px;
            }
        """)

        # -------- UI LAYOUT --------
        layout = QVBoxLayout()

        title = QLabel("Depth-First Traversal")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Dropdown to choose starting user
        layout.addWidget(QLabel("Start User:"))
        self.combo_start = QComboBox()

        users = self.graph.get_all_users()
        self.combo_start.addItems(users)

        layout.addWidget(self.combo_start)

        # Run button
        btn_run = QPushButton("Run DFS")
        btn_run.clicked.connect(self.run_dfs)
        layout.addWidget(btn_run)

        # Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_dfs(self):
        start = self.combo_start.currentText()

        if not start:
            self.output.setText("Please select a starting user.")
            return

        result = dfs_traversal(self.graph, start)

        if result:
            self.output.setText(
                "DFS Order:\n\n" + " → ".join(result)
            )
        else:
            self.output.setText("No traversal possible (user not found).")
