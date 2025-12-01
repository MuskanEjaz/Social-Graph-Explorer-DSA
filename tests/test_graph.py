import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from social_graph.graph import Graph

def test():
    g = Graph()
    g.add_user("A")
    g.add_user("B")
    g.add_friendship("A", "B")
    print(g.print_adjacency_list())

if __name__ == "__main__":
    test()
