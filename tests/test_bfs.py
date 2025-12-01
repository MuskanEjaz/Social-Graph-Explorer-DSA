import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from social_graph.graph import Graph
from social_graph.bfs import bfs_shortest_path


def test_bfs_simple_path():
    g = Graph()
    g.add_user("A")
    g.add_user("B")
    g.add_user("C")

    g.add_friendship("A", "B")
    g.add_friendship("B", "C")

    path = bfs_shortest_path(g, "A", "C")
    assert path == ["A", "B", "C"]


def test_bfs_no_path():
    g = Graph()
    g.add_user("A")
    g.add_user("B")
    g.add_user("C")

    g.add_friendship("A", "B")
    # C is isolated

    path = bfs_shortest_path(g, "A", "C")
    assert path == []


def test_bfs_same_node():
    g = Graph()
    g.add_user("A")

    path = bfs_shortest_path(g, "A", "A")
    assert path == ["A"]
