# Social Graph Explorer

This project is a Python-based Social Graph Explorer built using data structures and algorithms such as Graphs, BFS, DFS, and Disjoint Set Union (DSU). It allows users to add people, create friendships, visualize graph structures, detect communities, perform traversals, and receive friend recommendations. The application includes a colorful graphical interface made with PyQt5, where each feature is displayed in its own window. The backend algorithms are fully tested using pytest to ensure correctness. This project was developed as part of our DSA course to demonstrate practical implementation of graph algorithms and interactive UI design.

The Structure for the project is as follows
SocialGraphExplorer/
│
├── social_graph/
│   ├── graph.py
│   ├── recommendation.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── dsu.py
│   └── __init__.py
│
├── gui/
│   ├── MainWindow.py            
│   ├── bfs_animator.py
│   ├── recommendation_window.py
│   ├── dfs_animator.py
│   ├── graph_view_window.py
│   ├── graph_canvas.py
│   ├── add_user_dialog.py
│   ├── delete_friend_dialog.py
│   ├── add_friend_dialog.py
│   ├── community_window.py
│   ├── bfs_window.py  
│   └── dfs_window.py
│
├── main.py                      ← main launcher file (outside gui)
├── tests/                       ← for testing 
├── graph_data.json              ← for saving the data entered
└── README.md