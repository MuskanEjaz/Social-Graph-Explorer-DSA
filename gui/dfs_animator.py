from PyQt5.QtCore import QTimer
class DFSAnimator:
    def __init__(self, canvas, dfs_result, graph):
        self.canvas = canvas
        self.graph = graph
        self.result = dfs_result

        # Convert visited order to IDs
        self.order_ids = [graph.get_user_id(name) for name in dfs_result.visited_order]

        # Convert path to IDs (NEW!)
        self.path_ids = [graph.get_user_id(name) for name in dfs_result.path]

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_visit)

        self.path_timer = QTimer()
        self.path_timer.timeout.connect(self._step_path)

        # Counters
        self.index = 0
        self.path_index = 0

        self.exploration_done = False

    # ---------------------------------------------------------
    # Controls
    # ---------------------------------------------------------
    def play(self):
        self.stop_all()
        self.canvas.reset_colors()

        self.index = 0
        self.path_index = 0
        self.exploration_done = False

        self.timer.start(380)

    def pause(self):
        self.timer.stop()
        self.path_timer.stop()

    def step(self):
        if not self.exploration_done:
            self._step_visit()
        else:
            self._step_path()

    def restart(self):
        self.stop_all()
        self.canvas.reset_colors()
        self.index = 0
        self.path_index = 0
        self.exploration_done = False

    def stop_all(self):
        self.timer.stop()
        self.path_timer.stop()

    # ---------------------------------------------------------
    # DFS VISITING ORDER ANIMATION
    # ---------------------------------------------------------
    def _step_visit(self):
        if self.index >= len(self.order_ids):
            self.timer.stop()
            self.exploration_done = True
            self._start_path_animation()
            return

        uid = self.order_ids[self.index]

        self.canvas.mark_frontier(uid)

        if self.index > 0:
            prev = self.order_ids[self.index - 1]
            self.canvas.mark_visited(prev)

        self.index += 1

    # ---------------------------------------------------------
    # PATH ANIMATION
    # ---------------------------------------------------------
    def _start_path_animation(self):
        if not self.path_ids:
            return
        self.path_index = 0
        self.path_timer.start(380)

    def _step_path(self):
        if self.path_index >= len(self.path_ids):
            self.path_timer.stop()
            return

        uid = self.path_ids[self.path_index]
        self.canvas.mark_path(uid)

        self.path_index += 1
