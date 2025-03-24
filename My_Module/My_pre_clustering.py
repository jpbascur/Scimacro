import pyodbc
import pandas as pd
import igraph as ig

def Run(user_name, level, cluster_id):
    out_string = __GetSqlQuery(level, cluster_id)
    documents_data = __GetDocumentsData(out_string, user_name)
    translation = __GetTranslationDict(documents_data['translation'])
    graph = __GetGraph(documents_data['papers'], documents_data['conections'],
                       documents_data['paper_np'])
    preculster_dict = {'graph': graph, 'translation': translation}
    return preculster_dict

def __GetSqlQuery(level, cluster_id):
    if level == 1:
        cluster_id_column = "cluster_id1 = "
    elif level == 2:
        cluster_id_column = "cluster_id2 = "
    elif level == 3:
        cluster_id_column = "cluster_id3 = "
    out_string = """
    /*select the cluster*/
    SELECT
    ut
    INTO #ut
    FROM [wosclassification1913]..[clustering]
    WHERE """ + cluster_id_column + str(cluster_id) + """

    /*create the network of the cluster*/
    SELECT
    s_ut
    ,c_ut
    INTO #sut_cut
    FROM woskb..cwts_pairs
    WHERE s_ut in (SELECT ut from #ut) AND c_ut in (SELECT ut from #ut)

    /*get the number of citations within the clusters*/
    SELECT
    a.ut
    ,sum(case when b.c_ut is null then 0 else 1 end) as n_cits
    INTO #ut_ncits
    FROM #ut AS a
    LEFT JOIN #sut_cut AS b ON a.ut = b.s_ut
    GROUP BY
    a.ut

    /*create the data table of the papers*/
    SELECT
    a.ut
    ,a.n_cits
    ,c.ti 
    ,b.pub_year
    ,b.author_first
    ,b.author_et_al
    ,b.source
    ,c.ab
    ,c.de
    ,c.id
    ,b.doi
    INTO #ut_data
    FROM #ut_ncits AS a
    LEFT JOIN woskb..cwts_pub_details AS b ON a.ut = b.ut
    LEFT JOIN woskb..cwts_text_data AS c ON a.ut = c.ut

    /*get the nounphrase codes of the titles*/
    SELECT
    a.ut
    ,b.cwts_np_no
    INTO #ut_npno
    FROM #ut as a
    JOIN [woskb].[dbo].[cwts_ti_np] as b on a.ut = b.ut

    /*get the nounphrase codes of the abstracts*/
    INSERT INTO #ut_npno
    SELECT
    a.ut
    ,b.cwts_np_no
    FROM #ut as a 
    JOIN [woskb].[dbo].[cwts_ab_np] as b on a.ut = b.ut

    /*remove duplicates*/
    SELECT DISTINCT
    ut
    ,cwts_np_no
    INTO #distinct_ut_npno
    FROM #ut_npno

    /*make nounphrase codes unique*/
    SELECT DISTINCT
    cwts_np_no
    INTO #distinct_npno
    FROM #distinct_ut_npno

    /*get the nounphrase text of the nounphrase codes*/
    SELECT
    a.cwts_np_no,
    b.np
    INTO #npno_np
    FROM #distinct_npno as a
    JOIN [woskb].[dbo].[cwts_np] as b on a.[cwts_np_no] = b.[cwts_np_no]
    """
    return out_string

def __GetDocumentsData(out_string, user_name):
    conn = __GetConn(user_name)
    cursor = conn.cursor()
    cursor.execute(out_string)
    t_query = "select * from #npno_np order by cwts_np_no"
    n_query = "select * from #distinct_ut_npno order by ut, cwts_np_no"
    p_query = "select * from #ut_data order by n_cits desc"
    c_query = "select * from #sut_cut"
    translation = pd.read_sql(t_query, conn)
    paper_np = pd.read_sql(n_query, conn)
    papers = pd.read_sql(p_query, conn)
    conections = pd.read_sql(c_query, conn)
    documents_data = {'translation': translation, 'paper_np': paper_np,
                      'papers': papers, 'conections': conections}
    cursor.close()
    conn.close()
    del(cursor)
    del(conn)
    return documents_data

def __GetConn(user_name):
    conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                          server='SPCWTDBS02',
                          user=user_name,
                          trusted_connection='yes',
                          unicode_results=False,
                          MARS_Connection='Yes')
    return conn

def __GetTranslationDict(translation):
    translation_dict = dict()
    for index, row in translation.iterrows():
        translation_dict[row['cwts_np_no']] = row['np']
    return translation_dict

def __GetGraph(papers, conections, paper_np):
    graph = ig.Graph.DictList(vertices=papers.to_dict('records'),
                              edges=conections.to_dict('records'),
                             directed=True,
                             vertex_name_attr='ut',
                             edge_foreign_keys=('s_ut', 'c_ut'))
    ut_dict = dict()
    for index, row in papers.iterrows():
        ut_dict[row['ut']] = index
    paper_np_dict = dict()
    for index in range(len(ut_dict)):
        paper_np_dict[index] = list()
    for index, row in paper_np.iterrows():
        paper_np_dict[ut_dict[row['ut']]].append(row['cwts_np_no'])
    for node in graph.vs:
        index = node.index
        node['np'] = paper_np_dict[index]
    graph.simplify()
    return graph