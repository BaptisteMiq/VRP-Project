import networkx as nx
import matplotlib.pyplot as plt

from graphGeneration import randomDataGenerator

from tabu import tabu

def buildGraph(values, pond, totSize):
    #print(values, pond, totSize)
    size = totSize
    g = [0] * size
    for i in range(size):
        g[i] = [0] * size
        for j in range(size):
            g[i][j] = 0    
            
    #print("len", len(values))
    for v in range(len(values)):
        #print(v, v+1)
        if v+1 >= len(values):
            #print("YO WTF")
            break
        current = values[v]
        neighbour = values[v+1]
        
        #val = str(v+1) + " ( " + str(pond[v]) + " )"
        val = v+1
        #val = pond[v]
        g[current][neighbour] = val
        g[neighbour][current] = val
        
    #pprint.pprint(g)
    return g

def drawGraphs(graph, graphs, labels=None, graph_layout='shell',
               node_size=1200, node_color='blue', node_alpha=0.3,
               node_text_size=14,
               edge_color='gray', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    
    initGraph = graph

    values = []
    labels = []

    for i, vi in enumerate(initGraph):
        for j, vj in enumerate(initGraph):
            if initGraph[i][j] != 0:
                values.append((i, j))
                labels.append(graph[i][j])

    fullGraph = values

    plt.figure(figsize=(20,12))

    # create networkx graph
    G=nx.Graph()
    
    allColors = ["red", "green", "blue", "purple", "pink", "yellow", "brow", "cyan"]
    allColorsIndex = 0
    
    
    ## All paths
    for i in range(len(initGraph)):
        G.add_node(i)
        
    # add edges
    for edge in fullGraph:
        G.add_edge(edge[0], edge[1])
    
    graph_pos=nx.shell_layout(G)


    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness, alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size, font_family=text_font)
    
    ## Taken path
    for i, g in enumerate(graphs):

        values = []
        labels = []

        for i, vi in enumerate(g):
            for j, vj in enumerate(g):
                if g[i][j] != 0:
                    values.append((i, j))
                    labels.append(g[i][j])
                
        G.remove_edges_from(list(G.edges()))
        
        i = 0
        for edge in values:
            G.add_edge(edge[0], edge[1], length=labels[i])
            i += 1
                        
        nx.draw_networkx_edges(G,graph_pos,width=edge_tickness*2, alpha=edge_alpha*3,edge_color=allColors[allColorsIndex])
        edge_labels = dict(zip(values, labels))
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels)
        
        allColorsIndex += 1

    # show graph
    plt.show()

def generateGraph(graph, paths, pond = []):
    drawGraphs(graph, [buildGraph(paths[i], pond, len(graph)) for i in range(len(paths))])

graph = randomDataGenerator(1, 32, False)
(bestPath, bestDistance, totalLength) = tabu(graph, 6, 10)
generateGraph(graph, bestPath)