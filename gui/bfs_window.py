# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QPushButton,
#     QComboBox, QTextEdit
# )
# from PyQt5.QtCore import Qt
# from social_graph.graph import Graph
# from social_graph.bfs import bfs_shortest_path


# class BFSWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("BFS Shortest Path")
#         self.setMinimumWidth(400)

#         # -------- GLOBAL PASTEL THEME --------
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

#         # -------- UI ELEMENTS --------
#         layout = QVBoxLayout()

#         title = QLabel("Find Shortest Path Using BFS")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         layout.addWidget(title)

#         # Dropdown labels
#         layout.addWidget(QLabel("Start User:"))
#         self.combo_start = QComboBox()

#         layout.addWidget(QLabel("Target User:"))
#         self.combo_end = QComboBox()

#         # Load user list
#         users = self.graph.get_all_users()
#         self.combo_start.addItems(users)
#         self.combo_end.addItems(users)

#         layout.addWidget(self.combo_start)
#         layout.addWidget(self.combo_end)

#         # Run BFS button
#         btn_run = QPushButton("Run BFS")
#         btn_run.clicked.connect(self.run_bfs)
#         layout.addWidget(btn_run)

#         # Output display
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#     def run_bfs(self):
#         start = self.combo_start.currentText()
#         end = self.combo_end.currentText()

#         if not start or not end:
#             self.output.setText("Please select two users.")
#             return

#         if start == end:
#             self.output.setText("Start and end users must be different.")
#             return

#         # Call your BFS algorithm
#         path = bfs_shortest_path(self.graph, start, end)

#         if path:
#             self.output.setText(
#                 f"Shortest path from {start} to {end}:\n\n" +
#                 " → ".join(path)
#             )
#         else:
#             self.output.setText(f"No path found between {start} and {end}.")











# gui/bfs_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from social_graph.bfs import bfs_shortest_path
from .graph_canvas import GraphCanvas
from .bfs_animator import BFSAnimator


class BFSWindow(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("BFS Visualizer - Social Graph Explorer")
        self.setMinimumSize(1150, 650)

        self.animator = None

        self._build_ui()
        self._load_users()
        self._update_button_states(disable_all=True)

    # ---------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------
    def _build_ui(self):
        root = QHBoxLayout()
        left = QVBoxLayout()

        # Title
        title = QLabel("BFS Shortest Path Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        left.addWidget(title)

        # Start user
        left.addWidget(QLabel("Start User:"))
        self.combo_start = QComboBox()
        left.addWidget(self.combo_start)

        # End user
        left.addWidget(QLabel("Target User:"))
        self.combo_end = QComboBox()
        left.addWidget(self.combo_end)

        # Run BFS button
        self.btn_run = QPushButton("Run BFS")
        self.btn_run.clicked.connect(self.run_bfs)
        left.addWidget(self.btn_run)

        # Animation control buttons
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_step = QPushButton("⏭ Step")
        self.btn_restart = QPushButton("🔄 Restart")

        self.btn_play.clicked.connect(self.play_anim)
        self.btn_pause.clicked.connect(self.pause_anim)
        self.btn_step.clicked.connect(self.step_anim)
        self.btn_restart.clicked.connect(self.restart_anim)

        left.addWidget(self.btn_play)
        left.addWidget(self.btn_pause)
        left.addWidget(self.btn_step)
        left.addWidget(self.btn_restart)

        # Details Box
        left.addWidget(QLabel("Details:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        left.addWidget(self.output)

        left.addStretch()

        # Right panel: Graph Canvas
        self.canvas = GraphCanvas(self.graph)

        root.addLayout(left, 0)
        root.addWidget(self.canvas, 1)

        self.setLayout(root)

        # Apply UI styling
        self._apply_theme()

    # ---------------------------------------------------------
    # THEME / STYLING
    # ---------------------------------------------------------
    def _apply_theme(self):
        self.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 14px;
                border-radius: 8px;
                background-color: #c8e9ff;
            }
            QPushButton:hover {
                background-color: #b8ddff;
            }
            QComboBox {
                padding: 6px;
                font-size: 14px;
            }
            QTextEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
        """)

    # ---------------------------------------------------------
    # Load users into dropdowns
    # ---------------------------------------------------------
    def _load_users(self):
        self.combo_start.clear()
        self.combo_end.clear()

        users = sorted(self.graph.get_all_users())

        if not users:
            self.output.setText("⚠ No users found in the graph.\nAdd users first from the main menu.")
            return

        self.combo_start.addItems(users)
        self.combo_end.addItems(users)

    # ---------------------------------------------------------
    # Enable / Disable animation controls
    # ---------------------------------------------------------
    def _update_button_states(self, disable_all=False):
        """Disable animation buttons until BFS is run."""
        buttons = [self.btn_play, self.btn_pause, self.btn_step, self.btn_restart]

        for b in buttons:
            b.setEnabled(not disable_all)

        if disable_all:
            for b in buttons:
                b.setStyleSheet("background-color: #dddddd; color: #666;")

    # ---------------------------------------------------------
    # RUN BFS
    # ---------------------------------------------------------
    def run_bfs(self):
        start = self.combo_start.currentText()
        end = self.combo_end.currentText()

        if not start or not end:
            self.output.setText(" Please select both users.")
            return

        if start == end:
            self.output.setText(" Start and target users must be different.")
            return

        result = bfs_shortest_path(self.graph, start, end, return_full_result=True)

        if not result.path:
            self.output.setText(f" No path found between {start} and {end}.")
            return

        # Fill output box
        self.output.clear()
        self.output.append(f"Shortest Path:\n → {' → '.join(result.path)}\n")
        self.output.append("Visited Order:\n" + " → ".join(result.visited_order) + "\n")
        self.output.append("Distances:")
        for u, d in result.distances.items():
            self.output.append(f"• {u}: {d}")

        # Reset canvas + create new animator
        self.canvas.reset_colors()
        self.animator = BFSAnimator(self.canvas, result, self.graph)

        # Enable animation buttons
        self._update_button_states(disable_all=False)

    # ---------------------------------------------------------
    # ANIMATION CONTROLS
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
