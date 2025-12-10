# gui/bfs_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QMessageBox, QWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from social_graph.bfs import bfs_shortest_path
from .graph_canvas import GraphCanvas
from .bfs_animator import BFSAnimator


class BFSWindow(QDialog):
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.animator = None

        # Much more compact & visible
        self.setWindowTitle("BFS Visualizer - Social Graph Explorer")
        self.resize(1080, 600)
        self.setMinimumSize(900, 540)

        self._build_ui()
        self._load_users()
        self._update_button_states(disable_all=True)

    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def _build_ui(self):
        root = QHBoxLayout()
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(20)

        # LEFT PANEL INSIDE A SCROLL AREA
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(18)
        left_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(left_container)

        # TITLE ------------------------------------------------
        title = QLabel("🔎 BFS Shortest Path Visualizer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # Start User -------------------------------------------
        lbl_start = QLabel("Start User:")
        lbl_start.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_start)

        self.combo_start = QComboBox()
        self.combo_start.setMinimumHeight(36)
        left_layout.addWidget(self.combo_start)

        # End User ---------------------------------------------
        lbl_end = QLabel("Target User:")
        lbl_end.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_end)

        self.combo_end = QComboBox()
        self.combo_end.setMinimumHeight(36)
        left_layout.addWidget(self.combo_end)

        # Run BFS Button ---------------------------------------
        self.btn_run = QPushButton("Run BFS")
        self.btn_run.setObjectName("runButton")
        self._style_button(self.btn_run)
        left_layout.addWidget(self.btn_run)
        self.btn_run.clicked.connect(self.run_bfs)

        # Animation Buttons ------------------------------------
        self.btn_play = QPushButton("▶ Play")
        self.btn_play.setProperty("class", "controlBtn")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_pause.setProperty("class", "controlBtn")
        self.btn_step = QPushButton("⏭ Step")
        self.btn_step.setProperty("class", "controlBtn")
        self.btn_restart = QPushButton("🔄 Restart")
        self.btn_restart.setProperty("class", "controlBtn")


        for b in (self.btn_play, self.btn_pause, self.btn_step, self.btn_restart):
            self._style_button(b)
            left_layout.addWidget(b)

        self.btn_play.clicked.connect(self.play_anim)
        self.btn_pause.clicked.connect(self.pause_anim)
        self.btn_step.clicked.connect(self.step_anim)
        self.btn_restart.clicked.connect(self.restart_anim)

        # DETAILS LABEL ----------------------------------------
        lbl_details = QLabel("Details:")
        lbl_details.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_details)

        # DETAILS BOX (fixed visible height)
        self.output = QTextEdit()
        self.output.setMinimumHeight(200)
        self.output.setReadOnly(True)
        left_layout.addWidget(self.output)

        # Spacer to improve layout
        left_layout.addStretch()

        # ======================================================
        # RIGHT PANEL — Graph Canvas
        # ======================================================
        self.canvas = GraphCanvas(self.graph)

        root.addWidget(scroll_area, 0)  # never expands too large
        root.addWidget(self.canvas, 1)   # canvas expands instead

        self.setLayout(root)
        self._apply_theme()

    # Style buttons consistently
    def _style_button(self, btn):
        btn.setMinimumHeight(48)
        btn.setStyleSheet("font-size: 15px; font-weight: bold; padding: 6px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(1)
        shadow.setYOffset(2)
        btn.setGraphicsEffect(shadow)

    # ---------------------------------------------------------
    # THEME
    # ---------------------------------------------------------
    def _apply_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f3eaff;
            }

            /* Titles */
            QLabel {
                color: #3b2a66;
                font-size: 15px;
                font-weight: bold;
            }

            /* Dropdowns */
            QComboBox {
                background: #ffffff;
                border: 2px solid #d2c3ff;
                border-radius: 10px;
                padding: 6px 10px;
                font-size: 15px;
            }
            QComboBox:hover {
                border: 2px solid #b9a3ff;
            }

            /* MAIN ACTION BUTTON */
            QPushButton#runButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dec0ff,
                    stop:1 #caa2ff
                );
                border-radius: 16px;
                border: 2px solid #b28aff;
                padding: 12px;
                font-size: 17px;
                font-weight: bold;
                color: #2d1c48;
                min-height: 42px;
            }
            QPushButton#runButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9d1ff,
                    stop:1 #d7b8ff
                );
            }

            /* CONTROL BUTTONS */
            QPushButton.controlBtn {
                background-color: #e8e4ef;
                border: 2px solid #cfc4e8;
                border-radius: 16px;
                padding: 10px;
                font-size: 15px;
                min-height: 38px;
                color: #42345c;
                font-weight: 600;
            }

            QPushButton.controlBtn:hover {
                background-color: #ded7eb;
            }

            QPushButton.controlBtn:disabled {
                background-color: #d5d0db;
                color: #8c8695;
                border-color: #c8c3ce;
            }

            /* Details box */
            QTextEdit {
                background: #ffffff;
                border-radius: 12px;
                border: 2px solid #d9ceff;
                padding: 8px;
                font-size: 14px;
                color: #2a2240;
            }
        """)


    # ---------------------------------------------------------
    # BFS Logic
    # ---------------------------------------------------------
    def _load_users(self):
        users = sorted(self.graph.get_all_users())
        self.combo_start.clear()
        self.combo_end.clear()
        self.combo_start.addItems(users)
        self.combo_end.addItems(users)

    def _update_button_states(self, disable_all=False):
        buttons = [self.btn_play, self.btn_pause, self.btn_step, self.btn_restart]

        for b in buttons:
            b.setEnabled(not disable_all)

        if disable_all:
            for b in buttons:
                b.setStyleSheet("""
                    background-color: #DDD;
                    color: #666;
                    border-radius: 14px;
                    font-size: 15px;
                """)

    def run_bfs(self):
        start = self.combo_start.currentText()
        end = self.combo_end.currentText()
        self.output.clear()

        if start == end:
            self.output.setText("⚠ Start and Target cannot be the same.")
            return

        result = bfs_shortest_path(self.graph, start, end, return_full_result=True)

        if not result.path:
            self.output.setText(f"⚠ No path found between {start} and {end}.")
            return

        self.output.append(f"Shortest Path:\n → {' → '.join(result.path)}\n")
        self.output.append("Visited Order:\n" + " → ".join(result.visited_order) + "\n")
        self.output.append("Distances:\n")
        for u, d in result.distances.items():
            self.output.append(f"• {u}: {d}")

        self.canvas.reset_colors()
        self.animator = BFSAnimator(self.canvas, result, self.graph)
        self._update_button_states(disable_all=False)

    # Animation Controls
    def play_anim(self):
        if self.animator: self.animator.play()

    def pause_anim(self):
        if self.animator: self.animator.pause()

    def step_anim(self):
        if self.animator: self.animator.step()

    def restart_anim(self):
        if self.animator:
            self.animator.restart()
            self.canvas.reset_colors()
