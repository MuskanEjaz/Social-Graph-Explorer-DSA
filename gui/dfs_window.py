# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QPushButton,
#     QComboBox, QTextEdit
# )
# from PyQt5.QtCore import Qt
# from social_graph.graph import Graph
# from social_graph.dfs import dfs_traversal


# class DFSWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("DFS Traversal")
#         self.setMinimumWidth(400)

#         # -------- PASTEL THEME --------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f8f5ff;
#             }
#             QLabel {
#                 font-size: 15px;
#                 color: #4b4b4b;
#             }
#             QComboBox {
#                 padding: 8px;
#                 border-radius: 8px;
#                 border: 1px solid #c9bfff;
#                 background: white;
#             }
#             QPushButton {
#                 background-color: #c8e9ff;
#                 padding: 10px;
#                 border-radius: 10px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #b2ddff;
#             }
#             QTextEdit {
#                 background-color: #ffffff;
#                 border: 1px solid #dcd2ff;
#                 border-radius: 8px;
#                 padding: 8px;
#                 color: #4b4b4b;
#                 font-size: 14px;
#             }
#         """)

#         # -------- UI LAYOUT --------
#         layout = QVBoxLayout()

#         title = QLabel("Depth-First Traversal")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         layout.addWidget(title)

#         # Dropdown to choose starting user
#         layout.addWidget(QLabel("Start User:"))
#         self.combo_start = QComboBox()

#         users = self.graph.get_all_users()
#         self.combo_start.addItems(users)

#         layout.addWidget(self.combo_start)

#         # Run button
#         btn_run = QPushButton("Run DFS")
#         btn_run.clicked.connect(self.run_dfs)
#         layout.addWidget(btn_run)

#         # Output box
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#     def run_dfs(self):
#         start = self.combo_start.currentText()

#         if not start:
#             self.output.setText("Please select a starting user.")
#             return

#         result = dfs_traversal(self.graph, start)

#         if result:
#             self.output.setText(
#                 "DFS Order:\n\n" + " → ".join(result)
#             )
#         else:
#             self.output.setText("No traversal possible (user not found).")















# gui/dfs_window.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from gui.graph_canvas import GraphCanvas
from gui.dfs_animator import DFSAnimator
from social_graph.dfs import dfs_traversal


class DFSWindow(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("DFS Visualizer - Social Graph Explorer")
        self.setMinimumSize(1100, 600)

        # Root layout: Left controls + Right canvas
        root = QHBoxLayout()

        # -------------------------------------------------------------
        # LEFT PANEL (Controls + Output)
        # -------------------------------------------------------------
        left = QVBoxLayout()
        left.setSpacing(12)

        title = QLabel("Depth-First Search (DFS)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        left.addWidget(title)

        # Start user dropdown
        left.addWidget(QLabel("Start User:"))
        self.combo_start = QComboBox()
        users = sorted(self.graph.get_all_users())
        self.combo_start.addItems(users)
        left.addWidget(self.combo_start)

        # Run button
        btn_run = QPushButton("Run DFS")
        btn_run.clicked.connect(self.run_dfs)
        left.addWidget(btn_run)

        # Animation Controls
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_step = QPushButton("Step")
        self.btn_restart = QPushButton("Restart")

        self.btn_play.clicked.connect(self.play_anim)
        self.btn_pause.clicked.connect(self.pause_anim)
        self.btn_step.clicked.connect(self.step_anim)
        self.btn_restart.clicked.connect(self.restart_anim)

        left.addWidget(self.btn_play)
        left.addWidget(self.btn_pause)
        left.addWidget(self.btn_step)
        left.addWidget(self.btn_restart)

        # Output box
        left.addWidget(QLabel("Details:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        left.addWidget(self.output)
        left.addStretch()

        # -------------------------------------------------------------
        # RIGHT SIDE: Graph Canvas
        # -------------------------------------------------------------
        self.canvas = GraphCanvas(self.graph)
        root.addLayout(left, 0)
        root.addWidget(self.canvas, 1)

        self.setLayout(root)
        self.animator = None

    # ---------------------------------------------------------
    # DFS EXECUTION
    # ---------------------------------------------------------
    def run_dfs(self):
        start = self.combo_start.currentText()

        if not start:
            self.output.setText("Please select a valid user.")
            return

        result = dfs_traversal(self.graph, start, return_full=True)

        if not result.order:
            self.output.setText("DFS failed: user not found or graph empty.")
            return

        # Clear previous output
        self.output.clear()

        # Display traversal order
        self.output.append("DFS Order:\n" + " → ".join(result.order) + "\n")

        # Depth levels
        self.output.append("Node Depths:")
        for node, depth in result.depth.items():
            self.output.append(f"{node}: level {depth}")
        self.output.append("")

        # Parent tree
        self.output.append("Parent Tree (DFS Tree):")
        for node, parent in result.parent.items():
            self.output.append(f"{node} ← {parent}")
        self.output.append("")

        # Prepare animator
        self.canvas.reset_colors()
        self.animator = DFSAnimator(self.canvas, result, self.graph)

    # ---------------------------------------------------------
    # Animation controls
    # ---------------------------------------------------------
    def play_anim(self):
        if self.animator:
            self.animator.play()

    def pause_anim(self):
        if self.animator:
            self.animator.pause()

    def step_anim(self):
        if self.animator:
            self.animator.step()

    def restart_anim(self):
        if self.animator:
            self.animator.restart()
            self.canvas.reset_colors()