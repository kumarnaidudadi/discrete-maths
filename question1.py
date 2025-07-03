import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt
import random
# Read Excel file
file = pd.read_excel('project2.xlsx')

# Extract the all elements in comulm 'email address'
em = pd.DataFrame(file, columns=['Email Address'])
#created a list emails which stores all emails
emails = em.values.tolist()
# created to new list nodes to append the entry nos for corresponding emails
nodes=[]
#for i in emails
for i in emails:
    #we need only first 11 letters and we need to make them capital so used .upper()
    nodes.append(i[0][:11].upper())
#now created a directed graph
G=nx.DiGraph()
#now we add nodes to the graph from the list nodes
G.add_nodes_from(nodes)
# now we need edge_list 
edge_list=[]
#for i in range 133 
for i in range(133):
    #row data gives us the elements from column 2 to 32 in row i  and this becomes edge list
    row_data=file.iloc[i,2:32].tolist()
    #new list k

    k=[]
    #if some person didnot fill all 30 then it will be nan so we dont need those 
    for i in row_data:
        #so if type == str then only we append the last 11 letters and make them capital using upper()
        if type(i)==str:
            k.append(i[-11:].upper())
            #else pass
        else:
            pass
    #edge_list append k
    edge_list.append(k)
#print(edge_list)    
for node in G.nodes():
    # Check if the node is not in list nodes
    if node not in nodes:
        # Add the node to list nodes
        nodes.append(node)
        # edge_list append [] because those have no outgoing edges or no row exist
        edge_list.append([])
#we are constructing graph
for i in range(len(nodes)):
    #for nrb in edge_list[i] we need to add edge between this and nodes[i]
    for neb in edge_list[i]:
        #add edge between nodes[i] and neb
        G.add_edge(nodes[i],neb)

#print(G.edges())
# drawing graph
#nx.draw(G,with_labels=True)
#plt.show()
#plt.show()


def pagerank_random_walk(graph, num_iterations):
    points = {node: 0 for node in graph.nodes()}

    # Start with a random node
    s = random.choice(list(graph.nodes()))

    for i in range(num_iterations):
        # Increment the points of the current node
        points[s] += 1

        # Choose a random edge from the current node
        neighbors = list(graph.neighbors(s))
        r=random.random()
        # for better results if r>0.15 then only we go through this loop 
        if r>=0.15:
            if neighbors:
                e = random.choice(neighbors)
            else:
                # If the current node has no neighbors, restart the walk from a random node
                s = random.choice(list(graph.nodes()))
                continue

            if e in nodes:
                s = e
            else:
                # If the chosen edge leads to a new node, add it to the graph
                points[e] = 0
                nodes.append(e)
                edge_list.append([])

                s = random.choice(list(graph.nodes()))
        else:
            s=random.choice(list(graph.nodes()))

    # Normalize PageRank values
    total_visits = sum(points.values())
    pagerank_values = {node: score / total_visits for node, score in points.items()}

    return pagerank_values


pagerank_values = pagerank_random_walk(G, 10000000 )

# Sort nodes based on PageRank scores
sorted_pagerank = sorted(pagerank_values.items(), key=lambda x: x[1], reverse=True)

# Print nodes arranged by PageRank score
print("Nodes arranged by PageRank score:")
for i, (node, rank) in enumerate(sorted_pagerank, start=1):
    print(f"Rank {i}: Node {node}, PageRank {rank}")

leader = sorted_pagerank[0][0]
print(f"\nThe leader is Node {leader} with the highest PageRank score.")
