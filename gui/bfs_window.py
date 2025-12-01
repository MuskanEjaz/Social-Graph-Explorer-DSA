from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from social_graph.graph import Graph
from social_graph.bfs import bfs_shortest_path


class BFSWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("BFS Shortest Path")
        self.setMinimumWidth(400)

        # -------- GLOBAL PASTEL THEME --------
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

        # -------- UI ELEMENTS --------
        layout = QVBoxLayout()

        title = QLabel("Find Shortest Path Using BFS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Dropdown labels
        layout.addWidget(QLabel("Start User:"))
        self.combo_start = QComboBox()

        layout.addWidget(QLabel("Target User:"))
        self.combo_end = QComboBox()

        # Load user list
        users = self.graph.get_all_users()
        self.combo_start.addItems(users)
        self.combo_end.addItems(users)

        layout.addWidget(self.combo_start)
        layout.addWidget(self.combo_end)

        # Run BFS button
        btn_run = QPushButton("Run BFS")
        btn_run.clicked.connect(self.run_bfs)
        layout.addWidget(btn_run)

        # Output display
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_bfs(self):
        start = self.combo_start.currentText()
        end = self.combo_end.currentText()

        if not start or not end:
            self.output.setText("Please select two users.")
            return

        if start == end:
            self.output.setText("Start and end users must be different.")
            return

        # Call your BFS algorithm
        path = bfs_shortest_path(self.graph, start, end)

        if path:
            self.output.setText(
                f"Shortest path from {start} to {end}:\n\n" +
                " → ".join(path)
            )
        else:
            self.output.setText(f"No path found between {start} and {end}.")
