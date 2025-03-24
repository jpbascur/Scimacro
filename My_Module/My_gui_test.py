import pickle
import tkinter as tk
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from My_Module import My_clustering, My_post

def execute_clustering_gui():
    root = tk.Tk()
    app = clustering_gui(root)
    root.mainloop() 

class clustering_gui:
    # LeFr = Left Frame
    # LoDa = Load Data
    # Ra = Radiobutton
    # VaRa = Variable of the Radiobutton
    # QuCl = Quantity of Clusters
    # ClId = Cluster Id
    # ClSo = Clustering Solution
    # ShLa = Show Label
    # ShPa = Show Papers
    # DoPa = Download Papers
    # Gr = Graph
    def __init__(self, root):
        self.selected_papers = []
        self.show_x_papers = 100
        self.data = {'translation': None,
                     'translation_reverse': None,
                     'global_frequency': {},
                     'Gr': {},
                     'chart': {}, 'cluster_info': {}, 'ClId': {},
                     'labels':{},
                     'nodes':{}}
        self.data['Gr'][0] = None
        self.data['chart'][0] = mpl.figure.Figure(figsize=(7.5, 7.5))
        self.data['cluster_info'][0] = False
        self.data['global_frequency'][0] = False
        self.data['ClId'][0] = False
        self.data['labels'][0] = False
        self.data['nodes'][0] = False
        self.VaRa = tk.IntVar()
        self.VaRa.set(0)
        self.VaRaText = {1: tk.StringVar(), 2: tk.StringVar(), 3: tk.StringVar(), 
                         4: tk.StringVar(), 5: tk.StringVar(), 6: tk.StringVar(),
                         7: tk.StringVar()}
        self.selected_cluster = tk.IntVar()
        self.selected_cluster.set(None)
        self.selected_cluster_text = tk.StringVar()
        self.selected_cluster_text.set('No cluster selected')
        self.fig = self.data['chart'][self.VaRa.get()]
        self.sel_row = tk.IntVar()
        self.sel_row.set(0)
        self.enviroment = tk.StringVar()
        self.enviroment.set('all_data')
        self.root = root
        root.title('Scientific Macroscope')
        
        #### GUI
        self.LeFr0 = tk.Frame(self.root)
        self.LeFr0.grid(row=100, column=100, sticky=tk.NW)
        self.LoDaTe = tk.Text(self.LeFr0, height=1, width=20)
        self.LoDaBu = tk.Button(self.LeFr0, text='Load', command=self.LoDa)
        self.Ra0Ra = tk.Radiobutton(self.LeFr0, text='All Data', variable=self.VaRa, value=0, command=self.ClickRa)
        self.Ra1Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[1])
        self.Ra1Ra = tk.Radiobutton(self.LeFr0, text='Clustering 1', variable=self.VaRa, value=1, command=self.ClickRa)
        self.Ra2Te = tk.Label(self.LeFr0, text='-', textvariable= self.VaRaText[2])
        self.Ra2Ra = tk.Radiobutton(self.LeFr0, text='Clustering 2', variable=self.VaRa, value=2, command=self.ClickRa)
        self.Ra3Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[3])
        self.Ra3Ra = tk.Radiobutton(self.LeFr0, text='Clustering 3', variable=self.VaRa, value=3, command=self.ClickRa)
        self.Ra4Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[4])
        self.Ra4Ra = tk.Radiobutton(self.LeFr0, text='Clustering 4', variable=self.VaRa, value=4, command=self.ClickRa)
        self.Ra5Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[5])
        self.Ra5Ra = tk.Radiobutton(self.LeFr0, text='Clustering 5', variable=self.VaRa, value=5, command=self.ClickRa)
        self.Ra6Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[6])
        self.Ra6Ra = tk.Radiobutton(self.LeFr0, text='Clustering 6', variable=self.VaRa, value=6, command=self.ClickRa)
        self.Ra7Te = tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[7])
        self.Ra7Ra = tk.Radiobutton(self.LeFr0, text='Clustering 7', variable=self.VaRa, value=7, command=self.ClickRa)
        self.QuClLa = tk.Label(self.LeFr0, text='Q Clusters')
        self.QuClTe = tk.Text(self.LeFr0, height=1, width=3, bg='#D3D3D3')
        self.QuClTe.insert(tk.INSERT, '20')
        self.ClIdLa = tk.Label(self.LeFr0, text='Clusters ID')
        self.ClIdTe = tk.Text(self.LeFr0, height=3, width=20)
        self.ClSoBu = tk.Button(self.LeFr0, text='Create clustering solution', command=self.CreateClSo)
        self.QueryLa = tk.Label(self.LeFr0, text='Query search')
        self.QueryTe = tk.Text(self.LeFr0, height=1, width=20)
        self.QueryBu = tk.Button(self.LeFr0, text='Search', command=self.QuerySearch)
        
        self.LoDaTe.grid(row=100, column=100, sticky=tk.W, pady=(10, 0))
        self.LoDaBu.grid(row=101, column=100, pady=(0, 50))
        self.Ra0Ra.grid(row=202, column=100, sticky=tk.W)
        self.Ra1Te.grid(row=203, column=100, sticky=tk.W)
        self.Ra1Ra.grid(row=204, column=100, sticky=tk.W)
        self.Ra2Te.grid(row=205, column=100, sticky=tk.W)
        self.Ra2Ra.grid(row=206, column=100, sticky=tk.W)
        self.Ra3Te.grid(row=207, column=100, sticky=tk.W)
        self.Ra3Ra.grid(row=208, column=100, sticky=tk.W)
        self.Ra4Te.grid(row=209, column=100, sticky=tk.W)
        self.Ra4Ra.grid(row=210, column=100, sticky=tk.W)
        self.Ra5Te.grid(row=211, column=100, sticky=tk.W)
        self.Ra5Ra.grid(row=212, column=100, sticky=tk.W)
        self.Ra6Te.grid(row=213, column=100, sticky=tk.W)
        self.Ra6Ra.grid(row=214, column=100, sticky=tk.W)
        self.Ra7Te.grid(row=215, column=100, sticky=tk.W)
        self.Ra7Ra.grid(row=216, column=100, sticky=tk.W, pady=(0, 50))
        self.QuClLa.grid(row=300, column=100, sticky=tk.W)
        self.QuClTe.grid(row=301, column=100, sticky=tk.W)
        self.ClIdLa.grid(row=302, column=100, sticky=tk.W)
        self.ClIdTe.grid(row=303, column=100, sticky=tk.W)
        self.ClSoBu.grid(row=304, column=100)
        self.QueryLa.grid(row=305, column=100)
        self.QueryTe.grid(row=306, column=100)
        self.QueryBu.grid(row=307, column=100)
        
        self.LeFr1 = tk.Frame(self.root)
        self.LeFr1.grid(row=100, column=200, sticky=tk.W)
        
        self.Canvas = FigureCanvasTkAgg(self.fig, master=self.LeFr1)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().grid(row=100, column=100, padx=10, pady=10, sticky=tk.W)
       
        self.LeFr2 = tk.Frame(self.root)
        self.LeFr2.grid(row=100, column=300, sticky=tk.W)
        self.LiBoFr = tk.Frame(self.LeFr2)
        self.LiBoFr.grid(row=100, column=100)
        
        self.ScrollY = tk.Scrollbar(self.LiBoFr, orient='vertical')
        self.ScrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.ScrollX = tk.Scrollbar(self.LiBoFr, orient='horizontal')
        self.ScrollX.pack(side=tk.BOTTOM, fill=tk.X)
        self.LiBo = tk.Listbox(self.LiBoFr, yscrollcommand=self.ScrollY.set, xscrollcommand=self.ScrollX.set, height=35,
                               width=80)
        self.LiBo.bind('<<ListboxSelect>>', self.ClickListbox)
        self.LiBo.pack(side=tk.LEFT, fill=tk.BOTH)
        self.ScrollY.config(command=self.LiBo.yview)
        self.ScrollX.config(command=self.LiBo.xview)
        self.ShLaBu = tk.Button(self.LeFr2, text='Show Labels', command=self.CreateShLa)
        self.ShPaBu = tk.Button(self.LeFr2, text='Show Paper List',  command=self.CreateShPa)
        self.DoPaLa = tk.Label(self.LeFr2, text='-', textvariable=self.selected_cluster_text)
        self.DoPaBu = tk.Button(self.LeFr2, text='Download Paper List', command=self.RunDoPa)
        self.DoPaTe = tk.Text(self.LeFr2, height=1, width=40)
        
        self.ShLaBu.grid(row=101, column=100, sticky=tk.W)
        self.ShPaBu.grid(row=102, column=100, sticky=tk.W)
        self.DoPaLa.grid(row=200, column=100, pady=(50, 0), sticky=tk.W)
        self.DoPaTe.grid(row=201, column=100, sticky=tk.W)
        self.DoPaBu.grid(row=202, column=100, sticky=tk.W)
        
        
    ### Functions
    ### Left side
    def LoDa(self):
        path = self.LoDaTe.get("1.0","end-1c")
        preculster_dict = pickle.load(open(path,'rb'))
        self.data['translation'] = preculster_dict['translation']
        self.data['translation_reverse'] = {y: x for x, y in self.data['translation'].items()}
        self.data['Gr'][0] = preculster_dict['graph']

    def ClickRa(self):
        self.selected_papers = []
        self.__DrawCavnas()
        self.CreateShLa()
        self.sel_row.set(0)
        
    def Plot(self, chart_nodes, intensity_list=False):
        fig = plt.figure(figsize=(7.5, 7.5))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        x_list = [x['coor'][0] for x in chart_nodes]
        y_list = [x['coor'][1] for x in chart_nodes]
        radii = [x['radius'] for x in chart_nodes]
        print(intensity_list)
        if intensity_list:
            color_list = [(0, 0, 1, (intensity_list[x] + 0.1)/2.0) for x in intensity_list]
        else:
            color_list = [(0, 0, 1, 0.4) for x in chart_nodes]
        print(color_list)
        min_max = {'min_x':0, 'max_x':0, 'min_y':0, 'max_y':0}
        for x, y, r, c in zip(x_list, y_list, radii, color_list):
            circle = mpatches.Circle((x, y), r, facecolor=c, edgecolor='k', linewidth=0.7)
            ax.add_patch(circle)
            min_max['min_x'] = min([min_max['min_x'], x - r])
            min_max['max_x'] = max([min_max['max_x'], x + r])
            min_max['min_y'] = min([min_max['min_y'], y - r])
            min_max['max_y'] = max([min_max['max_y'], y + r])
        ax.set_xlim(min_max['min_x'], min_max['max_x'])
        ax.set_ylim(min_max['min_y'], min_max['max_y'])
        for node in chart_nodes:
            ax.annotate(str(node['id'] + 1),
                        (node['coor'][0], node['coor'][1]))
        return fig

    def CreateClSo(self, intensity_list=False):
        if intensity_list:
            print(intensity_list)
            chart_nodes = self.data['nodes'][self.VaRa.get()]
            fig = self.Plot(chart_nodes, intensity_list=intensity_list)
        else:
            self.selected_papers = []
            if self.VaRa.get() == 0:
                self.__ClusterizeAllData()
            else:
                self.__DrillDown()
            fig = self.data['chart'][self.VaRa.get()]
        self.__DrawCavnas(fig)
        self.CreateShLa()
        self.sel_row.set(0)
        pickle.dump(self.data, open("test.p", "wb"))
        
    def QuerySearch(self):
        level = self.VaRa.get()
        query = self.QueryTe.get("1.0","end-1c")
        if query in self.data['translation_reverse']:
            query_no = self.data['translation_reverse'][query]
            frecuency = {}
            for i in self.data['cluster_info'][level]:
                if query_no in self.data['cluster_info'][level][i]['local_frequency']:
                    query_local_frequency = self.data['cluster_info'][level][i]['local_frequency'][query_no]
                    local_size = self.data['cluster_info'][level][i]['size']
                    frecuency[i] = {'query_local_frequency': query_local_frequency
                                   ,'local_size': local_size}
                else:
                    frecuency[i] = {'query_local_frequency': 0
                                   ,'local_size': 0}
            print(frecuency)
            normalized_frecuency = self.__FrecuencyNormalization(frecuency)
            print(normalized_frecuency)
            self.CreateClSo(intensity_list=normalized_frecuency)
        else:
            print('None')
    
    def __FrecuencyNormalization(self, frecuency):
        ratio_dict = {}
        for i in frecuency:
            if frecuency[i]['local_size'] == 0:
                ratio_dict[i] = 0
            else:
                ratio_dict[i] = float(frecuency[i]['query_local_frequency']) / frecuency[i]['local_size']
        max_ratio = max(ratio_dict.values())
        for i in ratio_dict:
            if ratio_dict[i] == 0:
                ratio_dict[i] = 0
            else:
                ratio_dict[i] = ratio_dict[i] / max_ratio
        return ratio_dict
    
    
    def __DrawCavnas(self, fig):
        self.Canvas.get_tk_widget().destroy()
        self.Canvas = FigureCanvasTkAgg(fig, master=self.LeFr1) 
        self.Canvas.draw()
        self.Canvas.get_tk_widget().grid(row=100, column=100, padx=10, pady=10, sticky=tk.W)
        
    def __ClusterizeAllData(self):
        self.VaRa.set(self.VaRa.get() + 1)
        QuCl = int(self.QuClTe.get("1.0", "end-1c"))
        Gr = self.data['Gr'][1] = self.data['Gr'][0]
        self.__ClusterizeSomeData(QuCl, Gr)

    def __DrillDown(self):
        QuCl = int(self.QuClTe.get("1.0","end-1c"))
        id_string = self.ClIdTe.get("1.0","end-1c")
        clusters_id_list = [int(x) for x in id_string.split(',')]
        partition = self.data['cluster_info'][self.VaRa.get()]
        clusters_nodes_list = [partition[cluster_id]['members']
                               for cluster_id in clusters_id_list]
        nodes = [node for cluster_nodes in clusters_nodes_list
                 for node in cluster_nodes]  # Learn this compress list function
        Gr = self.data['Gr'][self.VaRa.get()]
        sub_Gr = Gr.subgraph(nodes)
        self.VaRa.set(self.VaRa.get() + 1)
        self.VaRaText[self.VaRa.get()].set(id_string)
        self.data['Gr'][self.VaRa.get()] = sub_Gr
        self.data['ClId'][self.VaRa.get()] = id_string
        self.__ClusterizeSomeData(QuCl, sub_Gr)

    def __ClusterizeSomeData(self, QuCl, Gr):
        partition = My_clustering.ClusteringPipeline(QuCl, Gr)
        post_dict = My_post.PostDict(partition)
        level = self.VaRa.get()
        self.data['cluster_info'][level] = post_dict['cluster_info']
        self.data['nodes'][level] = post_dict['nodes']
        self.data['chart'][level] = self.Plot(self.data['nodes'][level])
        self.data['global_frequency'][level] = post_dict['global_frequency']
        self.data['labels'][level] = self.__GetLabels(self.data['cluster_info'][level],
                                                      self.data['global_frequency'][level])
        
    def __GetLabels(self, cluster_info, global_frequency):
        labels = {}
        for i in cluster_info:
            labels[i] = str(cluster_info[i]['id']) + ': ' + str(cluster_info[i]['size'])
            score_list = []
            for j in cluster_info[i]['local_frequency']:
                if j in global_frequency:
                    score = cluster_info[i]['local_frequency'][j] / (global_frequency[j]+25)
                    score_list.append((j, score))
                else:
                    score_list.append((j, 0))
            score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
            for k in [x[0] for x in score_list[:4]]:
                labels[i] += ' | ' + self.data['translation'][k]
        return labels
        
    ### Right side
    def CreateShLa(self):
        self.enviroment.set('labels')
        self.selected_papers = []
        self.LiBo.delete(0, tk.END)
        level = self.VaRa.get()
        if level != 0:
            for i in self.data['labels'][level]:
                self.LiBo.insert(tk.END, self.data['labels'][level][i])

    def CreateShPa(self):
        if self.enviroment.get() == 'labels':
            self.enviroment.set('papers')
            VaRa = self.VaRa.get()
            nodes = self.data['cluster_info'][VaRa][self.sel_row.get() + 1]['members']
            sub_Gr = self.data['Gr'][VaRa].subgraph(nodes)
            node_list = [node for node in sub_Gr.vs]
            sorted_list = sorted(node_list, reverse=True,
                                 key=lambda x: x['n_cits'])
            self.selected_papers = sorted_list
            self.LiBo.delete(0, tk.END)
            for node in sorted_list[: self.show_x_papers]:
                self.LiBo.insert(tk.END, str(int(node['pub_year']))
                                            + ' | ' + str(node['n_cits'])
                                            + ' | ' + node['ti']
                                            + ' | ' + node['source'])
    
    def ClickListbox(self, event):
        if self.VaRa.get() == 0:
            self.enviroment.set('all_data')
        if self.enviroment.get() == 'labels':
            event_widget = event.widget
            self.sel_row.set(event_widget.curselection()[0])
            self.selected_cluster.set(self.sel_row.get() + 1)
            self.selected_cluster_text.set('Selected cluster ' + str(self.selected_cluster.get())
                                           + ' from clustering ' + str(self.VaRa.get()))

    def RunDoPa(self):
        if self.selected_cluster.get() == None:
            self.selected_cluster_text.set('Please select a cluster')
        else:
            file_name = self.DoPaTe.get("1.0", "end-1c")
            VaRa = self.VaRa.get()
            nodes = self.data['cluster_info'][VaRa][self.selected_cluster.get()]['members']
            sub_Gr = self.data['Gr'][VaRa].subgraph(nodes)
            node_list = [node for node in sub_Gr.vs]
            sorted_list = sorted(node_list, reverse=True,
                                 key=lambda x: x['n_cits'])
            papers_list = self.__CreateListPapers(sorted_list)
            self.__WriteListOfList(file_name, papers_list)
            
    def __CreateListPapers(self, sorted_list):
        papers_list = [['ti', 'pub_year',
                          'author_first',
                          'author_et_al',
                          'source', 'de',
                          'id', 'doi',
                          'n_cits']]
        for i in sorted_list:
            paper_data = [i['ti'], i['pub_year'],
                          i['author_first'],
                          i['author_et_al'],
                          i['source'], i['de'],
                          i['id'], i['doi'],
                          i['n_cits']]
            papers_list.append(paper_data)
        return papers_list

    def __WriteListOfList(self, file_name, items_list):
        file_string = ''
        for i in items_list:
            for j in i:
                file_string += str(j) + '\t'
            file_string += str(j) + '\n'
        with open(file_name, 'w') as f:
            f.write(file_string[:-1])