#clustering functions
import leidenalg as la
import time

def ClusteringPipeline(QuCl, Gr):
    # QuCl = Quantity of clusters
    # Gr = Graph
    mytime = time.time()
    partition = __OptimizePartition(QuCl, Gr)
    print(time.time() - mytime)
    mytime = time.time()
    partition = __MergeSmallClusters(QuCl, partition)
    print(time.time() - mytime)
    return partition

def __OptimizePartition(QuCl, Gr):
    # Pw = Power with base 10 of the resolution parameter
    # GrCl = Greatest cluter of the clustering
    Pw = -2
    partition = __FindPartition(Gr, Pw)
    GrCl = max([len(partition[x]) for x in range(len(partition))])
    while __Condition(QuCl, Gr, GrCl, Pw, partition, 'bigger'):  # Make GrCl bigger
        Pw += -2
        partition = __FindPartition(Gr, Pw)
        GrCl = max([len(partition[x]) for x in range(len(partition))])
    while __Condition(QuCl, Gr, GrCl, Pw, partition, 'smaller'):  # Make GrCl smaller
        Pw += 0.5
        partition = __FindPartition(Gr, Pw)
        GrCl = max([len(partition[x]) for x in range(len(partition))])
    print('Resolution: ' + str(10 ** Pw))
    print('Clusters: ' + str(len(partition)))
    return partition

def __Condition(QuCl, Gr, GrCl, Pw, partition, make):
    condition = False
    if make == 'bigger':
        condition = GrCl < Gr.vcount()/QuCl
    elif make == 'smaller':
        if len(partition) > 3:
            condition = GrCl > (len(partition[1])+len(partition[2]))
        else:
            condition = True
    return condition

def __FindPartition(Gr, Pw):
    partition = la.find_partition(Gr, la.CPMVertexPartition,
                                  resolution_parameter=10 ** Pw,
                                  seed=1, n_iterations=5)
    return partition

def __MergeSmallClusters(QuCl, partition, remove_small=False):
    partition.renumber_communities()
    if remove_small:
        partition = _RemoveSmallClusters(partition)
    while len(partition) > QuCl:
        smallest = len(partition) - 1
        score_list = []
        for i in range(smallest):
            score = __RelatednessScore(partition, smallest, i)
            score_list.append((i, score))
        max_score_i = max(score_list, key=lambda x: x[1])[0]
        for i in partition[smallest]:
            partition.move_node(i, max_score_i)
        partition.renumber_communities()
    return partition

def __RelatednessScore(partition, idxA, idxB):
    ClA = partition[idxA]
    ClB = partition[idxB]
    edges = len(partition.graph.es.select(_between=(ClA, ClB)))
    score = edges / (len(ClA)*len(ClB))
    return score

def _RemoveSmallClusters(partition):
    n_0 = partition.n
    sub_list = [x for x in range(len(partition)) if len(partition[x]) > 1]
    clusters = [partition[x] for x in sub_list]
    nodes = [x for y in clusters for x in y]
    SubGr = partition.graph.subgraph(nodes)
    membership = [x for x in partition.membership if x in sub_list]
    partition = la.ModularityVertexPartition(SubGr,
                                             initial_membership=membership)
    partition.renumber_communities()
    print('Removed: ' + str(n_0-partition.n))
    return partition