from My_Module import My_chart
import math
import collections

def PostDict(partition):
    chart_nodes = __BuildGraph(partition)
    frequency = __GetFrequency(partition)
    cluster_info = __GetInfo(partition, frequency)
    post_dict = {'nodes':chart_nodes, 'cluster_info':cluster_info, 'global_frequency':frequency['global_frequency']}
    return post_dict

def __BuildGraph(partition):
    node_list = []
    relatedness_dict = __RelatednesDict(partition)
    for i in range(len(partition)):
        node = {}
        node['id'] = i
        node['edges'] = relatedness_dict[i]
        node['radius'] = math.sqrt(len(partition[i]) / math.pi)
        node_list.append(node)
    chart_nodes = My_chart.bubble_chart().build_best_graph(node_list)
    return chart_nodes

def __RelatednesDict(partition):
    relatedness_dict = {}
    for i in range(len(partition)):
        relatedness_dict[i] = {}
        for j in range(len(partition)):
            if i == j:
                relatedness_dict[i][j] = 1
            else:
                score = __RelatednessScore(partition, i, j)
                relatedness_dict[i][j] = score
    return relatedness_dict

def __RelatednessScore(partition, idxA, idxB):
    edges = 0
    for i in partition[idxA]:
        to_comm = partition.weight_to_comm(i, idxB)
        from_comm = partition.weight_from_comm(i, idxB)
        edges += to_comm + from_comm
    score = edges / (len(partition[idxA])*len(partition[idxB]))
    return score

def __GetFrequency(partition):
    global_word_list = []
    local_frequency = {}
    for i in range(len(partition)):
        local_word_list = []
        for j in partition[i]:
            node_word_list = partition.graph.vs[j]['np']
            local_word_list += node_word_list
            global_word_list += node_word_list
        local_frequency[i] = dict(collections.Counter(local_word_list))
    global_frequency = dict(collections.Counter(global_word_list))
    frequency = {'global_frequency':global_frequency, 'local_frequency':local_frequency}
    return frequency

def __GetInfo(partition, frequency):
    cluster_info = {}
    for i in range(len(partition)):
        info = {}
        info['id'] = i + 1
        info['members'] = partition[i]
        info['size'] = len(partition[i])
        info['local_frequency'] = frequency['local_frequency'][i]
        cluster_info[info['id']] = info
    return cluster_info