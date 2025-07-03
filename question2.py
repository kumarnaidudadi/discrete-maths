import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
# Read Excel file
file = pd.read_excel('project2.xlsx')

# Extract Email Addresses
em = pd.DataFrame(file, columns=['Email Address'])
emails = em.values.tolist()
b=[]
for i in emails:
    b.append(i[0][:11].upper())
G=nx.DiGraph()
G.add_nodes_from(b)

c=[]
for i in range(133):
    row_data=file.iloc[i,2:32].tolist()
    k=[]
    for i in row_data:
        if type(i)==str:
            k.append(i[-11:].upper())
        else:
            pass
    c.append(k)
#print(c)

for i in range(len(b)):
    for neb in c[i]:
        G.add_edge(b[i],neb)
f=[]    
for node in G.nodes():
    # Check if the node is not in list b
    if node not in b:
        # Add the node to list b
        b.append(node)
        f.append(node)

nodes=list(G.nodes())
n = len(nodes)

#To find the missing links we use Ax = B matrix method
def remove_row_col(matrix, row_index, col_index):#finding the matrix after removing respective column and row
    new_matrix = np.delete(matrix, col_index, axis=1)
    final_matrix = np.delete(new_matrix, row_index, axis=0)
    transpose = final_matrix.T
    return final_matrix

def row(matrix, row_index, col_index):#finding the matrix B
    new_matrix = np.delete(matrix, col_index, axis=1)
    row= new_matrix[row_index]
    return row

def find_X(A, B):#find X with respect to A and B

    X, residuals, rank, s = np.linalg.lstsq(A, B, rcond=None)
    return X

def finding_link(matrix, X, i, j):# we make misiing link =value if value.size>0.
    new_matrix = np.delete(matrix, i, axis=0)
    col = new_matrix[:, j]
    value = np.dot(X, col)
    missing_link = value if value.size > 0 else 0
    return missing_link
#we finally print newly connected nodes and number of newly connected nodes
newly_connected_nodes=[]
newly_notconnected=[]
matrix= nx.to_numpy_array(G)
result=matrix

for i in range(n):
    for j in range(n):
        if matrix[i][j]==0:
            A = remove_row_col(matrix,i,j)
            B = row(matrix,i,j)
            X = find_X(A,B)
            
            link = finding_link(matrix,X,i,j)
            if link >= 1:
                result[i][j] = 1#resultant matrix
                newly_connected_nodes.append((i,j))#missing link with index i,j
            else:
                newly_notconnected.append((i,j))

print(newly_connected_nodes)
print("Number of missing edges or edgs  that would have actually connected = " , len(newly_connected_nodes))
print('Number of edges that would have not connected =',len(newly_notconnected))
print("The above list contains all the missing links corresponding to the i,j th index in the original adjacency_matrix")
