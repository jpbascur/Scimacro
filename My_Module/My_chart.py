# Importeren modules
import copy
import math

ERROR_MARGIN = 0.00001

def build_graph(node_list):  # main function
    MASTERSET = list()
    for i in range(len(node_list)):
        copy_node_list = copy.deepcopy(node_list)
        x_i = copy_node_list[i]  # get first node into the new list
        X_i = _order_node_list(x_i, copy_node_list)  # get the other nodes into the new list
        Z_i = list()  # list of noodes with coordinates
        X_i[0]['coor'] = (0,0)
        Z_i.append(X_i[0])  # add the first node with coordinates
        X_i[1]['coor'] = _x_i1_coor(X_i[0], X_i[1])
        Z_i.append(X_i[1]) # add the second node with coordinates
        for x_ij in X_i[2:]:
             Z_i.append(_get_coordinates(x_ij, Z_i))
        MASTERSET.append(Z_i)
    OUTPUTLIST = min(MASTERSET, key=lambda x: _graph_stress(x)) # get list of nodes with lowest stress
    return OUTPUTLIST

def _order_node_list(x_i, node_list): # sort nodes, x_i = first node of the list
    X_i = list()
    X_i.append(x_i)
    Y_i = node_list
    Y_i.remove(x_i)
    while len(Y_i) > 0:
        R_i = list()
        for x_j in Y_i:
            R_i.append([x_j, _score(x_j, X_i)])
        x_r = max(R_i, key=lambda x: x[1])[0]
        X_i.append(x_r)
        Y_i.remove(x_r)
    return X_i

def _x_i1_coor(node_1, node_2): # second node coordinate
    x_coordinate = node_1['radius'] + node_2['radius']
    return ((x_coordinate),0)

def _get_coordinates(x_ij, Z_i):
    temp_node_list = list()
    for x_ijm, x_ijn in _pairs_m_n(Z_i):
        temp_ijm = dict()
        temp_ijm['coor'] = x_ijm['coor']
        temp_ijm['radius'] = x_ij['radius'] + x_ijm['radius'] + ERROR_MARGIN
        temp_ijn = dict() # define new node
        temp_ijn['coor'] = x_ijn['coor']
        temp_ijn['radius'] = x_ij['radius'] + x_ijn['radius'] + ERROR_MARGIN
        if _overlaps(temp_ijm, temp_ijn):
            coor_ijmn1, coor_ijmn2 = _cr_intersection(temp_ijm, temp_ijn) # intersection coordinates
            for coor_ijmnk in [coor_ijmn1, coor_ijmn2]:
                temp_ijmnk = dict() # define new node
                temp_ijmnk['edges'] = x_ij['edges'] # copy atributes
                temp_ijmnk['radius'] = x_ij['radius'] # copy atributes
                temp_ijmnk['id'] = x_ij['id'] # copy atributes
                temp_ijmnk['coor'] = coor_ijmnk # add coordinates
                not_overlaps = True
                not_finish = True
                len_Z_i = len(Z_i)
                index_Z_i = 0
                while not_overlaps and not_finish:
                    z_i = Z_i[index_Z_i]
                    index_Z_i += 1
                    not_overlaps = not _overlaps(temp_ijmnk, z_i)
                    not_finish = not (index_Z_i == len_Z_i)
                if not_overlaps:
                    temp_ijmnk['stress'] = _node_stress(temp_ijmnk, Z_i)
                    temp_node_list.append(temp_ijmnk)
    x_ij['coor'] = min(temp_node_list, key = lambda x: x['stress'])['coor']
    return x_ij


#### specific utility functions
def _score(x_j, X_i):
    score = 0
    for x_i in X_i:
        if x_i['id'] != x_j['id']:
            score += x_i['edges'][x_j['id']]
    return score

def _node_stress(node, Z_i): # stress of a node against the graph
    function_sum = 0
    for z_i in Z_i:
        if z_i['id'] != node['id']:
            stress            = node['edges'][z_i['id']]
            distance_squared  = _distance_squared(node['coor'],z_i['coor'])
            function_sum     += stress*distance_squared
    return function_sum

def _graph_stress(Z_i): # total stress of the graph
    function_sum = 0
    len_Z_i = len(Z_i)
    for index_A in range(len_Z_i):
        A = Z_i[index_A]
        for index_B in range(len_Z_i):
            if index_A < index_B:
                B = Z_i[index_B]
                stress = A['edges'][B['id']]
                distance_squared = _distance_squared(A['coor'], B['coor'])
                function_sum += stress * distance_squared
    return function_sum

#### general utility functions            
def _pairs_m_n(Z_i): # order-independent combinaton without repetition
    len_Z_i = len(Z_i)
    pairs_list = list()
    for index_A in range(len_Z_i):
        A = Z_i[index_A]
        for index_B in range(len_Z_i):
            if index_A < index_B:
                B = Z_i[index_B]
                pairs_list.append((A,B))
    return pairs_list

def _distance_squared(c_1, c_2):
    x1, y1 = c_1
    x2, y2 = c_2
    return (x2-x1)**2 + (y2-y1)**2

def _overlaps(node_1,node_2): # if overlaps return true
    r1 = node_1['radius']
    r2 = node_2['radius']
    return (r1+r2)**2 > _distance_squared(node_1['coor'], node_2['coor'])

def _cr_intersection(node_1, node_2): # intersection points between circles
    r1 = node_1['radius']
    x1, y1 = node_1['coor']
    r2 = node_2['radius']
    x2, y2 = node_2['coor']
    R2 = (x2-x1)**2 + (y2-y1)**2
    a = (r1**2-r2**2) / (2*R2)
    b = math.sqrt(2*(r1**2 + r2**2)/R2 - (r1**2-r2**2)**2/R2**2-1)
    fx = (x1+x2)/2 + a*(x2-x1)
    gx = b*(y2-y1) / 2
    ix1 = fx + gx
    ix2 = fx - gx
    fy = (y1+y2)/2 + a*(y2-y1)
    gy = b*(x1-x2) / 2
    iy1 = fy + gy
    iy2 = fy - gy
    return (ix1, iy1), (ix2, iy2)






class bubble_chart():
    def __init__(self):
        self.ERROR_MARGIN = 0.00001
        
    def build_best_graph(self,node_list): # main function
        MASTERSET = list()
        for index in range(len(node_list)): # for each node in node_list
            copy_node_list    = copy.deepcopy(node_list) # create a deep copy of node_list
            x_i               = copy_node_list[index]    # get first node into the new list
            X_i               = self._order_node_list(x_i,copy_node_list) # get the other nodes into the new list
            Z_i               = list() # list of noodes with coordinates
            X_i[0]['coor']       = self._x_i0_coor()
            Z_i.append(X_i[0])         # add the first node with coordinates
            X_i[1]['coor']       = self._x_i1_coor(X_i[0],X_i[1])
            Z_i.append(X_i[1])         # add the second node with coordinates
            for x_ij in X_i[2:]:
                 Z_i.append(self._get_coordinates(x_ij,Z_i))
            MASTERSET.append(Z_i)
        OUTPUTLIST            = min(MASTERSET, key = lambda x: self._graph_stress(x)) # get list of nodes with lowest stress
        return OUTPUTLIST

    def _order_node_list(self,x_i,node_list): # sort nodes, x_i = first node of the list
        X_i     = list()
        X_i.append(x_i)
        Y_i     = node_list
        Y_i.remove(x_i)
        while len(Y_i) > 0:
            R_i     = list()
            for x_j in Y_i:
                R_i.append([x_j,self._relatedness(x_j, X_i)])
            x_r     = max(R_i, key= lambda x: x[1])[0]
            X_i.append(x_r)
            Y_i.remove(x_r)
        return X_i

    def _x_i0_coor(self): # first node coordinate
        return (0,0)
            
    def _x_i1_coor(self,node_1,node_2): # second node coordinate
        x_coordinate = node_1['radius'] + node_2['radius']
        return ((x_coordinate),0)

    def _get_coordinates(self,x_ij,Z_i):
        temp_node_list = list()
        for x_ijm, x_ijn in self._pairs_m_n(Z_i):
            temp_ijm         = dict() # define new node
            temp_ijm['coor']    = x_ijm['coor']
            temp_ijm['radius']  = x_ij['radius'] + x_ijm['radius'] + self.ERROR_MARGIN ################ REVIEW
            temp_ijn         = dict() # define new node
            temp_ijn['coor']    = x_ijn['coor']
            temp_ijn['radius']  = x_ij['radius'] + x_ijn['radius'] + self.ERROR_MARGIN ################ REVIEW
            if self._overlaps(temp_ijm,temp_ijn): # if nodes overlap
                coor_ijmn1, coor_ijmn2 = self._cr_intersection(temp_ijm,temp_ijn) # intersection coordinates
                for coor_ijmnk in [coor_ijmn1, coor_ijmn2]:
                    temp_ijmnk          = dict() # define new node
                    temp_ijmnk['edges']    = x_ij['edges'] # copy atributes
                    temp_ijmnk['radius']   = x_ij['radius'] # copy atributes
                    temp_ijmnk['id']       = x_ij['id'] # copy atributes
                    temp_ijmnk['coor']     = coor_ijmnk # add coordinates
                    not_overlaps        = True # overlaping indicator
                    not_finish          = True
                    len_Z_i             = len(Z_i)
                    index_Z_i           = 0
                    while not_overlaps and not_finish:
                        z_i          = Z_i[index_Z_i]
                        index_Z_i   += 1
                        not_overlaps = not self._overlaps(temp_ijmnk,z_i)
                        not_finish   = not (index_Z_i == len_Z_i)
                    if not_overlaps: # test overlaping indicator
                        temp_ijmnk['stress']    = self._node_stress(temp_ijmnk, Z_i)
                        temp_node_list.append(temp_ijmnk)
        x_ij['coor']   = min(temp_node_list, key = lambda x: x['stress'])['coor']
        return x_ij


    #### specific utility functions
    def _relatedness(self,x_j, X_i): # write output into the class TokenClass
        function_sum = 0
        for x_i in X_i:
            if x_i['id'] != x_j['id']:
                function_sum += x_i['edges'][x_j['id']]
        return function_sum

    def _node_stress(self,node, Z_i): # stress of a node against the graph
        function_sum = 0
        for z_i in Z_i:
            if z_i['id'] != node['id']:
                stress            = node['edges'][z_i['id']]
                distance_squared  = self._distance_squared(node['coor'],z_i['coor'])
                function_sum     += stress*distance_squared
        return function_sum

    def _graph_stress(self,Z_i): # total stress of the graph
        function_sum = 0
        len_Z_i      = len(Z_i)
        for index_A in range(len_Z_i):
            A     = Z_i[index_A]
            for index_B in range(len_Z_i):
                if index_A < index_B:
                    B                 = Z_i[index_B]
                    stress            = A['edges'][B['id']]
                    distance_squared  = self._distance_squared(A['coor'],B['coor'])
                    function_sum     += stress*distance_squared
        return function_sum
            
    #### general utility functions            
    def _pairs_m_n(self,Z_i): # order-independent combinaton without repetition
        len_Z_i     = len(Z_i)
        pairs_list  = list()
        for index_A in range(len_Z_i):
            A     = Z_i[index_A]
            for index_B in range(len_Z_i):
                if index_A < index_B:
                    B     = Z_i[index_B]
                    pairs_list.append((A,B))
        return pairs_list

    def _distance_squared(self,c_1,c_2):
        x1,y1 = c_1
        x2,y2 = c_2
        return (x2 - x1)**2 + (y2 - y1)**2

    def _overlaps(self,node_1,node_2): # if overlaps return true
        r1 = node_1['radius']
        r2 = node_2['radius']
        return (r1 + r2)**2 > self._distance_squared(node_1['coor'],node_2['coor'])
        
    def _cr_intersection(self,node_1,node_2): # intersection points between circles
        r1        = node_1['radius']
        x1,y1     = node_1['coor']
        r2        = node_2['radius']
        x2,y2     = node_2['coor']
        R2    = (x2 - x1)**2 + (y2 - y1)**2
        a     = (r1**2 - r2**2) / (2 * R2)
        b     = math.sqrt(2 * (r1**2 + r2**2) / R2 - (r1**2 - r2**2)**2 / R2**2 - 1)
        fx    = (x1+x2) / 2 + a * (x2 - x1)
        gx    = b * (y2 - y1) / 2
        ix1   = fx + gx
        ix2   = fx - gx
        fy    = (y1+y2) / 2 + a * (y2 - y1)
        gy    = b * (x1 - x2) / 2
        iy1   = fy + gy
        iy2   = fy - gy
        return (ix1, iy1), (ix2, iy2)
