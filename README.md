# QHF - Quantitative Habitability Framework

This is the repository of the QHF python framework developed as an illustration for the Quantitative Habitability Framework (QHF). 
QHF was developed by the NASA Nexus for Exoplanet System Science (NExSS) research coordinator network's Quantitative Habitability Science Working group (SWG), co-chaired by Dr. Daniel Apai and Dr. Rory Barnes. 

The QHF framework and example uses of this python implementation are published in:
Apai, Barnes, Murphy et al. 2025 Planetary Science Journal "A Terminology and Quantitative Framework for Assessing the Habitability of Solar System and Extraterrestrial Worlds" 

The latest version of QHF can be found on GitHub: github.com/danielapai/QHF/

-------------------------------------------------------------------------------------------------------
Overview:

QHF is a statistical comparison of a habitat model and a metabolism (organism) model. The former provides predictions for the conditions in the potential habitat; the latter predicts whether the organism is viability under specific conditions. During each run, QHF evaluates the compatibility of the predicted habitat conditions and the organisms' needs through Monte Carlo iterations. The results of the MC iterations are visualized in scatter plots and distribution plots. The ratio of the viable/non-viable outcomes provides a probabilistic assessment of the modeled organisms' viability in the modeled habitat.

Use:
QHF was designed to be modular. 
Habitat models are provided in the Habitats/ directory.
Metabolism/Organism models are provided in the Metabolisms/ directory.
The main QHF.py framework is ideally not modified for individual uses. Instead, the habitat and metabolism modules may be adopted for specific use cases, and global parameters are adjusted in a configuration file that is specified as a command line argument at execution.

For example: python QHF.py trappist1e.cfg


Note on graph visualization:
1) The habitat modules commonly consist of a sequence of interconnected functions. For example, the orbital elements and mass of a planet may influence its equilibrium temperature and atmospheric composition, which may then influence its surface pressure, etc. 
The interdependence of such modules are captured as a self-generated graph. 
The graph is automatically generated and works robustly for non-cyclical graphs. The approach does not work for cyclical situations (e.g., atmospheric pressure influences albedo which influences the temperature which influences the atmospheric pressure). Such uses are not currently possible with QHF but may be implemented with minor modifications.

2) The graph visualization uses a standard python library. When there are many nodes in the graph with longer node names, it is likely that some of them may overlap. To avoid overlaps, users may want to re-run the graph generation part of the QHF multiple times (arrangement of nodes is somewhat random) and select the desired version. Alternatively, the graphs saved in .png can be imported, for example, in Adobe Illustrator and the overlapping objects can be shifted by hand.


-------------------------------------------------------------------------------------------------------
Example execution:
python QHF.py trappist1e.cfg
-------------------------------------------------------------------------------------------------------
Acknowledgements: The development of QHF was directly supported by the Alien Earths project funded by the NASA ICAR program.
