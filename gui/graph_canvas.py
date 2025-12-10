# gui/graph_canvas.py

from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
)
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPointF

# ---------------------------------------------------------
# Updated color palette (Lavender Theme)
# ---------------------------------------------------------
BACKGROUND_COLOR = QColor("#f3eaff")        # soft lavender
EDGE_COLOR = QColor("#bba4ff")              # light purple lines
LABEL_COLOR = QColor("#372f5c")             # deep purple text
NODE_BORDER = QColor("#8f7bff")             # medium-purple ring

# Base node
DEFAULT_NODE = QBrush(QColor("#ffffff"))

# BFS / DFS theme colors
VISITED_NODE = QBrush(QColor("#d8c9ff"))    # light lavender (visited)
FRONTIER_NODE = QBrush(QColor("#ffe8a3"))   # soft yellow (frontier)
PATH_NODE = QBrush(QColor("#b1f7dd"))       # mint green (shortest path)

NODE_RADIUS = 26
FONT_OFFSET_Y = -6


class VisualNode:
    def __init__(self, node_id, name, scene: QGraphicsScene, pos: QPointF):
        self.id = node_id
        self.name = name
        self.pos = pos

        # Circle item (node)
        ellipse = QGraphicsEllipseItem(
            -NODE_RADIUS, -NODE_RADIUS,
            NODE_RADIUS * 2, NODE_RADIUS * 2
        )

        # ✨ New gradient fill for nodes
        gradient = QLinearGradient(0, -NODE_RADIUS, 0, NODE_RADIUS)
        gradient.setColorAt(0, QColor("#ffffff"))
        gradient.setColorAt(1, QColor("#f1e8ff"))
        ellipse.setBrush(QBrush(gradient))

        ellipse.setPen(QPen(NODE_BORDER, 2))
        ellipse.setZValue(10)
        ellipse.setPos(pos)

        scene.addItem(ellipse)
        self.item = ellipse

        # Label
        self.label = scene.addText(name)
        self.label.setDefaultTextColor(LABEL_COLOR)
        self.label.setScale(1.15)
        self.label.setPos(pos.x() - NODE_RADIUS / 2, pos.y() + FONT_OFFSET_Y)
        self.label.setZValue(20)


class VisualEdge:
    def __init__(self, u: VisualNode, v: VisualNode, scene: QGraphicsScene):
        self.u = u
        self.v = v
        self.item = QGraphicsLineItem()
        self.item.setPen(QPen(EDGE_COLOR, 2))
        scene.addItem(self.item)
        self.update()

    def update(self):
        self.item.setLine(
            self.u.pos.x(), self.u.pos.y(),
            self.v.pos.x(), self.v.pos.y()
        )


class GraphCanvas(QGraphicsView):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        # ✨ Canvas theme
        self.setStyleSheet("""
            QGraphicsView {
                background-color: #f3eaff;
                border: 3px solid #d3c5ff;
                border-radius: 18px;
            }
        """)

        self.nodes = {}
        self.edges = []

        self._build_graph()

    # ---------------------------------------------------------
    # Build graph visually
    # ---------------------------------------------------------
    def _build_graph(self):
        users = sorted(self.graph.get_all_users())
        center_x, center_y = 400, 300
        radius = 220

        import math
        n = len(users)

        for i, name in enumerate(users):
            angle = (2 * math.pi * i) / max(1, n)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            uid = self.graph.get_user_id(name)
            node = VisualNode(uid, name, self.scene, QPointF(x, y))
            self.nodes[uid] = node

        # Create edges
        for uid in self.nodes:
            for vid in self.graph.get_neighbors(uid):
                if uid < vid:  # avoid duplicates
                    self.edges.append(
                        VisualEdge(self.nodes[uid], self.nodes[vid], self.scene)
                    )

    # ---------------------------------------------------------
    # Color helpers used by BFS / DFS
    # ---------------------------------------------------------
    def reset_colors(self):
        for node in self.nodes.values():

            gradient = QLinearGradient(0, -NODE_RADIUS, 0, NODE_RADIUS)
            gradient.setColorAt(0, QColor("#ffffff"))
            gradient.setColorAt(1, QColor("#f1e8ff"))
            node.item.setBrush(QBrush(gradient))

    def mark_visited(self, uid):
        self.nodes[uid].item.setBrush(VISITED_NODE)

    def mark_frontier(self, uid):
        self.nodes[uid].item.setBrush(FRONTIER_NODE)

    def mark_path(self, uid):
        self.nodes[uid].item.setBrush(PATH_NODE)
