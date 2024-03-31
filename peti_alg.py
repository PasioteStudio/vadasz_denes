#Additional informations:
    #If you still don't understand the phrases, pls go watch this video on YT: GiDsjIBOVoA&t
    #The file currently used is "gyongyok.txt" or "gyongyok_short.txt" 
    #More about the Hungarian (Kunh Munkres) algorithm here: en.wikipedia.org/wiki/Hungarian_algorithm

#All imports go here:
from py3d import Vector3 as V3
import networkx as nx
import matplotlib.pyplot as plt
import munkres as HU
#The class representing points
class ˇPoints():
    def __init__(self, position, value):
        self.position = position #The position is saved in a V3
        self.value = value #The value is only one int


#Converts all of the elements of 'li' into ints
def list_to_int(li):
    try:
        return [int(x) for x in li]
    except:
        return None


#Opens the file corresponding to 'filename' based on the standard syntax
def data_input(filename):
    f = open(filename)
    f.readline()
    data = {}
    #Kezdőpont
    data[0] = ˇPoints(V3(0,0,0),1)
    for c, i in enumerate(f.readlines()):
        #Where c is the curet line, and i is it's content
        i = list_to_int(str(i).strip().split(";")[0:4])
        data[c+1] = ˇPoints(V3(i[0],i[1],i[2]),i[3])
    return data #This outputs a dictionary, names are the corresponding lines, the words are 'ˇPoints' classes. Let's call this format D-format from here.


#This is an algorithm finds the mst (Minimum Spanning Tree) for any given 'graph' D-format
#This returns a graph by an edge matrix in this extendable format: [[A,B],[B,C],[C,A]]. Let's call this E-format. [note: it only works with non-multigraphs]
def finding_mst(graph):
    final_mst = []
    #This loop goes 'till all the elements of 'graph' are popped and all the nodes are sorted *
    while len(graph)>0:
        graph = dict(graph)
        #Popping and saving the first element of the graph
        curet = graph[list(graph)[0]]
        curet_index = list(graph)[0]
        graph.pop(list(graph)[0])
        # *
        if (len(graph)<=0): break
        #Getting a default value to the correct pair for 'curet'
        smallest = [list(graph)[0], V3.distance_to_points(graph[list(graph)[0]].position , curet.position)]
        #Testing all the nodes, and finding the smallest weight for pairing
        for i in range(len(graph)):
            if V3.distance_to_points(graph[list(graph)[i]].position , curet.position) >= smallest[1]:
                smallest[0] = list(graph)[i]
                smallest[1] = V3.distance_to_points(graph[list(graph)[i]].position , curet.position)
        #Saving the pair, in a standard format
        if curet_index>smallest[0]: final_mst.append([curet_index,smallest[0]])
        else: final_mst.append([smallest[0],curet_index])
    #Returning the E-format mst
    return final_mst

#This function takes an E-format 'graph' and gives back every node with an odd degree in a simple array
def select_odd(graph):
    counted = {}
    result = []
    #Collects the number of mention for every node
    for i in graph:
        try: counted[i[0]] += 1
        except: counted[i[0]] = 1
        try: counted[i[1]] += 1
        except: counted[i[1]] = 1
    #Selects the odd mention numbers
    for i in counted:
        if counted[i]%2!=0: result.append(i)
    #Returns a simple array
    return sorted(result) 

#This method takes an E-format 'graph' and displays it using network and matplotlib.pyplot library
def show_graph(graph): 
    #Makes the graph
    G = nx.MultiGraph()
    #Adds all the edges
    for i in graph:
        G.add_edge(i[0],i[1])
    #Draws and shows the graph
    nx.draw_spectral(G, with_labels=True)
    plt.show()

#This function takes in a list of nodes, and creates an MWPM (Minimum Weight Perfect Matching) and outputs it in E-format
def finding_MWPM(data,nodes):
    nodes=select_odd(nodes)
    #Constructing matrix for the Hungarian (Kunh Munkres) algorithm to work with
    result = []
    for i in nodes:
        row = []
        for k in nodes:
            if k==i:
                row.append(HU.DISALLOWED)
            else:
                row.append(V3.distance_to_points(data[i].position , data[k].position))
        result.append(row)
    #Calculating MWPM with Hungarian (Kunh Munkres) algorithm
    m = HU.Munkres()
    mwpm = []
    #Correcting brackets
    for assignment in m.compute(result):
        mwpm.append([assignment[0], assignment[1]])
    #Returning in E-format
    return mwpm

#This function takes an E-format and converts it to an eulerian tour, which is a list of nodes
def find_eulerian_tour(edges):
    graph = {}
    for edge in edges:
        u, v = edge
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    def dfs(node):
        while graph[node]:
            neighbor = graph[node].pop()
            graph[neighbor].remove(node)
            dfs(neighbor)
        tour.append(node)

    start_node = edges[0][0]
    tour = []
    dfs(start_node)
    return tour[::-1]

#This function takes a list of nodes, possibly an eulerian tour, and converts it to a TSP (Traveling Salesman Problem) solution
def find_TSP(nodes):
    been_to = []
    tsp = []
    #Removes duplicating connections
    for i in nodes:
        if not i in been_to:
            been_to.append(i)
    #Makes E-format from the TSP array
    for i in range(len(been_to)):
        try:
            tsp.append([been_to[i],been_to[i+1]])
        except:
            #If it gets to the end of the list, it closes back
            tsp.append([been_to[i],been_to[0]])
    return tsp

def get_weight_of_tour(data, tour):
    weight=0
    for i in tour:
        weight += V3.distance_to_points(data[i[0]].position , data[i[1]].position)
    return weight

def get_efficiency_of_tsp(data,mst,tps):
    print(f"""The length of the mst is {get_weight_of_tour(data,mst)}
and the length of the tsp is {get_weight_of_tour(data,tps)}
the proportion of those is {get_weight_of_tour(data,tps)/get_weight_of_tour(data,mst)}""")

def run():
    #Run the program here:
    data = data_input("gyongyok.txt") #Raw D-format, contains all the points, their ID, value, and position in V3
    mst = finding_mst(data) #Minimum Spanning Tree
    ug = mst+finding_MWPM(data,mst) #Uniform Graph, the sum of an mst and an eulerian tour
    tsp = find_TSP(find_eulerian_tour(ug)) #TSP Traveling Salesman Problem solution
    print(tsp)
    get_efficiency_of_tsp(data,mst,tsp)
    return tsp