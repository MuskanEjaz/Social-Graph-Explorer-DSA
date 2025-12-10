# gui/graph_view_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout,
    QTabWidget, QWidget, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFont

from gui.graph_canvas import GraphCanvas
from social_graph.graph import Graph


# ------------------------------------------------------------
# SMALL MINI-CANVAS FOR ADJACENCY LIST PREVIEW
# ------------------------------------------------------------
class MiniListCanvas(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.setMinimumHeight(240)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        users = sorted(self.graph.get_all_users())
        x = 20
        y = 30

        qp.setPen(QPen(QColor("#9678d3"), 2))
        qp.setFont(QFont("Arial", 12))

        for u in users:
            qp.drawText(x, y, f"{u} → {', '.join(self.graph.get_friends(u))}")
            y += 28


# ------------------------------------------------------------
# MINI HEATMAP FOR ADJACENCY MATRIX
# ------------------------------------------------------------
class MatrixHeatmap(QWidget):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix
        self.size = len(matrix)
        self.setMinimumHeight(240)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        n = self.size
        if n == 0:
            return

        cell = min(self.width() // n, self.height() // n, 28)

        for r in range(n):
            for c in range(n):
                val = self.matrix[r][c]
                color = QColor("#b8f5c4") if val == 1 else QColor("#eee8ff")
                qp.setBrush(QBrush(color))
                qp.setPen(QPen(QColor("#b7a2ff"), 1))

                qp.drawRect(c * cell + 10, r * cell + 10, cell, cell)


# ------------------------------------------------------------
# STATISTIC BADGE CARD
# ------------------------------------------------------------
class StatCard(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 14px;
                padding: 14px;
            }}
        """)

        layout = QVBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2d1c48;")

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("font-size: 20px; font-weight: bold; color: #000;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        self.setLayout(layout)


# ============================================================
# MAIN WINDOW
# ============================================================
class GraphViewWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("📊 Graph Viewer - Social Graph Explorer")
        self.resize(980, 600)

        self._build_ui()
        self._apply_theme()

    # ------------------------------------------------------------
    # BUILD UI
    # ------------------------------------------------------------
    def _build_ui(self):
        root = QVBoxLayout()
        root.setSpacing(10)
        root.setContentsMargins(15, 15, 15, 15)

        title = QLabel("📊 Graph Visualization & Structure")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        root.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._tab_adj_list(), "Adjacency List")
        tabs.addTab(self._tab_adj_matrix(), "Adjacency Matrix")
        tabs.addTab(self._tab_stats(), "Graph Statistics")

        root.addWidget(tabs)
        self.setLayout(root)

    # ------------------------------------------------------------
    # TAB 1 — Adjacency List
    # ------------------------------------------------------------
    def _tab_adj_list(self):
        w = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Adjacency List Representation")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        # Visual preview
        preview = MiniListCanvas(self.graph)
        preview.setStyleSheet("background:#ffffff; border-radius:12px; border:2px solid #dcd2ff;")
        layout.addWidget(preview)

        # Text output
        box = QTextEdit()
        box.setReadOnly(True)
        box.setMinimumHeight(220)
        box.setStyleSheet("font-size:14px;")
        box.setText(self.graph.print_adjacency_list())
        layout.addWidget(box)

        w.setLayout(layout)
        return w

    # ------------------------------------------------------------
    # TAB 2 — Adjacency Matrix
    # ------------------------------------------------------------
    def _tab_adj_matrix(self):
        w = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Adjacency Matrix Heatmap")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        matrix = self.graph.adjacency_matrix()

        heatmap = MatrixHeatmap(matrix)
        heatmap.setStyleSheet("background:#ffffff; border-radius:12px; border:2px solid #dcd2ff;")
        layout.addWidget(heatmap)

        # Text version
        box = QTextEdit()
        box.setReadOnly(True)
        box.setMinimumHeight(220)
        box.setText(self.graph.print_adjacency_matrix())
        layout.addWidget(box)

        w.setLayout(layout)
        return w

    # ------------------------------------------------------------
    # TAB 3 — Statistics
    # ------------------------------------------------------------
    def _tab_stats(self):
        w = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Graph Metrics & Summary")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        users = self.graph.get_all_users()
        matrix = self.graph.adjacency_matrix()

        node_count = len(users)
        edge_count = sum(sum(row) for row in matrix) // 2
        isolated = [u for u in users if len(self.graph.get_friends(u)) == 0]

        # ------------------------
        # Statistic Cards
        # ------------------------
        card_layout = QHBoxLayout()
        card_layout.addWidget(StatCard("Users (Nodes)", str(node_count), "#dec0ff"))
        card_layout.addWidget(StatCard("Friendships (Edges)", str(edge_count), "#b8e1ff"))
        card_layout.addWidget(StatCard("Isolated Users", str(len(isolated)), "#ffd580"))
        layout.addLayout(card_layout)

        # ------------------------
        # List details
        # ------------------------
        details = QTextEdit()
        details.setReadOnly(True)
        details.setMinimumHeight(260)

        stats = [
            f"Users: {', '.join(sorted(users))}",
            "",
            "Isolated Users:",
            ", ".join(isolated) if isolated else "None"
        ]
        details.setText("\n".join(stats))

        layout.addWidget(details)
        w.setLayout(layout)
        return w

    # ------------------------------------------------------------
    # THEME
    # ------------------------------------------------------------
    def _apply_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f3eaff;
            }
            QTabWidget::pane {
                border: 2px solid #d2c3ff;
                border-radius: 12px;
                padding: 6px;
                background:#ffffff;
            }
            QTabBar::tab {
                background: #e8e0ff;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
                margin-right: 4px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #d4c2ff;
                font-weight: bold;
            }
            QTextEdit {
                border-radius: 12px;
                background:#ffffff;
                border:2px solid #d9ceff;
                padding:8px;
                font-size:14px;
            }
        """)
