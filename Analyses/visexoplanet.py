import keyparams
import matplotlib.pyplot as plt
import numpy as np
import math

def QHFvisualize(screen,sf,Suitability_Distribution,Temperature_Distribution,BondAlbedo_Distribution,GreenHouse_Distribution,Pressure_Distribution,Depth_Distribution,runid,Suitability_Plot,Variable):

    if screen:
        # Scaling factor
        sf = 1.0
        bkgcolor='#030810'
        selected_edgecolor='white'
        prior_node_color='blue'
        other_node_color='lightblue'
        labelcolor='lightblue'
        labeloffset=0.0
    else:
        bkgcolor='white'
        # Scaling factor
        sf = 1.3
        selected_edgecolor='darkblue'
        prior_node_color='red'
        other_node_color='blue'
        labelcolor='black'
        labeloffset=-0.05

    ax = plt.axes(projection='3d')#,figsize=(4.00, 2.00), dpi=400)
    ax.scatter3D(Temperature_Distribution, Pressure_Distribution, Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=0.7,alpha=0.5);
    if screen: ax.scatter3D(Temperature_Distribution, Pressure_Distribution, Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=4.9,alpha=0.1);
    ax.set_xlabel('Surface Temperature [K]')
    #ax.set_xrange(220,450)
    ax.axes.set_xlim3d(left=220, right=450)
    ax.set_ylabel('Surface Pressure [bar]')
    ax.set_zlabel('Habitat Suitability')
    ax.set_title(keyparams.runid + ' | S = %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor)
    #ax.text(0.02,0.02,0.02, 'Average Suitability %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor,transform=ax.transAxes)
    plt.show()


    breakpoint()

    # Multi-plot showing distributions of key parameters
    # This will need to be optimizable from the module loaded, but now I specify the parameters

    fig=plt.figure(figsize=(4.00, 2.00), dpi=400)
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].hist(Temperature_Distribution,bins=np.clip(math.floor(N_iter/60.), 5, 30))
    axs[0, 0].set_title('Surface Temp. [K]')
    #axs[0,0].set(xlabel='[K]', ylabel='y-label')
    axs[0, 1].hist(Pressure_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    axs[0, 1].set_title('Surface Pressure [bar]')
    axs[1, 0].hist(BondAlbedo_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    axs[1, 0].set_title('Bond Albedo')
    axs[1, 1].hist(GreenHouse_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    axs[1, 1].set_title('Greenhouse Warming [K]')
    fig.tight_layout()

    #for ax in axs.flat:
    #    ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    #for ax in axs.flat:
    #    ax.label_outer()
    plt.show()


    return
