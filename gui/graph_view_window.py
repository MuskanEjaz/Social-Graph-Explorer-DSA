# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
# )
# from PyQt5.QtCore import Qt

# from social_graph.graph import Graph


# class GraphViewWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("Graph View (Adjacency List & Matrix)")
#         self.setMinimumWidth(550)

#         # ----------- Pastel Purple Theme -----------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f7f3ff;
#             }
#             QLabel {
#                 font-size: 16px;
#                 color: #4b4b4b;
#             }
#             QTextEdit {
#                 background-color: #ffffff;
#                 border: 1px solid #dcd2ff;
#                 border-radius: 8px;
#                 padding: 10px;
#                 font-size: 14px;
#                 color: #4b4b4b;
#             }
#             QPushButton {
#                 background-color: #d7c9ff;
#                 padding: 10px;
#                 border-radius: 10px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #cbbaff;
#             }
#         """)

#         # ----------- Layout Setup -----------
#         layout = QVBoxLayout()

#         title = QLabel("Graph Representation")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
#         layout.addWidget(title)

#         # Button to refresh the graph visuals
#         btn_refresh = QPushButton("Refresh View")
#         btn_refresh.clicked.connect(self.refresh_view)
#         layout.addWidget(btn_refresh)

#         # Text area to display adjacency list AND matrix
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#         # Initial rendering
#         self.refresh_view()

#     # ----------- Render Graph Data -----------
#     def refresh_view(self):
#         users = self.graph.get_all_users()

#         if not users:
#             self.output.setText("Graph is empty — add some users first.")
#             return

#         # Build adjacency list text
#         adj_list_str = self.graph.print_adjacency_list()

#         # Build adjacency matrix text
#         adj_matrix_str = self.graph.print_adjacency_matrix()

#         final_text = (
#             "=============================\n"
#             "        ADJACENCY LIST\n"
#             "=============================\n\n"
#             f"{adj_list_str}\n\n\n"
#             "=============================\n"
#             "       ADJACENCY MATRIX\n"
#             "=============================\n\n"
#             f"{adj_matrix_str}"
#         )

#         self.output.setText(final_text)










# gui/graph_view_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QTabWidget
)
from PyQt5.QtCore import Qt
from social_graph.graph import Graph


class GraphViewWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("📊 Graph Viewer - Social Graph Explorer")
        self.setMinimumSize(900, 600)

        # -------------------------------------------------------
        # Theme
        # -------------------------------------------------------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 17px;
                color: #4b4b4b;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcd2ff;
                border-radius: 8px;
                padding: 10px;
                color: #333333;
                font-size: 14px;
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
        """)

        # -------------------------------------------------------
        # Layout
        # -------------------------------------------------------
        root = QVBoxLayout()
        title = QLabel("📊 Graph Visualization & Structure")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        root.addWidget(title)

        # Tab Widget for multiple views
        tabs = QTabWidget()
        tabs.addTab(self._build_adj_list_tab(), "Adjacency List")
        tabs.addTab(self._build_adj_matrix_tab(), "Adjacency Matrix")
        tabs.addTab(self._build_stats_tab(), "Graph Statistics")

        root.addWidget(tabs)
        self.setLayout(root)

    # -------------------------------------------------------
    # Adjacency List Tab
    # -------------------------------------------------------
    def _build_adj_list_tab(self):
        w = QDialog()
        layout = QVBoxLayout()

        label = QLabel("Adjacency List Representation")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        box = QTextEdit()
        box.setReadOnly(True)
        box.setText(self.graph.print_adjacency_list())
        layout.addWidget(box)

        w.setLayout(layout)
        return w

    # -------------------------------------------------------
    # Adjacency Matrix Tab
    # -------------------------------------------------------
    def _build_adj_matrix_tab(self):
        w = QDialog()
        layout = QVBoxLayout()

        label = QLabel("Adjacency Matrix Representation")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        box = QTextEdit()
        box.setReadOnly(True)
        box.setText(self.graph.print_adjacency_matrix())
        layout.addWidget(box)

        w.setLayout(layout)
        return w

    # -------------------------------------------------------
    # Graph Statistics Tab
    # -------------------------------------------------------
    def _build_stats_tab(self):
        w = QDialog()
        layout = QVBoxLayout()

        label = QLabel("Graph Metrics & Summary")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        stats_text = QTextEdit()
        stats_text.setReadOnly(True)

        users = self.graph.get_all_users()
        matrix = self.graph.adjacency_matrix()

        node_count = len(users)
        edge_count = sum(sum(row) for row in matrix) // 2
        isolated = [u for u in users if len(self.graph.get_friends(u)) == 0]

        stats = [
            f"Total Users (Nodes): {node_count}",
            f"Total Friendships (Edges): {edge_count}",
            "",
            "List of Users:",
            ", ".join(sorted(users)),
            "",
            f"Isolated Users ({len(isolated)}):",
            ", ".join(isolated) if isolated else "None",
        ]

        stats_text.setText("\n".join(stats))
        layout.addWidget(stats_text)

        w.setLayout(layout)
        return w
