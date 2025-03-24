def _merge_small_clusters(QuCl, Gr, InPa):
    # InPa = Input partition
    # OuPa = Output partition
    # SmCl = Small cluster
    # BiCl = Big cluster
    OuPa = la.ModularityVertexPartition(Gr,
                                        initial_membership=InPa.membership)
    for SmCl_idx in range(QuCl, len(InPa)): # Giving clusters
        SmCl_BiCl_relatedness = list()
        for BiCl_idx in range(QuCl): # Reciving clusters 
            edge = 0
            for SmCl_node in InPa[SmCl_idx]:
                to_comm = InPa.weight_to_comm(SmCl_node, BiCl_idx)
                from_comm = InPa.weight_from_comm(SmCl_node, BiCl_idx)
                edge += to_comm + from_comm
            relatedness = edge / (len(InPa[SmCl_idx])*len(InPa[BiCl_idx]))
            SmCl_BiCl_relatedness.append((BiCl_idx, relatedness))
        best_BiCl_idx = max(SmCl_BiCl_relatedness, key=lambda x: x[1])[0]
        for SmCl_node in InPa[SmCl_idx]:
            OuPa.move_node(SmCl_node, best_BiCl_idx)
    OuPa.renumber_communities()
    return OuPa


def _merge_small_clusters(QuCl, partition):
    partition.renumber_communities()
    while len(partition) > QuCl:
        smallest = len(partition) - 1
        score_list = []
        for i in range(smallest):
            score = _relatedness_score(partition, smallest, i)
            score_list.append((i, score))
        max_score_i = max(score_list, key=lambda x: x[1])[0]
        for i in partition[smallest]:
            partition.move_node(i, max_score_i)
        partition.renumber_communities()
    return partition

def _relatedness_score(partition, idxA, idxB):
    edges = 0
    for i in partition[idxA]:
        to_comm = partition.weight_to_comm(i, idxB)
        from_comm = partition.weight_from_comm(i, idxB)
        edges += to_comm + from_comm
    score = edges / (len(partition[idxA])*len(partition[idxB]))
    return score


def _merge_small_clusters(QuCl, InPa):
    # InPa = Input partition
    # OuPa = Output partition
    # SmCl = Small cluster
    # BiCl = Big cluster
    OuPa = la.ModularityVertexPartition(InPa.graph,
                                        initial_membership=InPa.membership)
    for SmCl in range(QuCl, len(InPa)): # Giving clusters
        mytime = time.time()
        SmCl_BiCl_relatedness = list()
        for BiCl in range(QuCl): # Reciving clusters 
            relatedness = _relatedness_score(InPa, SmCl, BiCl)
            SmCl_BiCl_relatedness.append((BiCl, relatedness))
        best_BiCl = max(SmCl_BiCl_relatedness, key=lambda x: x[1])[0]
        for i in InPa[SmCl]:
            OuPa.move_node(i, best_BiCl)
        print(time.time() - mytime)
    OuPa.renumber_communities()
    return OuPa

def _relatedness_score(partition, idxA, idxB):
    ClA = partition[idxA]
    ClB = partition[idxB]
    edges = len(partition.graph.es.select(_between=(ClA,ClB)))
    score = edges / (len(ClA)*len(ClB))
    return score






def __GetTopWords(partition):
    global_frequency = __GetGlobalFrequency(partition)
    top_words = {}
    for i in range(len(partition)):
        score_list = []
        local_frequency = __GetWordCount(partition, i)
        for j in local_frequency:
            score = local_frequency[j] / (global_frequency[j]+25)
            score_list.append((j, score))
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        top_words[i] = score_list
    return top_words