# gui/recommendation_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QHBoxLayout, QWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from gui.graph_canvas import GraphCanvas
from social_graph.bfs import bfs_shortest_path


class RecommendationWindow(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("⭐ Friend Recommendations")
        self.resize(980, 540)          # smaller overall window
        self.setMinimumSize(850, 500)

        self._build_ui()
        self._apply_theme()

    # -----------------------------------------------------------
    # UI SETUP
    # -----------------------------------------------------------
    def _build_ui(self):
        root = QHBoxLayout()
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(15)

        # -------------------------------------------------------
        # LEFT PANEL SCROLL AREA
        # -------------------------------------------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_area.setFixedWidth(280)     # <<< NARROWER LEFT PANEL

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(12)
        left_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(left_container)

        # TITLE — smaller font
        title = QLabel("⭐ Friend Recommendations")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # User selector
        lbl_user = QLabel("Select User:")
        lbl_user.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_user)

        self.combo_user = QComboBox()
        self.combo_user.setMinimumHeight(30)
        self.combo_user.setStyleSheet("font-size: 13px;")
        self.combo_user.addItems(sorted(self.graph.get_all_users()))
        left_layout.addWidget(self.combo_user)

        # Generate Button
        self.btn_run = QPushButton("Generate")
        self.btn_run.setObjectName("runButton")
        self._style_button(self.btn_run)
        self.btn_run.clicked.connect(self.run_recommendations)
        left_layout.addWidget(self.btn_run)

        # Output section
        lbl_results = QLabel("Results:")
        lbl_results.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_results)

        self.output = QTextEdit()
        self.output.setMinimumHeight(160)
        self.output.setReadOnly(True)
        self.output.setStyleSheet("font-size: 13px;")
        left_layout.addWidget(self.output)

        left_layout.addStretch()

        # -------------------------------------------------------
        # RIGHT CANVAS
        # -------------------------------------------------------
        self.canvas = GraphCanvas(self.graph)
        self.canvas.setMaximumHeight(480)  # slightly shorter right panel

        root.addWidget(scroll_area, 0)
        root.addWidget(self.canvas, 1)

        self.setLayout(root)

    # -----------------------------------------------------------
    # BUTTON STYLE
    # -----------------------------------------------------------
    def _style_button(self, btn):
        btn.setMinimumHeight(38)            # smaller button height
        btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(1)
        shadow.setYOffset(2)
        btn.setGraphicsEffect(shadow)

    # -----------------------------------------------------------
    # THEME
    # -----------------------------------------------------------
    def _apply_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f3eaff;
            }

            QLabel#Title {
                font-size: 18px;            /* smaller title text */
                font-weight: bold;
                color: #3b2a66;
                margin-bottom: 6px;
            }

            QLabel {
                color: #3b2a66;
                font-size: 13px;             /* smaller labels */
                font-weight: bold;
            }

            QComboBox {
                background: #ffffff;
                border: 2px solid #d2c3ff;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 13px;
            }

            QPushButton#runButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dec0ff,
                    stop:1 #caa2ff
                );
                border-radius: 14px;
                border: 2px solid #b28aff;
                padding: 8px;
                font-size: 14px;            /* smaller button font */
                font-weight: bold;
                color: #2d1c48;
            }

            QTextEdit {
                background: #ffffff;
                border-radius: 10px;
                border: 2px solid #d9ceff;
                padding: 6px;
                font-size: 13px;            /* smaller text */
                color: #2a2240;
            }
        """)

    # ======================================================================
    # FRIEND RECOMMENDATION LOGIC
    # ======================================================================
    def run_recommendations(self):
        username = self.combo_user.currentText()
        if not username:
            self.output.setText("Please select a user.")
            return

        recommendations = self.get_recommendations(username)

        self.output.clear()
        self.output.append(f"Recommendations for {username}:\n")

        if not recommendations:
            self.output.append("No recommendations found.")
            return

        for idx, (user, score, mutual_count, distance) in enumerate(recommendations, 1):
            self.output.append(
                f"{idx}. {user} | Score={score:.3f} "
                f"(Mutual={mutual_count}, Dist={distance})"
            )

        self.highlight_recommendations([rec[0] for rec in recommendations])

    # Ranking system (unchanged)
    def get_recommendations(self, user):
        all_users = set(self.graph.get_all_users())
        friends = set(self.graph.get_friends(user))
        candidates = all_users - friends - {user}

        recommendations = []

        for other in candidates:
            mutual_count = len(friends.intersection(self.graph.get_friends(other)))
            bfs_res = bfs_shortest_path(self.graph, user, other, return_full_result=True)
            distance = bfs_res.distances.get(other, None)
            distance_score = 0 if distance is None else 1 / (1 + distance)

            final_score = (mutual_count * 0.7) + (distance_score * 0.3)
            recommendations.append((other, final_score, mutual_count, distance))

        recommendations.sort(key=lambda x: -x[1])
        return recommendations

    # Highlight recommended users
    def highlight_recommendations(self, recommended_users):
        self.canvas.reset_colors()
        rec_color = QColor("#b8f5c4")
        for u in recommended_users:
            uid = self.graph.get_user_id(u)
            self.canvas.nodes[uid].item.setBrush(rec_color)
