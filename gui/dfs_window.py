# gui/dfs_window.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTextEdit,
    QWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from gui.graph_canvas import GraphCanvas
from gui.dfs_animator import DFSAnimator
from social_graph.dfs import dfs_shortest_path



class DFSWindow(QDialog):
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.animator = None

        self.setWindowTitle("DFS Visualizer - Social Graph Explorer")
        self.resize(1020, 600)
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

        # ---- LEFT PANEL ----
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(18)
        left_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(left_container)

        # Title
        title = QLabel("🔎 DFS Path Visualizer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # Start Users
        lbl_start = QLabel("Start User:")
        lbl_start.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_start)

        self.combo_start = QComboBox()
        self.combo_start.setMinimumHeight(36)
        left_layout.addWidget(self.combo_start)

        # End Users
        lbl_end = QLabel("Target User:")
        lbl_end.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_end)

        self.combo_end = QComboBox()
        self.combo_end.setMinimumHeight(36)
        left_layout.addWidget(self.combo_end)

        # Run button
        self.btn_run = QPushButton("Run DFS")
        self.btn_run.setObjectName("runButton")
        self._style_button(self.btn_run)
        left_layout.addWidget(self.btn_run)
        self.btn_run.clicked.connect(self.run_dfs)

        # Animation Controls
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

        # RIGHT PANEL — Graph Canvas
        # ======================================================
        self.canvas = GraphCanvas(self.graph)

        root.addWidget(scroll_area, 0)  # never expands too large
        root.addWidget(self.canvas, 1)   # canvas expands instead

        self.setLayout(root)
        self._apply_theme()

    # ---------------------------------------------------------
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
            QLabel {
                color: #3b2a66;
                font-size: 15px;
                font-weight: bold;
            }
            QLabel#Title {
                font-size: 22px;
                font-weight: 900;
            }
            QComboBox {
                background: #ffffff;
                border-radius: 10px;
                border: 2px solid #d2c3ff;
                padding: 6px 10px;
                font-size: 15px;
            }
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
            }
            QPushButton.controlBtn {
                background-color: #e8e4ef;
                border: 2px solid #cfc4e8;
                border-radius: 16px;
                padding: 10px;
                font-size: 15px;
                color: #42345c;
                font-weight: 600;
            }
        """)

    # ---------------------------------------------------------
    # LOAD USERS
    # ---------------------------------------------------------
    def _load_users(self):
        users = sorted(self.graph.get_all_users())
        self.combo_start.addItems(users)
        self.combo_end.addItems(users)

    # ---------------------------------------------------------
    def _update_button_states(self, disable_all=False):
        for b in (self.btn_play, self.btn_pause, self.btn_step, self.btn_restart):
            b.setEnabled(not disable_all)

    # ---------------------------------------------------------
    # DFS LOGIC
    # ---------------------------------------------------------
    def run_dfs(self):
        start = self.combo_start.currentText()
        end = self.combo_end.currentText()
        self.output.clear()

        if start == end:
            self.output.setText("⚠ Start and Target cannot be the same.")
            return

        # result = dfs_traversal(self.graph, start, end, return_full_result=True)
        result = dfs_shortest_path(self.graph, start, end, return_full_result=True)



        if not result.path:
            self.output.setText(f"⚠ No path found between {start} and {end}.")
            return

        #self.output.append(f"Path:\n → {' → '.join(result.path)}\n")
        #self.output.append("Visited:\n" + " → ".join(result.visited_order) + "\n")

        self.output.append(f"Path:\n → {' → '.join(result.path)}\n")
        self.output.append("Visited:\n" + " → ".join(result.visited_order) + "\n")


        self.canvas.reset_colors()
        self.animator = DFSAnimator(self.canvas, result, self.graph)
        self._update_button_states(disable_all=False)

    # ---------------------------------------------------------
    # Animation Controls
    # ---------------------------------------------------------
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


