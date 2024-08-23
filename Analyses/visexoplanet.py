import keyparams
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats

#(screen,sf,Suitability_Distribution,Temperature_Distribution,BondAlbedo_Distribution,GreenHouse_Distribution,Pressure_Distribution,runid):
def QHFvisualize(screen,sf,Suitability_Distribution,Temperature_Distribution,BondAlbedo_Distribution,GreenHouse_Distribution,Pressure_Distribution,Depth_Distribution, runid,Suitability_Plot,Variable,HabitatLogo):
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
    fig = ax.get_figure()
    fig.set_size_inches(8, 8)
    if screen: ax.scatter3D(Temperature_Distribution, Pressure_Distribution, Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=4.9,alpha=0.1);
    ax.set_xlabel('Surface Temperature [K]')
    #ax.set_xrange(220,450)
    ax.axes.set_xlim3d(left=220, right=450)
    ax.set_ylabel('Surface Pressure [bar]')
    ax.set_zlabel('Habitat Suitability')
    ax.set_title(keyparams.runid + ' | S = %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor)
    #ax.text(0.02,0.02,0.02, 'Average Suitability %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor,transform=ax.transAxes)

    # Add logo of the habitat
    im = plt.imread(HabitatLogo)
    newax = fig.add_axes([0.75, 0.55, 0.15, 0.15], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)


    #fig.tight_layout()
    fig.savefig('Figures/'+keyparams.runid+'_HS-Pressure-Temperature.png')
    plt.show()


    #breakpoint()

    # Multi-plot showing distributions of key parameters
    # This will need to be optimizable from the module loaded, but now I specify the parameters
    
    ## For now, hard-coding what is/isn't a prior!!
    
    ## for parameters with a cut-off, the build-up at the cut-off messes up the automatically-drawn axes limits
    ##    so, define a way to set y-limit based on the height of the distribution at its median


    nbins=np.floor(len(Temperature_Distribution)/30.).astype(int)
    print(nbins)
    #fig=plt.figure(figsize=(6.00, 2.00), dpi=400)
    fig, axs = plt.subplots(2, 2,constrained_layout=True,figsize=(12.00, 4.00))
    N_iter = 100.
    #axs[0, 0].hist(Temperature_Distribution) #,bins=np.clip(math.floor(N_iter/60.), 5, 30))
    
    # surface temperature is a RESULT
    counts, bins = np.histogram(Temperature_Distribution, bins=nbins)
    axs[0, 0].text(0.8, 0.8, 'Result', c='blue', transform=axs[0,0].transAxes, fontsize=12)
    axs[0, 0].stairs(counts, bins, fill=1)
    axs[0, 0].set_xlabel('Surface Temp. [K]')
    axs[0, 0].set_ylim(0, np.sort(counts)[-2]+10) # set y-limit based on 2nd-highest bin height + buffer to prevent build-ups at cutoff from messing with default y-limit
    #axs[0,0].set(xlabel='[K]', ylabel='y-label')

    # surface pressure is a PRIOR
    # note this "Pressure" is surface pressure, not interior pressure at depth
    counts, bins = np.histogram(Pressure_Distribution, bins=nbins)
    axs[0, 1].text(0.8, 0.8, 'Prior', c='red', transform=axs[0,1].transAxes, fontsize=12)
    axs[0, 1].stairs(counts, bins, fill=1, color='red')
    axs[0, 1].set_xlabel('Surface Pressure [bar]')
    axs[0, 1].set_ylim(0, np.sort(counts)[-2]+10)

    # bond albedo is a prior
    counts, bins = np.histogram(BondAlbedo_Distribution, bins=nbins)
    axs[1, 0].text(0.8, 0.8, 'Prior', c='red', transform=axs[1,0].transAxes, fontsize=12)
    axs[1, 0].stairs(counts, bins, fill=1, color='red')
    axs[1, 0].set_xlabel('Bond Albedo')
    axs[1, 0].set_ylim(0, np.sort(counts)[-2]+10)

    # greenhouse distribution is a PRIOR
    counts, bins = np.histogram(GreenHouse_Distribution, bins=nbins)
    axs[1, 1].text(0.8, 0.8, 'Prior', c='red', transform=axs[1,1].transAxes, fontsize=12)
    axs[1, 1].stairs(counts, bins, fill=1, color='red')
    axs[1, 1].set_xlabel('Greenhouse Warming [K]')
    axs[1, 1].set_ylim(0, np.sort(counts)[-2]+10)

    fig.suptitle('Probability Distribution of Key Parameters  '+keyparams.runid, fontsize=13)


    #axs[0, 0].hist(Temperature_Distribution) #,bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[0, 0].set_xlabel('Surface Temp. [K]')
    #axs[0, 1].hist(Pressure_Distribution ) #, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[0, 1].set_xlabel('Surface Pressure [bar]')
    #axs[1, 0].hist(BondAlbedo_Distribution)#, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[1, 0].set_xlabel('Bond Albedo')
    #axs[1, 1].hist(GreenHouse_Distribution )#), bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[1, 1].set_xlabel('Greenhouse Warming [K]')


    fig.tight_layout()

    fig.savefig('Figures/'+keyparams.runid+'_Multi-plot.png')

    #for ax in axs.flat:
    #    ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    #for ax in axs.flat:
    #    ax.label_outer()
    plt.show()


    return
