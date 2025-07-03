import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
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
#print(len(c))


for i in range(len(b)):
    for neb in c[i]:
        G.add_edge(b[i],neb)
'''
for i in G.nodes():
    if i  not in b:
        b.append(i)
        c.append([])
print(len(b))
print(len(c))'''
d=[]
for i in range(len(c)):
    for j in range(len(c[i])):
        d.append(c[i][j])
print(d)
#print(len(d))


points=[]
e=[]
for i in range(len(b)):
    score=0
    for j  in range(len(d)):
        if b[i]==d[j]:
            score=score+1
    points.append([b[i],score])

    
sorted_points = sorted(points, key=lambda tup: tup[1])

print(sorted_points)
print(len(sorted_points))
p=0.05
final=[]
persons=[]
maximum=sorted_points[-1][1]
for i in range(1,21):
    f=[]
    pe=[]
    for j in sorted_points:
        if (p * (i - 1) * maximum) < j[1] <= (i * p * maximum):
            f.append(j[1])
            pe.append(j[0])

    final.append(f)
    persons.append(pe)


print(final)

freq=[]
for i in final:
    freq.append(len(i))
print(freq)
x=range(20)
plt.bar(x,freq)
plt.xlabel('percentages ')
plt.ylabel('number of people lying in this percent')
plt.title('Bell Graph for given data')
plt.show()
print(persons[10])
