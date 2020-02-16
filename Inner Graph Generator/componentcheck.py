import networkx as nx
from NESW import num_cips


def cip_rule_filter(graph_list):
    """
    Given List of Graphs
    Returns filtered list that satisfy the CIP rule

    CIP Rule = 2 CIP on outer biconnected components
                no CIP on inner biconnected components
                Less than 4 CIPs
    """
    filtered_graphs = []
    a = 0
    for graph in graph_list:
        print(f'reach {a}')
        print(graph.edges())
        a += 1
        cip_check = True
        outer_comps, inner_comps, single_component = component_break(graph)
        # list, list, element
        # print(outer_comps, inner_comps, single_component)
        if not single_component:
            # CIP Rule for Outer Components
            for comp in outer_comps:
                if num_cips(comp) > 2 and not complex_triangle_check(comp):
                    cip_check = False
                    print('FALSE')
            # CIP Rule for Inner Components
            for comp in inner_comps:
                if num_cips(comp) > 0 and not complex_triangle_check(comp):
                    cip_check = False
                    print('FALSE')
        else:
            # CIP Rule for single_component Components
            if num_cips(single_component) > 4 and \
                    not complex_triangle_check(single_component):
                cip_check = False
                print('FALSE')
        if cip_check:
            filtered_graphs.append(graph)

    return filtered_graphs


def cip_rule_check(graph):
    """
    Given A Graph
    Returns true if cip rule is satisfied

    CIP Rule = 2 CIP on outer biconnected components and no CIP on
    inner biconnected components
    """
    cip_check = True
    outer_comps, inner_comps, single_component = component_break(graph)
    # CIP Rule for Outer Components
    for comp in outer_comps:
        if num_cips(comp) > 2:
            cip_check = False

    # CIP Rule for Outer Components
    for comp in inner_comps:
        if num_cips(comp) > 0:
            cip_check = False
    # CIP Rule for single_component Components
    if num_cips(single_component) > 4:
        cip_check = False
    return cip_check


def component_break(given_graph):
    """
    Given a graph,
    returns [list of the 2 outer components(1 articulation point) with 2cip],
    [list of other inner components(2 articulation points) with 0 cip]
    """
    test_graph = given_graph.copy()
    cutvertices = list(nx.articulation_points(test_graph))

    # O(biconnected_components * cutvertices)
    inner_components = []
    outer_components = []
    if len(cutvertices) == 0:
        single_component = test_graph
        return 0, 0, single_component
    for peice_edges in nx.biconnected_component_edges(test_graph):
        # Find num cutvertices
        # num_cutverts = nx.intersection(peice, cutvertices)
        peice = nx.Graph()
        peice.add_edges_from(list(peice_edges))
        num_cutverts = 0
        for cutvert in cutvertices:
            if cutvert in peice.nodes():
                num_cutverts += 1

        if num_cutverts == 2:
            inner_components.append(peice)
        elif num_cutverts == 1:
            outer_components.append(peice)
        else:
            print("Illegal Case 1")
            print(test_graph.edges())

        if len(outer_components) > 2:
            print("Illegal Case 2")
            print(test_graph)
    return outer_components, inner_components, 0


def complex_triangle_check(graph):
    for compedges in nx.biconnected_component_edges(graph):
        comp=nx.Graph()
        comp.add_edges_from(compedges)
        
        comp=comp.to_directed()

        # Get all triangles
        all_cycles = list(nx.simple_cycles(comp))
        all_triangles = []
        for cycle in all_cycles:
            if len(cycle) == 3:
                all_triangles.append(cycle)

        # Get edges on outer boundary
        outer_boundary = []
        for edge in comp.edges:
            count = 0
            for triangle in all_triangles:
                if edge[0] in triangle and edge[1] in triangle:
                    count += 1
            if count == 2:
                outer_boundary.append(edge)

        # Get Vertex-Set of outerboundary
        outer_vertices = []
        for edge in outer_boundary:
            if edge[0] not in outer_vertices:
                outer_vertices.append(edge[0])
            if edge[1] not in outer_vertices:
                outer_vertices.append(edge[1])

        if len(outer_vertices) == 3:
            if len(comp) != 3:
               return False
    return True
