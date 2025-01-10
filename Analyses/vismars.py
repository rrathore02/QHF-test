import keyparams
import matplotlib.pyplot as plt
import numpy as np
import math

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

    ### ===================================================================================== ##
    ##   Suitability vs. Depth profile plot
    ### ===================================================================================== ##

    plt.rcParams.update({'font.size': 4})
    fig, ax = plt.subplots(figsize=(2.00, 4.00), dpi=200)
    # Suitability vs. negative Depth 
    #   negative Depth so that it is 'elevation' instead
    #   above surface = positive, below surface = negative
    ax.plot(Suitability_Plot,-np.asarray(Variable), alpha=0.8,color='black',markersize=1.1)
    # Limit suitability axis
    ax.set_xlim([0.,1.2])
    # Limit elevation to 5000 m below the surface
    ax.set_ylim([-15000,2000]) 
    # Plot shaded regions to indicate above/below the surface
    #    blue = atmosphere, red = sub-surface
    ax.text(0.7, 750.,'Atmosphere', fontsize=5, color='gray')
    ax.fill_between([0.0,1.2],[0_000,0_000],[5000,5000], color='lightblue',alpha=0.3) # make sure these somewhat match axes limits!
    ax.text(0.7,-5_000.,'Subsurface', fontsize=5, color='red')
    ax.plot([-100.,100],[0.,0.], linestyle='--', linewidth=0.5, color='red') # dotted line to highlight the surface
    ax.fill_between([0.0,1.2],[0_000,0_000],[-100_000,-100_000], color='red',alpha=0.05)
    # Set axes labels and titles
    ax.set_title('Habitat Suitability for Mars Subsurface \n '+ keyparams.runid)
    ax.set_ylabel('Elevation [m]')
    ax.set_xlabel('Probability of Habitat Suitability')
    # Add logo of the habitat to the plot (optional)
    im = plt.imread(HabitatLogo)
    newax = fig.add_axes([0.75, 0.55, 0.15, 0.15], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)
    # save and show figure
    fig.tight_layout()
    fig.savefig('Figures/Mars_HS-Depth.png')
    fig.savefig('Figures/Mars_HS-Depth.svg') # vector format
    plt.show()

    ### ======================================================================================= ##
    ##    3D Suitability vs. Temperature vs. Depth scatter plot
    ### ======================================================================================= ##

    ax = plt.axes(projection='3d')#,figsize=(4.00, 2.00), dpi=400)
    ax.scatter3D(Temperature_Distribution, -np.array(Depth_Distribution), Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=1.7,alpha=0.3);
    fig = ax.get_figure()
    fig.set_size_inches(8, 8)
    plt.rcParams.update({'font.size': 10})
    if screen: ax.scatter3D(Temperature_Distribution, -np.array(Depth_Distribution), Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=4.9,alpha=0.1,fontsize=10*sf,);
    ax.set_xlabel('Temperature [K]',fontsize=10*sf)
    ax.tick_params(labelsize=8*sf)
    #ax.set_xrange(220,450)
    #ax.axes.set_xlim3d(left=220, right=650)
    ax.axes.set_xlim3d(left=min(Temperature_Distribution), right=max(Temperature_Distribution))
    ax.set_ylabel('Elevation [m]',fontsize=10*sf)
    ax.axes.set_ylim3d(bottom=0, top=-max(Depth_Distribution))
    ax.set_zlabel('Habitat Suitability',fontsize=10*sf)
    ax.set_title(keyparams.runid + ' | S = %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor)
    #ax.text(0.02,0.02,0.02, 'Average Suitability %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor,transform=ax.transAxes)
    # add logo:
    newax = fig.add_axes([0.75, 0.65, 0.10, 0.10], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)
    fig.savefig('Figures/Mars_3D-Plot.png')
    fig.savefig('Figures/Mars_3D-Plot.svg')
    plt.show()


    #breakpoint()

    # Multi-plot showing distributions of key parameters
    #sns.reset_orig()
    N_iter = 10.
    #fig=plt.figure(figsize=(4.00, 2.00), dpi=400)
    #fig, axs = plt.subplots(2, 2)
    #axs[0, 0].hist(Temperature_Distribution,bins=np.clip(math.floor(N_iter/60.), 5, 30),histtype='step')
    #axs[0, 0].hist(Temperature_Distribution,histtype='step')
    #axs[0, 0].set_title('Surface Temp. [K]')
    #axs[0,0].set(xlabel='[K]', ylabel='y-label')
    #axs[0, 1].hist(Pressure_Distribution, histtype='step')
    #axs[0, 1].set_title('Surface Pressure [bar]')
    #axs[1, 0].hist(BondAlbedo_Distribution, histtype='step')
    #axs[1, 0].set_title('Bond Albedo')
    #axs[1, 1].hist(GreenHouse_Distribution,histtype='step')
    #axs[1, 1].set_title('Greenhouse Warming [K]')
    #fig.tight_layout()


    fig, axs = plt.subplots(2, 2,constrained_layout=True,figsize=(12.00, 4.00))
    #N_iter = 100.

    counts, bins = np.histogram(Temperature_Distribution, bins=20)
    axs[0, 0].stairs(counts, bins, fill=1)
    axs[0, 0].set_xlabel('Temperature [K]')
    #axs[0,0].set(xlabel='[K]', ylabel='y-label')

    counts, bins = np.histogram(Pressure_Distribution, bins=20)
    axs[0, 1].stairs(counts, bins, fill=1)
    axs[0, 1].set_xlabel('Surface Pressure [bar]')

    counts, bins = np.histogram(BondAlbedo_Distribution, bins=20)
    axs[1, 0].stairs(counts, bins, fill=1)
    axs[1, 0].set_xlabel('Bond Albedo')

    counts, bins = np.histogram(GreenHouse_Distribution, bins=20)
    axs[1, 1].stairs(counts, bins, fill=1)
    axs[1, 1].set_xlabel('Greenhouse Warming [K]')

    fig.suptitle('Probability Distribution of Key Parameters  '+keyparams.runid, fontsize=13)

    fig.savefig('Figures/'+keyparams.runid+'_Multi-plot.png')
    fig.savefig('Figures/'+keyparams.runid+'_Multi-plot.svg')
    #for ax in axs.flat:
    #    ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    #for ax in axs.flat:
    #    ax.label_outer()
    #plt.show()
    plt.close()


    return
