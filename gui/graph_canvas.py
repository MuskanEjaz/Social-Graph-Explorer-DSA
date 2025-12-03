# gui/graph_canvas.py
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF

NODE_RADIUS = 26
FONT_OFFSET_Y = -6

EDGE_COLOR = QColor("#c7b7ff")

BACKGROUND_COLOR = QColor("#f6f2ff")

DEFAULT_NODE = QBrush(QColor("#ffffff"))
VISITED_NODE = QBrush(QColor("#a8d0ff"))
FRONTIER_NODE = QBrush(QColor("#ffd580"))
PATH_NODE = QBrush(QColor("#b8f5c4"))

class VisualNode:
    def __init__(self, node_id, name, scene: QGraphicsScene, pos: QPointF):
        self.id = node_id
        self.name = name

        # static position
        self.pos = pos

        # circle
        self.item = QGraphicsEllipseItem(-NODE_RADIUS, -NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2)
        self.item.setBrush(DEFAULT_NODE)
        self.item.setPen(QPen(QColor("#8a76ff"), 2))
        self.item.setZValue(10)
        self.item.setPos(pos)
        scene.addItem(self.item)

        # label
        self.label = scene.addText(name)
        self.label.setDefaultTextColor(QColor("#393555"))
        self.label.setScale(1.1)
        self.label.setPos(pos.x() - NODE_RADIUS/2, pos.y() + FONT_OFFSET_Y)
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
        self.item.setLine(self.u.pos.x(), self.u.pos.y(), self.v.pos.x(), self.v.pos.y())

class GraphCanvas(QGraphicsView):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.setStyleSheet("""
            background: #faf7ff;
            border: 3px solid #d8cbff;
            border-radius: 16px;
        """)

        self.nodes = {}
        self.edges = []

        self._build_graph()

    # ---------------------------------------------------------
    # Build graph visuals (STATIC POSITIONS)
    # ---------------------------------------------------------
    def _build_graph(self):
        users = sorted(self.graph.get_all_users())

        # static layout (circle pattern)
        center_x, center_y = 400, 300
        radius = 200

        import math
        n = len(users)
        for index, name in enumerate(users):
            angle = (2 * math.pi * index) / max(1, n)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            uid = self.graph.get_user_id(name)
            node = VisualNode(uid, name, self.scene, QPointF(x, y))
            self.nodes[uid] = node

        # Create edges
        for uid in self.nodes:
            for vid in self.graph.get_neighbors(uid):
                if uid < vid:
                    self.edges.append(VisualEdge(self.nodes[uid], self.nodes[vid], self.scene))

    # ---------------------------------------------------------
    # Coloring helpers for BFS / DFS animations
    # ---------------------------------------------------------
    def reset_colors(self):
        for n in self.nodes.values():
            n.item.setBrush(DEFAULT_NODE)

    def mark_visited(self, uid):
        self.nodes[uid].item.setBrush(VISITED_NODE)

    def mark_frontier(self, uid):
        self.nodes[uid].item.setBrush(FRONTIER_NODE)

    def mark_path(self, uid):
        self.nodes[uid].item.setBrush(PATH_NODE)
