import os
import itertools

import utils.main_util as main_util
from utils.graph import Graph
import math
from functools import reduce
def getLength(x1,y1,z1,e1,x2,y2,z2,e2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)/e1/e2
def getLengthProper(x1,y1,z1,x2,y2,z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
def getRealPathValues(path:list[dict]):
    print(path)
    legth=[]
    for id,point in enumerate(path):
        print(point)
        if id != len(path)-1:
            legth.append(getLengthProper(point["x"],point["y"],point["z"],path[id+1]["x"],path[id+1]["y"],path[id+1]["z"]))
        else:
            pass
    return legth
        
def initInput():
    f=open("gyongyok.txt","r+",encoding="utf8")
    lines=f.readlines()
    f.close()
    for id,line in enumerate(lines):
        if id == 0:
            continue
        parts=line.strip().split(";")
        temporary_points.append({"x":int(parts[0]),
                                 "y":int(parts[1]),
                                 "z":int(parts[2]),
                                 "e":int(parts[3])})
    complete_lines=[]
    number_of_completed_lines=reduce(lambda x, y:x+y, range(len(temporary_points)))
    print(number_of_completed_lines)
    for id,point in enumerate(temporary_points):
        for i in range(len(temporary_points)-id-1):
            path=getLength(point["x"],point["y"],point["z"],point["e"],temporary_points[id+i+1]["x"],temporary_points[id+i+1]["y"],temporary_points[id+i+1]["z"],temporary_points[id+i+1]["e"])
            path=float(path)
            print(f"{point},{temporary_points[id+i+1]},{path}")
            complete_lines.append(f"{id+1},{id+i+2},{path}")
    return complete_lines
if __name__ == '__main__':
    #x;y;z;e to vertext to vertex format
    temporary_points=[]
    complete_lines=initInput()
    debug_folder = r"output/"
    source_node = "1"
    debug = True

    if not os.path.exists(debug_folder):
        os.makedirs(debug_folder)
    else:
        #print("Output Directory already exists")
        #exit(1)
        pass

    # create graph from input txt file
    initial_g = main_util.create_graph_from_list(complete_lines)
    if debug:
        print("Initial Graph:")
        main_util.print_edges_with_weight(initial_g)
        initial_g.plot_graph(os.path.join(debug_folder, "graph.png"))

    # TODO : Validation of the graph: triangle inequality property

    # create a MST
    mst_graph = main_util.get_mst(initial_g)
    if debug:
        print("\nMST:")
        main_util.print_edges_with_weight(mst_graph)
        mst_graph.plot_graph(os.path.join(debug_folder, "mst.png"))

    mst_degrees = main_util.get_degrees(mst_graph)
    if debug:
        print(f"\nMST degree : {mst_degrees}")

    odd_degrees = main_util.get_nodes_odd_degrees(mst_degrees)
    if debug:
        print(f"\nMST odd degree : {odd_degrees}")

    subgraph = main_util.create_subgraph(initial_g, odd_degrees)
    if debug:
        print("\nSubgraph:")
        main_util.print_edges_with_weight(subgraph)
        subgraph.plot_graph(os.path.join(debug_folder, "subgraph.png"))

    minimum_perfect_match = main_util.create_minimum_weight_perfect_matching(subgraph)
    if debug:
        print("\nMinimum weight perfect match:")
        main_util.print_edges_with_weight(minimum_perfect_match)
        minimum_perfect_match.plot_graph(os.path.join(debug_folder, "minimum_perfect_match.png"))

    union_graph = main_util.union_graphs(mst_graph, minimum_perfect_match)
    if debug:
        print("\nUnion graph details:")
        main_util.print_edges_with_weight(union_graph)
        union_graph.plot_graph(os.path.join(debug_folder, "union_graph.png"))

    euler_tour_itr = union_graph.get_euler_tour(source_node)
    euler_tour = []
    for e in euler_tour_itr:
        print("a"+str(e))
        euler_tour.append(e)

    if debug:
        print(f"\n Euler tour: {euler_tour}")
        euler_g = Graph()
        for e in euler_tour:
            euler_g.add_edge(e[0], e[1], initial_g.get_edge_weight(e[0], e[1]))
        euler_g.plot_graph(os.path.join(debug_folder, "euler_tour.png"))

    euler_tour = list(itertools.chain.from_iterable(list(euler_tour)))
    euler_tour = list(dict.fromkeys(euler_tour).keys())
    euler_tour.append(source_node)

    print(f"\nPath: {euler_tour}")
    if debug:
        final_path = Graph(di_graph=True)
        for i in range(len(euler_tour)-1):
            final_path.add_edge(euler_tour[i],
                                euler_tour[i+1],
                                initial_g.get_edge_weight(euler_tour[i], euler_tour[i+1]))
        final_path.plot_graph(os.path.join(debug_folder, "output.png"))
    all_path,total_weight = main_util.get_total_cost(initial_g, euler_tour)
    peti=['5','4','3','2','1','5']
    alternative_path,alternative=main_util.get_total_cost(initial_g,peti)
    print(alternative)
    print(f"Total traveling cost : {total_weight}")
    
    all_points1=[]
    for point in euler_tour:
        point=int(point)
        all_points1.append({"x":temporary_points[point-1]["x"],
                                "y":temporary_points[point-1]["y"],
                                "z":temporary_points[point-1]["z"],
                                "e":temporary_points[point-1]["e"]})
    all_points2=[]
    for point in peti:
        point=int(point)
        all_points2.append({"x":temporary_points[point-1]["x"],
                                "y":temporary_points[point-1]["y"],
                                "z":temporary_points[point-1]["z"],
                                "e":temporary_points[point-1]["e"]})
    a1=getRealPathValues(all_points1)
    a2=getRealPathValues(all_points2)
    t1=[]
    t2=[]
    if True:
        velocity=float(input("Sebesség(float)(e/s):"))
        for path in a1:
            time=path/velocity
            t1.append(time)
        for path in a2:
            time=path/velocity
            t2.append(time)
    print(f"Debug: path:{euler_tour},cost:{a1};{reduce(lambda x, y:x+y, a1)},{list(map(lambda x: x["e"],all_points1))},time:{t1};{reduce(lambda x, y:x+y, t1)}")
    #print(f"with value{all_path};{total_weight},")
    print(f"PetiDebug: path:{peti},cost:{a2};{reduce(lambda x, y:x+y, a2)},{list(map(lambda x: x["e"],all_points2))},time:{t2};{reduce(lambda x, y:x+y, t2)}")
    #print(f"with value{alternative_path};{alternative},")
    