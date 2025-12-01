from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
)
from PyQt5.QtCore import Qt

from social_graph.graph import Graph


class GraphViewWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Graph View (Adjacency List & Matrix)")
        self.setMinimumWidth(550)

        # ----------- Pastel Purple Theme -----------
        self.setStyleSheet("""
            QDialog {
                background-color: #f7f3ff;
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
                font-size: 14px;
                color: #4b4b4b;
            }
            QPushButton {
                background-color: #d7c9ff;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #cbbaff;
            }
        """)

        # ----------- Layout Setup -----------
        layout = QVBoxLayout()

        title = QLabel("Graph Representation")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Button to refresh the graph visuals
        btn_refresh = QPushButton("Refresh View")
        btn_refresh.clicked.connect(self.refresh_view)
        layout.addWidget(btn_refresh)

        # Text area to display adjacency list AND matrix
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

        # Initial rendering
        self.refresh_view()

    # ----------- Render Graph Data -----------
    def refresh_view(self):
        users = self.graph.get_all_users()

        if not users:
            self.output.setText("Graph is empty — add some users first.")
            return

        # Build adjacency list text
        adj_list_str = self.graph.print_adjacency_list()

        # Build adjacency matrix text
        adj_matrix_str = self.graph.print_adjacency_matrix()

        final_text = (
            "=============================\n"
            "        ADJACENCY LIST\n"
            "=============================\n\n"
            f"{adj_list_str}\n\n\n"
            "=============================\n"
            "       ADJACENCY MATRIX\n"
            "=============================\n\n"
            f"{adj_matrix_str}"
        )

        self.output.setText(final_text)
