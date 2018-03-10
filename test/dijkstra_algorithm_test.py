"""
===================================
Demo of Shortest path algorithm
===================================

"""


import networkx as nx
import matplotlib.pyplot as plt

# dijkstra_sample_data.txt is csv file.
# edges.txt의 형식은 출발지,도착지,weight 로 정의하였습니다. 마지막 네번째 column은 도로명으로 정했는데 여기서는 사용하지 않았습니다.
FILE_NAME = "../asset/dijkstra_sample_data.txt"
GRAPH_TYPE = nx.Graph() # if you want to treat a directed graph -> use nx.Digraph()

# dijkstra_sample_data.txt 파일을 불러와 graph를 생성합니다
G = nx.read_edgelist(FILE_NAME, create_using=GRAPH_TYPE, delimiter=",", nodetype=str, data=[("weight", int), ("attr", str)])
G.edges(data=True)

# the shortest path from A(source) to I(target)
shortest_path = nx.dijkstra_path(G, 'A', 'I', 'weight')
shortest_path_length = nx.dijkstra_path_length(G, 'A', 'I', 'weight')

for i in shortest_path:
    if i == shortest_path[len(shortest_path)-1]:
        print(i)
    else :
        print(i + " -> ", end="")
print("total path length: " + str(shortest_path_length) + "km")

# Graph layout
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True)

# Display attribute on graph
edge_labels = dict(((C, E), d["weight"]) for C, E, d in G.edges(data=True))
# edge_labels = dict(((C, E), d["attr"]) for C, E, d in G.edges(data=True))
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8.0)

plt.show()
