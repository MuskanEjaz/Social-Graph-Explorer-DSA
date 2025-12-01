import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from social_graph.graph import Graph
from social_graph.dfs import DFS

def test_dfs():
    g = Graph()
    g.add_friendship("A", "B")
    g.add_friendship("A", "C")
    g.add_friendship("B", "D")

    dfs = DFS(g)
    result = dfs.run("A")
    print("DFS Traversal:", result)

if __name__ == "__main__":
    test_dfs()
