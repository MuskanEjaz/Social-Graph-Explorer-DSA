# gui/bfs_animator.py

from PyQt5.QtCore import QTimer


class BFSAnimator:
    def __init__(self, canvas, bfs_result, graph):
        self.canvas = canvas
        self.graph = graph
        self.result = bfs_result

        # Convert names → numeric IDs
        self.visit_ids = [graph.get_user_id(n) for n in bfs_result.visited_order]
        self.path_ids = [graph.get_user_id(n) for n in bfs_result.path]

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_exploration)

        self.path_timer = QTimer()
        self.path_timer.timeout.connect(self._step_path)

        # Index counters
        self.index = 0
        self.path_index = 0

        # Flags
        self.exploration_done = False

    # -------------------------------------------------------------
    # PUBLIC CONTROLS
    # -------------------------------------------------------------
    def play(self):
        """Start BFS exploration animation."""
        self.stop_all()
        self.canvas.reset_colors()

        self.index = 0
        self.path_index = 0
        self.exploration_done = False

        self.timer.start(400)

    def pause(self):
        self.timer.stop()
        self.path_timer.stop()

    def step(self):
        """Perform one animation step manually."""
        if not self.exploration_done:
            self._step_exploration()
        else:
            self._step_path()

    def restart(self):
        self.stop_all()
        self.canvas.reset_colors()
        self.index = 0
        self.path_index = 0
        self.exploration_done = False

    def stop_all(self):
        """Force-stop everything before a new animation is started."""
        self.timer.stop()
        self.path_timer.stop()

    # -------------------------------------------------------------
    # BFS EXPLORATION PHASE
    # -------------------------------------------------------------
    def _step_exploration(self):
        """Animate BFS visitation order (frontier and visited)."""

        if self.index >= len(self.visit_ids):
            # Stop exploration → start path animation
            self.timer.stop()
            self.exploration_done = True
            self._start_path_animation()
            return

        uid = self.visit_ids[self.index]

        # Mark the current node as frontier
        self.canvas.mark_frontier(uid)

        # Mark previous as visited
        if self.index > 0:
            prev_uid = self.visit_ids[self.index - 1]
            self.canvas.mark_visited(prev_uid)

        self.index += 1

    # -------------------------------------------------------------
    # SHORTEST PATH PHASE
    # -------------------------------------------------------------
    def _start_path_animation(self):
        """Start animating the final shortest path."""
        if not self.path_ids:
            return  # No path exists

        # Reset path index
        self.path_index = 0

        # Start path highlighting
        self.path_timer.start(350)

    def _step_path(self):
        """Step through the final BFS path."""
        if self.path_index >= len(self.path_ids):
            self.path_timer.stop()
            return

        uid = self.path_ids[self.path_index]

        # Highlight path node
        self.canvas.mark_path(uid)

        self.path_index += 1
