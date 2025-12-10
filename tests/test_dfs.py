import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from social_graph.graph import Graph
from social_graph.dfs import dfs_traversal, DFSResult


# ------------------------------------------------------------------
# Basic DFS correctness
# ------------------------------------------------------------------
def test_dfs_simple_chain():
    g = Graph()
    g.add_friendship("A", "B")
    g.add_friendship("B", "C")

    result = dfs_traversal(g, "A")

    assert isinstance(result, DFSResult)
    assert result.order == ["A", "B", "C"]
    assert result.parent["A"] is None
    assert result.parent["B"] == "A"
    assert result.parent["C"] == "B"
    assert result.depth == {"A": 0, "B": 1, "C": 2}


# ------------------------------------------------------------------
# DFS with branching and sorted adjacency
# ------------------------------------------------------------------
def test_dfs_sorted_traversal():
    """
    DFS should visit neighbors in sorted lexicographic order.
    Graph:
        A connected to B, D, C
        expecting order: A → B → C → D
    """
    g = Graph()
    g.add_friendship("A", "C")
    g.add_friendship("A", "B")
    g.add_friendship("A", "D")

    result = dfs_traversal(g, "A")

    assert result.order == ["A", "B", "C", "D"]


# ------------------------------------------------------------------
# DFS on disconnected graph
# ------------------------------------------------------------------
def test_dfs_on_disconnected():
    g = Graph()
    g.add_user("A")
    g.add_user("B")   # isolated

    result = dfs_traversal(g, "A")

    assert result.order == ["A"]
    assert result.depth["A"] == 0
    assert "B" not in result.order


# ------------------------------------------------------------------
# DFS with self-start
# ------------------------------------------------------------------
def test_dfs_single_node():
    g = Graph()
    g.add_user("A")

    result = dfs_traversal(g, "A")

    assert result.order == ["A"]
    assert result.parent["A"] is None
    assert result.depth["A"] == 0


# ------------------------------------------------------------------
# Parent and depth correctness in branching tree
# ------------------------------------------------------------------
def test_dfs_parent_and_depth():
    """
    Graph:
         A
       /   \
      B     C
     / \
    D   E
    """
    g = Graph()
    g.add_friendship("A", "B")
    g.add_friendship("A", "C")
    g.add_friendship("B", "D")
    g.add_friendship("B", "E")

    result = dfs_traversal(g, "A")

    # order guaranteed because neighbors sorted: A → B → D → E → C
    assert result.order == ["A", "B", "D", "E", "C"]

    # parent checks
    assert result.parent["A"] is None
    assert result.parent["B"] == "A"
    assert result.parent["D"] == "B"
    assert result.parent["E"] == "B"
    assert result.parent["C"] == "A"

    # depth checks
    assert result.depth["A"] == 0
    assert result.depth["B"] == 1
    assert result.depth["D"] == 2
    assert result.depth["E"] == 2
    assert result.depth["C"] == 1


# ------------------------------------------------------------------
# Timestamp sanity check
# ------------------------------------------------------------------
def test_dfs_timestamp_rules():
    g = Graph()
    g.add_friendship("A", "B")
    g.add_friendship("A", "C")

    result = dfs_traversal(g, "A")

    tin = result.tin
    tout = result.tout

    # tin must be < tout for every node
    for node in result.order:
        assert tin[node] < tout[node]

    # first node visited must have smallest tin
    assert tin["A"] == min(tin.values())
