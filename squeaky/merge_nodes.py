def merge_nodes(G, nodeA, nodeB, newNode, multi_centroid=False):
    # First create a new node and combine the attributes
    if multi_centroid:
        G.add_node(
            newNode,
            size=G.node[nodeA]['size'] + G.node[nodeB]['size'],
            centroid=";".join(
                set(G.node[nodeA]['centroid'].split(";") +
                    G.node[nodeB]['centroid'].split(";"))),
            members=G.node[nodeA]['members'] + G.node[nodeB]['members'],
            protein=";".join(
                set(G.node[nodeA]['protein'].split(";") +
                    G.node[nodeB]['protein'].split(";"))),
            dna=";".join(
                set(G.node[nodeA]['dna'].split(";") +
                    G.node[nodeB]['dna'].split(";"))),
            annotation=";".join(
                set(G.node[nodeA]['annotation'].split(";") +
                    G.node[nodeB]['annotation'].split(";"))),
            description=";".join(
                set(G.node[nodeA]['description'].split(";") +
                    G.node[nodeB]['description'].split(";"))),
            paralog=(G.node[nodeA]['paralog'] or G.node[nodeB]['paralog']))
    else:
        G.add_node(
            newNode,
            size=G.node[nodeA]['size'] + G.node[nodeB]['size'],
            centroid=G.node[nodeA]['centroid'],
            members=G.node[nodeA]['members'] + G.node[nodeB]['members'],
            protein=G.node[nodeA]['protein'],
            dna=G.node[nodeA]['dna'],
            annotation=G.node[nodeA]['annotation'],
            description=G.node[nodeA]['description'],
            paralog=(G.node[nodeA]['paralog'] or G.node[nodeB]['paralog']))

    # Now iterate through neighbours of each node and add them to the new node
    neigboursB = list(G.neighbors(nodeB))
    neigboursA = list(G.neighbors(nodeA))
    for neighbor in neigboursA:
        if neighbor in neigboursB:
            G.add_edge(
                newNode,
                neighbor,
                weight=G[nodeA][neighbor]['weight'] +
                G[nodeB][neighbor]['weight'],
                members=G[nodeA][neighbor]['members'] +
                G[nodeB][neighbor]['members'])
            neigboursB.remove(neighbor)
        else:
            G.add_edge(
                newNode,
                neighbor,
                weight=G[nodeA][neighbor]['weight'],
                members=G[nodeA][neighbor]['members'])

    for neighbor in neigboursB:
        G.add_edge(
            newNode,
            neighbor,
            weight=G[nodeB][neighbor]['weight'],
            members=G[nodeB][neighbor]['members'])

    # remove old nodes from Graph
    G.remove_nodes_from([nodeA, nodeB])

    return G
