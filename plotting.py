import networkx as nx
#from pyvis.network import Network   
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1,2),(2,3),(3,4),(4,1)])
print(G.number_of_nodes())
print(G.number_of_edges())
#print("hallo?")


pos = nx.circular_layout(G)

print("-------------------")
print(pos)