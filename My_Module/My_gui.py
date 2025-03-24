from My_Module import My_pre_clustering
from My_Module import My_clustering
from My_Module import My_post
import pickle
import tkinter as tk
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def execute_downloading_gui():
    root = tk.Tk()
    downloading_gui(root)
    root.mainloop()

def execute_clustering_gui():
    root = tk.Tk()
    clustering_gui(root)
    root.mainloop()
    
class downloading_gui:
    # Obly uses the My_pre_clustering module
    # UsNa = User Name
    # ClLe = Cluster Level
    # ClId = Cluster ID
    # FiNa = File Name
    # Do = Download
    def __init__(self, root):
        self.root = root
        self.Fr1 = tk.Frame(self.root)  # <FRAME 1>
        self.Fr1.pack(side=tk.TOP, anchor=tk.W)
        self.UsNaLa = tk.Label(self.Fr1, text="User Name")
        self.UsNaLa.pack(side=tk.LEFT, anchor=tk.W)
        self.UsNaTe = tk.Text(self.Fr1, height=1, width=20)
        self.UsNaTe.pack(side=tk.LEFT, anchor=tk.W)  # </FRAME 1>
        self.Fr2 = tk.Frame(self.root)  # <FRAME 2>
        self.Fr2.pack(side = tk.TOP, anchor=tk.W)
        self.ClLeLa = tk.Label(self.Fr2, text="Cluster Level")
        self.ClLeLa.pack(side = tk.LEFT, anchor=tk.W)
        self.ClLeTe = tk.Text(self.Fr2, height=1, width=20)
        self.ClLeTe.pack(side = tk.LEFT, anchor=tk.W)  # </FRAME 2>
        self.Fr3 = tk.Frame(self.root)  # <FRAME 3>
        self.Fr3.pack(side=tk.TOP, anchor=tk.W)
        self.ClIdLa = tk.Label(self.Fr3, text="Cluster ID")
        self.ClIdLa.pack(side=tk.LEFT, anchor=tk.W)
        self.ClIdTe = tk.Text(self.Fr3, height=1, width=20)
        self.ClIdTe.pack(side=tk.LEFT, anchor=tk.W)  # </FRAME 3>
        self.Fr4 = tk.Frame(self.root)  # <FRAME 4>
        self.Fr4.pack(side=tk.TOP, anchor=tk.W)
        self.FiNaLa = tk.Label(self.Fr4, text="File Name")
        self.FiNaLa.pack(side=tk.LEFT, anchor=tk.W)
        self.FiNaTe = tk.Text(self.Fr4, height=1, width=20)
        self.FiNaTe.pack(side=tk.LEFT, anchor=tk.W)  # </FRAME 4>
        self.Fr5 = tk.Frame(self.root)  # <FRAME 5>
        self.Fr5.pack(side=tk.TOP, anchor=tk.W)
        self.Do = tk.Button(self.Fr5, text="Download", command=self.download)
        self.Do.pack(side=tk.LEFT, anchor=tk.W)  # </FRAME 5>

    def download(self):
        UsNa = self.UsNaTe.get("1.0", "end-1c")
        ClLe = int(self.ClLeTe.get("1.0", "end-1c"))
        ClId = int(self.ClIdTe.get("1.0", "end-1c"))
        FiNa = self.FiNaTe.get("1.0", "end-1c")
        precluster_dict = My_pre_clustering.Run(UsNa, ClLe, ClId)
        pickle.dump(precluster_dict, open(FiNa, 'wb'))

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
        self.data = {'translation': None, 'Gr': {},
                     'chart': {}, 'info': {}}
        self.data['Gr'][0] = None
        self.data['chart'][0] = mpl.figure.Figure(figsize=(7.5, 7.5))
        self.data['info'][0] = False
        self.root = root
        root.title('Interative Search Tool')
        self.VaRa = tk.IntVar()
        self.VaRa.set(0)
        self.fig = self.data['chart'][self.VaRa.get()]
        self.s_row = tk.IntVar()
        self.s_row.set(0)
        self.enviroment = tk.StringVar()
        self.enviroment.set('all_data')
        #### GUI
        self.LeFr = tk.Frame(self.root)
        self.LeFr.pack(side=tk.LEFT)
        self.LeFr0 = tk.Frame(self.LeFr)
        self.LeFr0.pack(side=tk.TOP, anchor=tk.W)
        self.LoDaTe = tk.Text(self.LeFr0, height=1, width=40)
        self.LoDaTe.pack(side = tk.LEFT, anchor=tk.W)
        self.LoDaBu = tk.Button(self.LeFr0, text='Load', command=self.LoDa)
        self.LoDaBu.pack(side=tk.LEFT, anchor=tk.W)
        self.LeFr1 = tk.Frame(self.LeFr)
        self.LeFr1.pack(side = tk.TOP)
        self.LeFr1Ri = tk.Frame(self.LeFr1)
        self.LeFr1Ri.pack(side=tk.RIGHT, anchor=tk.N)
        self.Canvas = FigureCanvasTkAgg(self.fig, master=self.LeFr1Ri)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        self.LeFr1Le = tk.Frame(self.LeFr1)
        self.LeFr1Le.pack(side=tk.LEFT, anchor=tk.N)
        self.Ra0 = tk.Radiobutton(self.LeFr1Le, text='All Data',
                                  variable=self.VaRa, value=0,
                                  command=self.ClickRa)
        self.Ra0.pack(anchor=tk.W)
        for i in range(1, 11):
            self.RaX = tk.Radiobutton(self.LeFr1Le,
                                      text='Clustering ' + str(i),
                                      variable=self.VaRa, value=i,
                                      command=self.ClickRa)
            self.RaX.pack(anchor=tk.W)
        self.LeFr2 = tk.Frame(self.LeFr)
        self.LeFr2.pack(side=tk.TOP, anchor=tk.W)
        self.LeFrLe = tk.Frame(self.LeFr2)
        self.LeFrLe.pack(side=tk.LEFT, anchor=tk.N)
        self.QuClLa = tk.Label(self.LeFrLe, text='Q Clusters')
        self.QuClLa.pack(anchor=tk.W)
        self.QuClTe = tk.Text(self.LeFrLe, height=1, width=3)
        self.QuClTe.pack(anchor=tk.W)
        self.LeFr2Ri = tk.Frame(self.LeFr2)
        self.LeFr2Ri.pack(side=tk.RIGHT, anchor=tk.N)
        self.ClIdLa = tk.Label(self.LeFr2Ri, text='Clusters ID')
        self.ClIdLa.pack(anchor=tk.E)
        self.ClIdTe = tk.Text(self.LeFr2Ri, height=1, width=40)
        self.ClIdTe.pack(anchor=tk.E)
        self.LeFr3 = tk.Frame(self.LeFr)
        self.LeFr3.pack(side=tk.TOP, anchor=tk.W)
        self.ClSoBu = tk.Button(self.LeFr3, text='Create clustering solution',
                                command=self.CreateClSo)
        self.ClSoBu.pack()
        self.RiFr = tk.Frame(self.root)
        self.RiFr.pack(side=tk.RIGHT, anchor=tk.N)
        self.RiFr1 = tk.Frame(self.RiFr)
        self.RiFr1.pack(side=tk.TOP)
        self.ScrollY = tk.Scrollbar(self.RiFr1, orient='vertical')
        self.ScrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.ScrollX = tk.Scrollbar(self.RiFr1, orient='horizontal')
        self.ScrollX.pack(side=tk.BOTTOM, fill=tk.X)
        self.Listbox = tk.Listbox(self.RiFr1,
                                  yscrollcommand=self.ScrollY.set,
                                  xscrollcommand=self.ScrollX.set,
                                  height=35, width=80,
                                  font=('Courier New', '15'),
                                  activestyle='none')
        self.Listbox.bind('<<ListboxSelect>>', self.on_select_label)
        self.Listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.ScrollY.config(command=self.Listbox.yview)
        self.ScrollX.config(command=self.Listbox.xview)
        self.RiFr2 = tk.Frame(self.RiFr)
        self.RiFr2.pack(side=tk.BOTTOM, anchor=tk.S)
        self.ShLaBu = tk.Button(self.RiFr2, text='Show Labels',
                                command=self.CreateShLa)
        self.ShLaBu.pack(side=tk.LEFT, anchor=tk.S)
        self.ShPaBu = tk.Button(self.RiFr2, text='Show Paper List',
                                command=self.CreateShPa)
        self.ShPaBu.pack(side=tk.LEFT, anchor= tk.S)
        self.DoPaBu = tk.Button(self.RiFr2, text='Download Paper List',
                                command=self.RunDoPa)
        self.DoPaBu.pack(side=tk.LEFT, anchor=tk.S)
        self.DoPaTe = tk.Text(self.RiFr2, height=1, width=40)
        self.DoPaTe.pack(side=tk.LEFT, anchor=tk.S)

    ### Functions
    ### Left side
    def LoDa(self):
        path = self.LoDaTe.get("1.0","end-1c")
        preculster_dict = pickle.load(open(path,'rb'))
        self.data['translation'] = preculster_dict['translation_dict']
        self.data['Gr'][0] = preculster_dict['G']

    def ClickRa(self):
        self.selected_papers = list()
        self.draw_cavnas()
        self.CreateShLa()
        self.s_row.set(0)

    def draw_cavnas(self):
        self.Canvas.get_tk_widget().destroy()
        self.fig = self.data['chart'][self.VaRa.get()]
        self.Canvas = FigureCanvasTkAgg(self.fig,
                                        master=self.LeFr1Ri) 
        self.Canvas.draw()
        self.Canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

    def Plot(self,chart_nodes):
        fig = mpl.figure.Figure(figsize=(7.5, 7.5))
        ax = fig.add_axes([0, 0, 1, 1])
        x_list = [x['coor'][0] for x in chart_nodes]
        y_list = [x['coor'][1] for x in chart_nodes]
        radii = [x['radius']  for x in chart_nodes]
        min_max = {'min_x':0, 'max_x':0, 'min_y':0, 'max_y':0}
        patches = []
        for x, y, r in zip(x_list, y_list, radii):
            circle = Circle((x, y), r)
            patches.append(circle)
            min_max['min_x'] = min([min_max['min_x'], x - r])
            min_max['max_x'] = max([min_max['max_x'], x + r])
            min_max['min_y'] = min([min_max['min_y'], y - r])
            min_max['max_y'] = max([min_max['max_y'], y + r])
        p = PatchCollection(patches, alpha=0.4)
        ax.add_collection(p)
        ax.set_xlim(min_max['min_x'], min_max['max_x'])
        ax.set_ylim(min_max['min_y'], min_max['max_y'])
        for node in chart_nodes:
            ax.annotate(str(node['id'] + 1),
                        (node['coor'][0], node['coor'][1]))
        return fig

    def CreateClSo(self):
        self.selected_papers = list()
        if self.VaRa.get() == 0:
            self.clusterize_all_data()
        else:
            self.drill_down()
        self.draw_cavnas()
        self.CreateShLa()
        self.s_row.set(0)

    def clusterize_all_data(self):
        self.VaRa.set(self.VaRa.get() + 1)
        QuCl = int(self.QuClTe.get("1.0", "end-1c"))
        Gr = self.data['Gr'][1] = self.data['Gr'][0]
        self.clusterize(QuCl, Gr)

    def drill_down(self):
        QuCl = int(self.QuClTe.get("1.0","end-1c"))
        id_string = self.ClIdTe.get("1.0","end-1c")
        clusters_id_list = [int(x) for x in id_string.split(',')]
        partition = self.data['info'][self.VaRa.get()]
        clusters_nodes_list = [partition[cluster_id]['members']
                               for cluster_id in clusters_id_list]
        nodes = [node for cluster_nodes in clusters_nodes_list
                 for node in cluster_nodes]  # Learn this compress list function
        Gr = self.data['Gr'][self.VaRa.get()]
        sub_Gr = Gr.subgraph(nodes)
        self.data['Gr'][self.VaRa.get() + 1] = sub_Gr
        self.VaRa.set(self.VaRa.get() + 1)
        self.clusterize(QuCl, sub_Gr)

    def clusterize(self, QuCl, Gr):
        partition = My_clustering.clustering_pipeline(QuCl, Gr)
        post_dict = My_post.post_dict(partition, self.data['translation'])
        data_dict = dict()
        for i in post_dict['info']:
            data_dict[i['id']] = i
            data_dict[i['id']]['members'] = partition[i['id'] - 1]
        self.data['info'][self.VaRa.get()] = data_dict
        self.data['chart'][self.VaRa.get()] = self.Plot(post_dict['nodes'])

    ### Right side
    def CreateShLa(self):
        self.enviroment.set('labels')
        self.selected_papers = list()
        self.Listbox.delete(0, tk.END)
        if self.VaRa.get() != 0:
            for cluster in self.data['info'][self.VaRa.get()]:
                cluster_dict = self.data['info'][self.VaRa.get()][cluster]
                self.Listbox.insert(tk.END,str(cluster_dict['id'])
                                    + ': ' + str(cluster_dict['size'])
                                    + ' | ' + cluster_dict['keywords'][0]
                                    + ' | ' + cluster_dict['keywords'][1]
                                    + ' | ' + cluster_dict['keywords'][2]
                                    + ' | ' + cluster_dict['keywords'][3])

    def on_select_label(self, event):
        if self.VaRa.get() == 0:
            self.enviroment.set('all_data')
        if self.enviroment.get() == 'labels':
            event_widget = event.widget
            self.s_row.set(event_widget.curselection()[0])

    def CreateShPa(self):
        if self.enviroment.get() == 'labels':
            self.enviroment.set('papers')
            VaRa = self.VaRa.get()
            nodes = self.data['info'][VaRa][self.s_row.get() + 1]['members']
            sub_Gr = self.data['Gr'][VaRa].subgraph(nodes)
            node_list = [node for node in sub_Gr.vs]
            sorted_list = sorted(node_list, reverse=True,
                                 key=lambda x: x['n_cits'])
            self.selected_papers = sorted_list
            self.Listbox.delete(0, tk.END)
            for node in sorted_list[: self.show_x_papers]:
                self.Listbox.insert(tk.END, str(int(node['pub_year']))
                                            + ' | ' + str(node['n_cits'])
                                            + ' | ' + node['ti']
                                            + ' | ' + node['source'])

    def RunDoPa(self):
        if self.enviroment.get() == 'papers':
            file_name = self.DoPaTe.get("1.0", "end-1c")
            print(self.selected_papers[0])
            pass 