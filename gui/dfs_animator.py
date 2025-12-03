# gui/dfs_animator.py
from PyQt5.QtCore import QTimer


class DFSAnimator:
    """
    DFS Animation Controller

    Handles:
        - highlighting DFS visiting order
        - showing active (current) node
        - marking visited nodes
        - marking DFS tree edges by marking parent path
    """

    def __init__(self, canvas, dfs_result, graph):
        self.canvas = canvas
        self.graph = graph
        self.result = dfs_result

        # convert traversal order to node IDs
        self.order_ids = [graph.get_user_id(name) for name in dfs_result.order]

        # convert DFS tree (parents)
        self.parent_map = {
            graph.get_user_id(node): (
                None if parent is None else graph.get_user_id(parent)
            )
            for node, parent in dfs_result.parent.items()
        }

        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)

        # for path animation
        self.tree_index = 0
        self.tree_nodes = list(self.parent_map.keys())
        self.tree_timer = QTimer()
        self.tree_timer.timeout.connect(self._tree_step)

    # ---------------------------------------------------------
    # External controls
    # ---------------------------------------------------------
    def play(self):
        self.canvas.reset_colors()
        self.index = 0
        self.timer.start(400)

    def pause(self):
        self.timer.stop()

    def step(self):
        self._step()

    def restart(self):
        self.timer.stop()
        self.tree_timer.stop()
        self.canvas.reset_colors()

        self.index = 0
        self.tree_index = 0

    # ---------------------------------------------------------
    # DFS visiting order animation
    # ---------------------------------------------------------
    def _step(self):
        if self.index >= len(self.order_ids):
            self.timer.stop()
            self._start_tree_animation()
            return

        current_uid = self.order_ids[self.index]

        # Mark current node as frontier (yellow)
        self.canvas.mark_frontier(current_uid)

        # Previous becomes visited
        if self.index > 0:
            self.canvas.mark_visited(self.order_ids[self.index - 1])

        self.index += 1

    # ---------------------------------------------------------
    # DFS tree animation (parent relationships)
    # ---------------------------------------------------------
    def _start_tree_animation(self):
        self.tree_index = 0
        self.tree_timer.start(300)

    def _tree_step(self):
        if self.tree_index >= len(self.tree_nodes):
            self.tree_timer.stop()
            return

        node_id = self.tree_nodes[self.tree_index]

        # Mark DFS tree nodes as green (final DFS structure)
        self.canvas.mark_path(node_id)

        self.tree_index += 1
