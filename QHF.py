import sys, os
sys.path.append('./Habitats')
sys.path.append('./Metabolisms')
sys.path.append('./Analyses')
from collections import defaultdict
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.patches as patches
import importlib
import configparser # For handling of a configuration file
import pdb # Python debugger
import keyparams
from mcmodules import Module as Module
from layout_presets import presets, label_offsets



#======================================
# Program flow:
# 1) Configure/load modules
# 2) Translate connections between modules to graph
# 3) Visualize Graph
# 4) Apply topological sorting to graph
# 5) Evaluate vertices following the sorted graph
# 6) Analyze results
# 7) Visualize and save results
#======================================



#===================================================
# Daniel Apai: We represent the connections between the modules as a graph, where each
# vertex is a module, and each edge represents a dependency (parameters passed).
# Once encoded as a graph, we apply a basic topological sorting to identify The
# order in which the vertices can be evaluated.
#

#================================================================
# Build and Visualize the Graph
# Based on https://www.geeksforgeeks.org/visualize-graphs-in-python/


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b, label):
        self.visual.append([a, b])

    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)

        # Choose layout spacing and pull offsets for current config
        preset_name = HabitatShortName.lower()
        offset_dict = presets.get(preset_name, {})
        label_dict = label_offsets.get(preset_name, {})

        # Spread out graph layout
        pos = nx.spring_layout(G, seed=42, k=0.7, scale = 3.0, iterations=150)
        for node, label in mod_labels.items():
            normalized_label = label.replace('\n', ' ').strip()
            x, y = pos[node]
            dx, dy = offset_dict.get(label, (0.00, 0.00))
            pos[node] = (x + dx, y + dy)

        # Node color logic
        node_colors = [
            prior_node_color if len(Modules[node].input_parameters) == 0 else
            metabolism_node_color if 'Suitability' in Modules[node].output_parameters else
            other_node_color for node in G
        ]

        node_size_val = 12 * sf  # Unified box size

        # Draw background layers if screen is True
        if screen:
            nx.draw_networkx(G, pos, arrows=False, arrowsize=3.0 * sf, with_labels=False,
                            width=3 * sf, alpha=0.02, edge_color=selected_edgecolor,
                            node_color="white", node_size=70 * sf)
            nx.draw_networkx(G, pos, arrows=False, arrowsize=3.0 * sf, with_labels=False,
                            width=2 * sf, alpha=0.05, edge_color=selected_edgecolor,
                            node_color=node_colors, node_size=50 * sf)

        # Main network draw
        nx.draw_networkx(G, pos, arrows=True, arrowsize=3.0 * sf, with_labels=False,
                        width=0.5 * sf, alpha=0.7, edge_color=selected_edgecolor,
                        node_color=node_colors, node_size=node_size_val)

        # Edge label cleanup
        for idx, varlabel_key in enumerate(edge_labels):
            if edge_labels[varlabel_key] == 'Surface Temperature':
                edge_labels[varlabel_key] = 'Temperature'
            elif edge_labels[varlabel_key] == 'Surface Pressure':
                edge_labels[varlabel_key] = 'Pressure'

        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            label_pos=0.4,
            rotate=False,
            font_color=selected_edgecolor,
            font_size=1.6 * sf,
            font_weight='light',
            bbox=dict(alpha=0.2, fc=bkgcolor, ec=labelcolor, linewidth=0.1 * sf),
            clip_on=True
        )

        # Label placement (below or offset per label)
        pos_upper = {}
        for k, v in pos.items():
            label = mod_labels[int(k)]
            pos_upper[k] = (v[0], v[1] + 0.05)  # small diagonal offset

        nx.draw_networkx_labels(G, pos_upper, mod_labels,
                                font_size=1.8 * sf, font_color=labelcolor,
                                font_weight='light', horizontalalignment='center',verticalalignment="bottom")

        plt.title('Connections between Modules', color=labelcolor, fontsize=5,
                bbox=dict(alpha=0.1, fc=bkgcolor, ec=bkgcolor, linewidth=0.))
        plt.axis("off")
        ax = plt.gca()

        if screen:
            rect = patches.Rectangle((0., 0.), 1., 1., linewidth=0.2,
                                    edgecolor='lightblue', facecolor='none',
                                    transform=ax.transAxes)
            ax.add_patch(rect)

        return ax



# Examples for networkx plots:
# https://networkx.org/documentation/latest/auto_examples/index.html


#================================================================
# Main code starts here

#=================================================================
# LOAD CONFIGURATION FILE

# load in from command line
cl_args = sys.argv
# This reads anything after 'python' as CL args, so the intended indices are:
# 0 = name of this MC script (i.e. what's being 'python'ed)
# 1 = name/path to configuration file
config_file_path = str(cl_args[1])

config = configparser.ConfigParser()

# For documentation on the ConfigParser, see https://docs.python.org/3/library/configparser.html

config.read(config_file_path)
ConfigID = config['Configuration']['ConfigID']


# read in user input on modules
HabitatFile = config['Habitat']['HabitatFile']
#HabitatFile = os.path.splitext(HabitatFile)[0] # this line removes any .py extension from specified file, which messes up the module import
HabitatModule = config['Habitat']['HabitatModule']
HabitatLogo = config['Habitat']['HabitatLogo']
HabitatShortName = config['Habitat']['HabitatShortname']

MetabolismFile = config['Metabolism']['MetabolismFile']
MetabolismFile = os.path.splitext(MetabolismFile)[0] # this removes any .py extension
MetabolismModule = config['Metabolism']['MetabolismModule']

VisualizationFile = config['Visualization']['VisualizationFile']
VisualizationFile = os.path.splitext(VisualizationFile)[0] # this removes any .py extension
VisualizationModule = config['Visualization']['VisualizationModule']


NumProbes = config['Sampling']['NumProbes']
if float(NumProbes) > 1e8:
    print('### Warning: Number of Probes limited -- change QHF code if you need more probes.')
NumProbes = np.clip(float(NumProbes), 1, 1e8)

print(' [ Configuration file: ]', ConfigID)
print(' [ Habitat Module: ]', HabitatModule)
print(' [ Metabolism Module: ]', MetabolismModule)
print(' [ Visualization Module: ]', VisualizationModule)


#===================================================================
# IMPORT MODULES
#===================================================================

habitat_file = __import__(HabitatFile)
habitat_module_load = getattr(habitat_file, str(HabitatModule))
Modules = habitat_module_load()

metabolism_file = __import__(MetabolismFile)
metabolism_module_load = getattr(metabolism_file, str(MetabolismModule))
ModuleHabitability = metabolism_module_load()

# Combine the habitat and organism models into a single array of modules:
Modules.append(ModuleHabitability)
# Determine the total number of modules loaded
nmods = len(Modules)

visualization_file = __import__(VisualizationFile)
VisualizationModule = getattr(visualization_file, str(VisualizationModule))
#= habitat_module_load()

#from visexoplanet import *


#=================================================================
print('[Modules Loaded]')
for mi in np.arange(nmods):
    print(mi, ' : ', Modules[mi].name)


#=================================================================
# Set up plotting choices: on-screen (dark theme) or paper (white background)

#screen = True
screen = False

# Define two plotting modes, one for screen, one for articles
if screen:
    # Scaling factor
    sf = 1.0
    bkgcolor='#030810'
    selected_edgecolor='white'
    prior_node_color='blue'
    other_node_color='lightblue'
    metabolism_node_color='green'
    labelcolor='lightblue'
    labeloffset=0.0
else:
    bkgcolor='white'
    # Scaling factor
    sf = 1.3
    selected_edgecolor='darkblue'
    prior_node_color='red'
    other_node_color='blue'
    metabolism_node_color='green'
    labelcolor='black'
    labeloffset=-0.05



#================================================
# Translate the module list into a graph, where edges represent input/output connections
# between the vertices (out MC modules)

G = GraphVisualization()
edge_labels = {}

#============================
# Determine the order of evaluation for the graph through a topological sorting
# This will only work for acyclical graphs, i.e., no infinite loops
# =====================================

mod_labels={}

for jj in np.arange(nmods):
    mod_labels[int(jj)]=Modules[jj].name
    print('--------------------------------------------------------------------------------')
    print('Identifying input connections for module ', Modules[jj].name)

    for ip in Modules[jj].input_parameters:
# For each input parameter, find all modules with matching output parameters:
        print('......................................................................')
        print('Scanning for output parameters matching the input parameter:', ip)

        # Cycle through all modules:
        for module_scanned in np.arange(nmods):

            # Check if the input parameter matches the output parameters of the given module:
            if any(x == ip for x in Modules[module_scanned].output_parameters): #<<< Example
                print(' + Input/output Match found in module: ', Modules[module_scanned].name)
                G.addEdge(module_scanned,jj,label=ip.replace('_',' '))
                edge_labels[(module_scanned,jj)]=ip.replace('_',' ')


#============================
# Determine the order of evaluation for the graph through a topological sorting
# This will only work for acyclical graphs, i.e., no infinite loops
# =====================================

print("The Topological Sort Of The Graph Is:  ")

DG = nx.DiGraph()
DG.add_edges_from(G.visual)
topsorted = list(nx.topological_sort(DG))
print(topsorted)   # Array of topologically sorted module numbers. Key to Monte Carlo realization.


# ==========================================================
# Now execute Monte Carlo realization of the Module chain
# ==========================================================

N_iter = HabitatFile = int(config['Sampling']['Niterations']) # Number of Monte Carlo iterations, as specified in the configuration file

Suitability_Distribution = []
Temperature_Distribution = []
Pressure_Distribution = []
BondAlbedo_Distribution = []
GreenHouse_Distribution = []
Depth_Distribution = []
SavedParameters = []

N_probes = 100

Suitability_Plot = []
Variable = []

# If there is a parameter to study
for keyparams.ProbeIndex in np.arange(float(NumProbes)):  # Index of the parameter space locations to sample. This value is passed on to every module.
    print('Probing location ', keyparams.ProbeIndex)
# Monte Carlo loop itself:
    for ii in np.arange(N_iter):      # Number of iterations
        keyparams.runid=''
        for mi in np.arange(len(topsorted)):     # Step through and executed the modules in the topologically sorted order
            # Execute
            print('Executing ',Modules[topsorted[mi]].name)
            Modules[topsorted[mi]].execute()

        Suitability_Distribution.append(keyparams.Suitability)
        #Temperature_Distribution.append(keyparams.Surface_Temperature)
        Temperature_Distribution.append(keyparams.Temperature)
        BondAlbedo_Distribution.append(keyparams.Bond_Albedo)
        GreenHouse_Distribution.append(keyparams.GreenhouseWarming)
        Pressure_Distribution.append(keyparams.Pressure)
        Depth_Distribution.append(keyparams.Depth)
        runid = keyparams.runid

    print('Monte Carlo loop completed')
    print('Runid: ' + keyparams.runid)
    This_Suitability = np.mean(Suitability_Distribution)
    print('Average Suitability %.2f' % This_Suitability)
    Suitability_Plot.append(This_Suitability)
    Variable.append(keyparams.Depth)
    SavedParameters.append(keyparams)

# ==============================
# Now visualize the graph to allow verification of the connections
# ==============================
node_colors=[]
node_sizes={}



fig=plt.figure(figsize=(12.00, 8.00), dpi=300)
fig.set_facecolor(bkgcolor)
fig.set_edgecolor(selected_edgecolor)
# Add frame:
ax = G.visualize()
#plt.text(0.02,0.02, 'Average Suitability %.2f' % np.mean(Suitability_Distribution),fontsize=4*sf,color=labelcolor,transform=ax.transAxes)

# Add habitat logo
im = plt.imread(HabitatLogo)
newax = fig.add_axes([0.75, 0.75, 0.10, 0.10], anchor='NE')
newax.set_axis_off()
newax.imshow(im)
fig.savefig('Figures/'+HabitatShortName+'_Connections.png')
fig.savefig('Figures/'+HabitatShortName+'_Connections.svg') # vector format
plt.show()

#========================================================
# Visualization of the Results
VisualizationModule(screen,sf,Suitability_Distribution,Temperature_Distribution,BondAlbedo_Distribution,GreenHouse_Distribution,Pressure_Distribution,Depth_Distribution, keyparams.runid,Suitability_Plot,Variable,HabitatLogo)
