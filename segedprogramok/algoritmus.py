import os
import itertools
import segedprogramok.main_util as main_util
from segedprogramok.graph import Graph
import math
from functools import reduce


def getHosszErtekkel(x1,y1,z1,e1,x2,y2,z2,e2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)/e1/e2

def getHossz(x1,y1,z1,x2,y2,z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def maximalizal(filename,max):
    f = open(filename,"r+",encoding="utf8")
    f.readline()
    lines = f.readlines()
    f.close()
    max.append(None)
    x = [int(i.strip().split(';')[0]) for i in lines]
    y = [int(i.strip().split(';')[1]) for i in lines]
    z = [int(i.strip().split(';')[2]) for i in lines]
    v = [int(i.strip().split(';')[3]) for i in lines]
    eredmeny  = []
    for index,i in enumerate([x,y,z]):
        eredmeny .append([max[index] if n > max[index] else n for n in i])
    res = [[eredmeny [0][i],eredmeny [1][i],eredmeny [2][i],v[i],] for i in range(len(lines))]
    return res


def getUtHossza(ut:list[dict]):
    hossz=[]
    for id,pont in enumerate(ut):
        if id != len(ut)-1:
            hossz.append(getHossz(pont["x"],pont["y"],pont["z"],ut[id+1]["x"],ut[id+1]["y"],ut[id+1]["z"]))
        else:
            pass
    return hossz


def initBeolvasas(gyongyokFajlNeve,ideiglenes_pontok,x,y,z):
    ideiglenes_pontok.append({"x":0,"y":0,"z":0,"e":1})#Kezdőpont
    for id,vonal in enumerate(maximalizal(gyongyokFajlNeve,[x,y,z])):
        if id == 0:
            continue
        ideiglenes_pontok.append({"x":int(vonal[0]),
                                 "y":int(vonal[1]),
                                 "z":int(vonal[2]),
                                 "e":int(vonal[3])})
    befejezettVonalak=[]
    for id,point in enumerate(ideiglenes_pontok):
        for i in range(len(ideiglenes_pontok)-id-1):
            ut=getHosszErtekkel(point["x"],point["y"],point["z"],point["e"],ideiglenes_pontok[id+i+1]["x"],ideiglenes_pontok[id+i+1]["y"],ideiglenes_pontok[id+i+1]["z"],ideiglenes_pontok[id+i+1]["e"])
            ut=float(ut)
            befejezettVonalak.append(f"{id+1},{id+i+2},{ut}")
    return befejezettVonalak
def minimalisUtIdonBelul(utTav:list[float],utIdok:list[float],utPontok:list[dict],ido:float,sebesseg:float):
    utErtek=[]
    #meg kell győzödni, hogy nem tudjuk körbejárni az adott idő alatt
    if not reduce(lambda x, y:x+y, utIdok) > ido:
        for id,pont in enumerate(utPontok):
            if id==0 or id==len(utPontok)-1:
                utErtek.append(0)
                continue
            utErtek.append(pont["e"])
        return utTav,utIdok,utPontok,utErtek
    #Első szegmens, előről
    elsoPontok=[utPontok[0]]
    elsoIdok=[utIdok[0]]
    elsoTavolsagok=[utTav[0]]
    pillanatnyiIdo=utIdok[0]
    while pillanatnyiIdo <= ido/2:
        lesz=utIdok[len(elsoPontok)]
        if lesz+pillanatnyiIdo <= ido/2:
            pillanatnyiIdo+=lesz
            elsoPontok.append(utPontok[len(elsoPontok)])
            elsoIdok.append(lesz)
            elsoTavolsagok.append(utTav[len(elsoPontok)-1])
        else:
            break
        
    #Második szegmens, hátulról
    utIdok.reverse()
    utPontok.reverse()
    utTav.reverse()
    pillanatnyiIdo=utIdok[0]
    hatsoPontok=[utPontok[0]]
    hatsoIdok=[utIdok[0]]
    hatsoTavolsagok=[utTav[0]]
    while pillanatnyiIdo <= ido/2:
        lesz=utIdok[len(hatsoPontok)]
        if lesz+pillanatnyiIdo <= ido/2:
            pillanatnyiIdo+=lesz
            hatsoPontok.append(utPontok[len(hatsoPontok)])
            hatsoIdok.append(lesz)
            hatsoTavolsagok.append(utTav[len(hatsoPontok)-1])
        else:
            break
        
    #Összekötjük őket (a hátulról menő arrayt, az elülről menő arrayel)
    #Megnézzük, hogy jó-e így
    while reduce(lambda x, y:x+y, hatsoIdok+elsoIdok+[getHossz(elsoPontok[-1]["x"],
                                                                                              elsoPontok[-1]["y"],
                                                                                              elsoPontok[-1]["z"],
                                                                                              hatsoPontok[-1]["x"],
                                                                                              hatsoPontok[-1]["y"],
                                                                                              hatsoPontok[-1]["z"])/sebesseg]) > ido:
        if elsoPontok[-1]["e"]/elsoIdok[-1] > hatsoPontok[-1]["e"]/hatsoIdok[-1]:
            hatsoTavolsagok.pop()
            hatsoIdok.pop()
            hatsoPontok.pop()
        else:
            elsoTavolsagok.pop()
            elsoIdok.pop()
            elsoPontok.pop()
            
    #összekötés
    kapcsolat=getHossz(elsoPontok[-1]["x"],
                                elsoPontok[-1]["y"],
                                elsoPontok[-1]["z"],
                                hatsoPontok[-1]["x"],
                                hatsoPontok[-1]["y"],
                                hatsoPontok[-1]["z"])
    hatsoPontok.reverse()
    hatsoIdok.reverse()
    hatsoTavolsagok.reverse()
    
    osszPontok=elsoPontok+hatsoPontok
    osszIdok=elsoIdok+[kapcsolat/sebesseg]+hatsoIdok
    osszTavolsagok=elsoTavolsagok+[kapcsolat]+hatsoTavolsagok
    
    for id,point in enumerate(osszPontok):
        if id==0 or id==len(osszPontok)-1:
            utErtek.append(0)
            continue
        utErtek.append(point["e"])
    
    return osszTavolsagok,osszIdok,osszPontok,utErtek


def getGyongy(gyongyokFajl, x,y,z):
    ideiglenesPontok=[]
    for id,line in enumerate(maximalizal(gyongyokFajl,[x,y,z])):
        if id == 0:
            continue
        ideiglenesPontok.append({"x":int(line[0]),
                                 "y":int(line[1]),
                                 "z":int(line[2]),
                                 "e":int(line[3])})
    return ideiglenesPontok


def main(gyongyokFajlNeve,all_time,sebesseg,x,y,z,debug=False):
    #x;y;z;e to vertext to vertex format
    ideiglenesPontok=[]
    vegsoVonalak=initBeolvasas(gyongyokFajlNeve,ideiglenesPontok,x,y,z)
    debug_folder = r"output/"
    source_node = "1"

    if not os.path.exists(debug_folder) and debug:
        os.makedirs(debug_folder)
    else:
        pass

    # create graph from input txt file
    initial_g = main_util.create_graph_from_list(vegsoVonalak)
    if debug:
        print("Initial Graph:")
        main_util.print_edges_with_weight(initial_g)
        initial_g.plot_graph(os.path.join(debug_folder, "graph.png"))

    #todo Validation of the graph: triangle inequality property
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

    
    if debug:
        print(f"\nPath: {euler_tour}")
        final_path = Graph(di_graph=True)
        for i in range(len(euler_tour)-1):
            final_path.add_edge(euler_tour[i],
                                euler_tour[i+1],
                                initial_g.get_edge_weight(euler_tour[i], euler_tour[i+1]))
        final_path.plot_graph(os.path.join(debug_folder, "output.png"))
        print(f"Total traveling cost : {total_weight}")
    all_path,total_weight = main_util.get_total_cost(initial_g, euler_tour)
    
    
    
    osszes_pont=[]
    for pont in euler_tour:
        pont=int(pont)
        osszes_pont.append({"x":ideiglenesPontok[pont-1]["x"],
                                "y":ideiglenesPontok[pont-1]["y"],
                                "z":ideiglenesPontok[pont-1]["z"],
                                "e":ideiglenesPontok[pont-1]["e"]})
    
    utak=getUtHossza(osszes_pont)
    idok=[]
    if sebesseg:
        for ut in utak:
            time=ut/sebesseg
            idok.append(time)
        
    ut_hossz,ut_ido,ut_pontok,ut_ertekek=minimalisUtIdonBelul(utak,idok,osszes_pont,all_time,sebesseg)
    if debug:
        print(f"Debug: path:{euler_tour},cost:{utak};{reduce(lambda x, y:x+y, utak)},{list(map(lambda x: x['e'],osszes_pont))},time:{idok};{reduce(lambda x, y:x+y, idok)}")
        print(f"1{ut_pontok}")
        print(f"2 Idő:{reduce(lambda x, y:x+y,ut_ido)}/{all_time},{ut_ido}")
        print(f"3 Hossz: {reduce(lambda x, y:x+y,ut_hossz)},{ut_hossz}")
        print(f"4 Pont: {reduce(lambda x, y:x+y,ut_ertekek)},{ut_ertekek}")
    return ut_hossz,ut_ido,ut_pontok,ut_ertekek
if __name__ == "__main__":
    sebesseg=float(input("Sebesség(float)(e/s):"))
    ido=float(input("Idő(float)(s):"))
    main(ido,sebesseg,100,100,100)
