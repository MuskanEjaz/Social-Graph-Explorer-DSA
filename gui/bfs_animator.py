# gui/bfs_animator.py

from PyQt5.QtCore import QTimer


class BFSAnimator:
    """Handles BFS animation timing and state transitions."""

    def __init__(self, canvas, bfs_result, graph):
        self.canvas = canvas
        self.graph = graph
        self.result = bfs_result

        # Convert visited order & path to internal graph IDs
        self.visit_ids = [graph.get_user_id(name) for name in bfs_result.visited_order]
        self.path_ids = [graph.get_user_id(name) for name in bfs_result.path]

        # Timers for animation
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
        """Start full BFS animation."""
        self.stop_all()
        self.canvas.reset_colors()

        self.index = 0
        self.path_index = 0
        self.exploration_done = False

        # Slightly smoother speed for UI harmony
        self.timer.start(350)

    def pause(self):
        """Pause both animation phases."""
        self.timer.stop()
        self.path_timer.stop()

    def step(self):
        """Perform a single animation step."""
        if not self.exploration_done:
            self._step_exploration()
        else:
            self._step_path()

    def restart(self):
        """Reset everything and prepare for a new animation cycle."""
        self.stop_all()
        self.canvas.reset_colors()
        self.index = 0
        self.path_index = 0
        self.exploration_done = False

    def stop_all(self):
        """Stop all timers safely."""
        self.timer.stop()
        self.path_timer.stop()

    # -------------------------------------------------------------
    # EXPLORATION PHASE (Visited Order)
    # -------------------------------------------------------------
    def _step_exploration(self):
        """Animate BFS visiting order."""
        if self.index >= len(self.visit_ids):
            # Move to shortest path phase
            self.timer.stop()
            self.exploration_done = True
            self._start_path_animation()
            return

        uid = self.visit_ids[self.index]
        self.canvas.mark_frontier(uid)

        # Mark previous node as visited
        if self.index > 0:
            prev_uid = self.visit_ids[self.index - 1]
            self.canvas.mark_visited(prev_uid)

        self.index += 1

    # -------------------------------------------------------------
    # SHORTEST PATH PHASE (Final Path)
    # -------------------------------------------------------------
    def _start_path_animation(self):
        """Begin animating the shortest path."""
        if not self.path_ids:
            return

        self.path_index = 0
        self.path_timer.start(350)

    def _step_path(self):
        """Highlight nodes in the shortest path."""
        if self.path_index >= len(self.path_ids):
            self.path_timer.stop()
            return

        uid = self.path_ids[self.path_index]
        self.canvas.mark_path(uid)

        self.path_index += 1
