from PyQt5.QtCore import QTimer


class DFSAnimator:
    """
    DFS Animation Controller – Lavender Themed
    Now compatible with DFSPathResult.
    """

    def __init__(self, canvas, dfs_result, graph):
        self.canvas = canvas
        self.graph = graph
        self.result = dfs_result

        # Use visited_order instead of dfs_result.order
        self.order_ids = [graph.get_user_id(name) for name in dfs_result.visited_order]

        # DFSPathResult does NOT include parent information → disable tree animation
        self.parent_map = {}
        self.tree_nodes = []

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)

        # No tree animation needed anymore
        self.tree_timer = QTimer()

        # Counters
        self.index = 0
        self.tree_index = 0

    # ---------------------------------------------------------
    # Controls
    # ---------------------------------------------------------
    def play(self):
        self.stop_all()
        self.canvas.reset_colors()

        self.index = 0
        self.tree_index = 0

        self.timer.start(380)

    def pause(self):
        self.timer.stop()
        self.tree_timer.stop()

    def step(self):
        if self.index < len(self.order_ids):
            self._step()

    def restart(self):
        self.stop_all()
        self.canvas.reset_colors()
        self.index = 0
        self.tree_index = 0

    def stop_all(self):
        self.timer.stop()
        self.tree_timer.stop()

    # ---------------------------------------------------------
    # DFS VISITING ORDER ANIMATION
    # ---------------------------------------------------------
    def _step(self):
        if self.index >= len(self.order_ids):
            self.timer.stop()
            return

        uid = self.order_ids[self.index]

        # Highlight active node
        self.canvas.mark_frontier(uid)

        if self.index > 0:
            prev = self.order_ids[self.index - 1]
            self.canvas.mark_visited(prev)

        self.index += 1
