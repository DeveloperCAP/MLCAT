"""
This module is used to find the community structure of the network according to the Infomap method of Martin Rosvall
and Carl T. Bergstrom and returns an appropriate VertexClustering object. This module has been implemented using both
the iGraph package and the Infomap tool from MapEquation.org. The VertexClustering object represents the clustering of
the vertex set of a graph and also provides some methods for getting the subgraph corresponding to a cluster and such.

"""
import json
import subprocess
import sys

import networkx as nx
import igraph
import numpy
# import plotly
# from matplotlib import pyplot as plt
# from plotly.tools import FigureFactory as FF
# from scipy.cluster.hierarchy import dendrogram, linkage

from analysis.author import ranking
from util.read import *

sys.setrecursionlimit(10000)


def write_matrix(json_data, tree_filename="infomap/output/" + "author_graph.tree"):
    """

    :param json_data:
    :return:
    """
    top_authors = set()
    top_authors_data = dict()
    author_scores = ranking.get(active_score=2, passive_score=1, write_to_file=False)
    index = 0
    for email_addr, author_score in author_scores:
        index += 1
        top_authors.add(email_addr)
        top_authors_data[email_addr] = [author_score]
        if index == 100:
            break

    print("Adding nodes to author's graph...")
    author_graph = nx.DiGraph()
    for msg_id, message in json_data.items():
        if message['From'] in top_authors:
            if message['Cc'] is None:
                addr_list = message['To']
            else:
                addr_list = message['To'] | message['Cc']
            for to_address in addr_list:
                if to_address in top_authors:
                    if author_graph.has_edge(message['From'], to_address):
                        author_graph[message['From']][to_address]['weight'] *= \
                            author_graph[message['From']][to_address]['weight'] / (author_graph[message['From']][to_address]['weight'] + 1)
                    else:
                        author_graph.add_edge(message['From'], to_address, weight=1)

    author_graph_undirected = author_graph.to_undirected()
    clustering_coeff = nx.clustering(author_graph_undirected)
    in_degree_dict = author_graph.in_degree(nbunch=author_graph.nodes_iter())
    out_degree_dict = author_graph.out_degree(nbunch=author_graph.nodes_iter())

    for email_addr in top_authors:
        top_authors_data[email_addr].append(in_degree_dict[email_addr])
        top_authors_data[email_addr].append(out_degree_dict[email_addr])
        top_authors_data[email_addr].append(clustering_coeff[email_addr])

    print("Parsing", tree_filename + "...")
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:
            if not line or line[0] == '#':
                continue
            line = line.split()
            if line[2][1:-1] in top_authors:
                top_authors_data[line[2][1:-1]].append(float(line[1]))
        tree_file.close()

    with open("top_authors_data.csv", 'w') as output_file:
        output_file.write("Email Address,Author Score,In-Degree,Out-Degree,Clustering Coeff,Module Flow\n")
        for email_addr, data_list in top_authors_data.items():
            output_file.write(email_addr+","+",".join([str(x) for x in data_list])+"\n")
        output_file.close()
    print("Authors data written to file.")


def write_pajek(author_graph, filename="author_graph.net"):
    # Write Pajek file compatible with the Infomap Community Detection module
    nx.write_pajek(author_graph, filename)
    lines_in_file= list()
    with open(filename, 'r') as pajek_file:
        for line in pajek_file:
            lines_in_file.append(line)
    num_vertices = int(lines_in_file[0].split()[1])
    for i in range(1, num_vertices+1):
        line = lines_in_file[i].split()
        line[1] = "\"" + line[1] + "\""
        del line[2:]
        line.append("\n")
        lines_in_file[i] = " ".join(line)
    with open(filename, 'w') as pajek_file:
        for line in lines_in_file:
            pajek_file.write(line)
    print("Written to:", filename)


def write_pajek_for_submodules(json_data, tree_filename="infomap/output/"+"author_graph.tree"):
    """

    :param tree_filename:
    :param json_data:
    :return:
    """
    current_module = 1
    authors_in_module = set()
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:

            if line[0] == '#':
                continue

            if int(line[:line.index(":")]) > current_module:
                author_graph = nx.DiGraph()
                for msg_id, message in json_data.items():
                    if message['Cc'] is None:
                        addr_list = message['To']
                    else:
                        addr_list = message['To'] | message['Cc']
                    # Adding only the required edges to the authors graph:
                    for to_address in addr_list & authors_in_module:
                        if author_graph.has_edge(message['From'], to_address):
                            author_graph[message['From']][to_address]['weight'] += 1
                        else:
                            author_graph.add_edge(message['From'], to_address, weight=1)
                output_filename = "submodule_"+str(current_module)+".net"
                write_pajek(author_graph, filename=output_filename)
                # Run the infomaps algorithm
                output_folder = 'output_submodule' + str(current_module) + "/"
                subprocess.run(args=['mkdir', output_folder])
                subprocess.run(args=['./infomap/Infomap', output_filename + ' ' + output_folder
                               +' --tree --bftree --btree -d -c --node-ranks --flow-network --map'])

                current_module += 1
                authors_in_module = {line[line.index("\"")+1:line.rindex("\"")]}
            else:
                authors_in_module.add(line[line.index("\"")+1:line.rindex("\"")])


def vertex_clustering(json_filename, nodelist_filename, edgelist_filename, foldername, time_limit=None, ignore_lat=False):
    """

    :param json_filename:
    :param time_limit: Time limit can be specified here in the form of a timestamp in one of the identifiable formats
    and all messages that have arrived after this timestamp will be ignored.
    :param ignore_lat: If true, then messages that belong to threads that have only a single author are ignored.
    :return:
    """

    json_data = dict()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    if time_limit is None:
        time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_before_time = set()
    time_limit = get_datetime_object(time_limit)
    print("All messages before", time_limit, "are being considered.")

    if not ignore_lat:
        with open(json_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                if json_obj['Time'] < time_limit:
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    from_addr = email_re.search(json_obj['From'])
                    json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                    json_obj['To'] = set(email_re.findall(json_obj['To']))
                    json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    json_data[json_obj['Message-ID']] = json_obj
    else:
        lone_author_threads = get_lone_author_threads(False, nodelist_filename, edgelist_filename)
        with open(json_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                if json_obj['Message-ID'] not in lone_author_threads:
                    json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                    if json_obj['Time'] < time_limit:
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        from_addr = email_re.search(json_obj['From'])
                        json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                        json_obj['To'] = set(email_re.findall(json_obj['To']))
                        json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

    author_graph = igraph.Graph()
    author_graph.es["weight"] = 1.0
    author_map = dict()

    """
    Graphs can also be indexed by strings or pairs of vertex indices or vertex names. When a graph is
    indexed by a string, the operation translates to the retrieval, creation, modification or deletion
    of a graph attribute.

    When a graph is indexed by a pair of vertex indices or names, the graph itself is treated as an
    adjacency matrix and the corresponding cell of the matrix is returned. Assigning values different
    from zero or one to the adjacency matrix will be translated to one, unless the graph is weighted,
    in which case the numbers will be treated as weights.
    """
    top_authors = set()
    author_scores = ranking.get(json_filename, None, active_score=2, passive_score=1, write_to_file=False)
    index = 0
    for email_addr, author_score in author_scores:
        index += 1
        top_authors.add(email_addr)
        if index == 100:
            break

    index = 0
    for id, node in json_data.items():
        if node['From'] in top_authors:
            if node['From'] not in author_map:
                author_map[node['From']] = index
                author_graph.add_vertex(name=node['From'], label=node['From'])
                index += 1
            for to_addr in node['To']:
                if to_addr in top_authors:
                    if to_addr not in author_map:
                        author_map[to_addr] = index
                        author_graph.add_vertex(name=to_addr, label=to_addr)
                        index += 1
                    if author_graph[node['From'], to_addr] == 0:
                        author_graph.add_edge(node['From'], to_addr, weight=1)
                    else:
                        author_graph[node['From'], to_addr] += 1
            if node['Cc'] is None:
                continue
            for to_addr in node['Cc']:
                if to_addr in top_authors:
                    if to_addr not in author_map:
                        author_map[to_addr] = index
                        author_graph.add_vertex(name=to_addr, label=to_addr)
                        index += 1
                    if author_graph[node['From'], to_addr] == 0:
                        author_graph.add_edge(node['From'], to_addr, weight=1)
                    else:
                        author_graph[node['From'], to_addr] += 1

    print("Nodes and Edges added to iGraph.")

    vertex_dendogram = author_graph.community_edge_betweenness(clusters=8, directed=True, weights="weight")
    igraph.plot(vertex_dendogram, foldername + "vd.pdf", vertex_label_size=3, bbox=(1200, 1200))
    print("Dendrogram saved as PDF.")

    vertex_clustering_obj = author_graph.community_infomap(edge_weights=author_graph.es["weight"])
    igraph.plot(vertex_clustering_obj, foldername + "vc.pdf", vertex_label_size=10, bbox=(1500, 1500), edge_color="gray")
    print("Vertex Clustering saved as PDF.")

    with open(foldername + "community_vertex_clustering.txt", 'w') as output_file:
        output_file.write(str(vertex_clustering_obj))
        output_file.close()