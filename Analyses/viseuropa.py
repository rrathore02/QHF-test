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


    plt.rcParams.update({'font.size': 4})
    fig, ax = plt.subplots(figsize=(2.00, 3.00), dpi=400)

    #ax.facecolor(bkgcolor)
    #ax.edgecolor(selected_edgecolor)
    # Add frame:
    #for zz in np.arange(int(NumProbes)):
    ax.set_xlim([0.,1.2])
    ax.set_ylim([136_000,-15000])
    ax.plot(Suitability_Plot,Variable, alpha=0.8,color='black',markersize=1.1)
    ax.plot([0., 1.2],[keyparams.Mean_IceThickness,keyparams.Mean_IceThickness], linestyle='--',linewidth=0.5,color='darkblue')
    ax.fill_between([0., 1.2],[keyparams.Mean_IceThickness,keyparams.Mean_IceThickness], color='lightblue')
    ax.plot([-100.,100],[0.,0.], linestyle='--', linewidth=0.5, color='red')
    ax.text(0.1,4000.,'Surface', fontsize=4, color='darkblue')
    # Plot the ocean floor level and color it gray
    ax.fill_between([0., 1.2],[0_000,0_000], [-15_000,-15_000],color='black')
    ax.text(0.6,-10_000.,'Space', fontsize=6, color='white')
    ax.text(0.6,70_000.,'Ocean', fontsize=6, color='darkblue')
    ax.text(0.6,135000.,'Rocky Interior', fontsize=6, color='white')
    ax.text(0.6,13_000.,'Ice', fontsize=6, color='white')
    ax.plot([-100.,128000],[0.,0.], linestyle='--', linewidth=0.5, color='gray')
    ax.fill_between([0., 1.2],[128_000,128_000], [136_000,136_000],color='lightgray')
    #ax.text(0.7,keyparams.Mean_IceThickness-2000,'Mean Ice Thickness', fontsize=4, color='black')
    ax.text(0.1,-1000.,keyparams.runid, fontsize=3.5)
    ax.set_title('Habitat Suitability for Europa Subsurface \n '+ keyparams.runid, fontsize=3.5)
    ax.set_ylabel('Depth [m]')
    ax.set_xlabel('Probability of Habitat Suitability')

    # Add logo of the habitat
    im = plt.imread(HabitatLogo)
    newax = fig.add_axes([0.75, 0.55, 0.15, 0.15], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)

    fig.tight_layout()
    fig.savefig('Figures/Europa_HS-Depth.png')
    plt.show()

    #=========================================================
    # 3D SCATTER PLOT : Pressure - Temperature - Depth

    #fig, ax = plt.subplots(figsize=(2.00, 3.00))
    ax = plt.axes(projection='3d')#,figsize=(4.00, 2.00), dpi=400)
    fig = ax.get_figure()
    fig.set_size_inches(8, 8)
    ax.scatter3D(Temperature_Distribution, Depth_Distribution, Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=1.7,alpha=0.3);
    plt.rcParams.update({'font.size': 10})
    if screen: ax.scatter3D(Temperature_Distribution, Depth_Distribution, Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=4.9,alpha=0.1,fontsize=10*sf,);
    ax.set_xlabel('Temperature [K]',fontsize=10*sf)
    ax.tick_params(labelsize=8*sf)
    #ax.set_xrange(220,450)
    #ax.axes.set_xlim3d(left=50, right=900)
    ax.axes.set_xlim3d(left=50, right=np.max(Temperature_Distribution)+200.0)
    ax.set_ylabel('Depth [m]',fontsize=10*sf)
    ax.axes.set_ylim3d(bottom=-15_000, top=128_000)
    ax.set_zlabel('Habitat Suitability',fontsize=10*sf)
    ax.set_title(keyparams.runid + ' | S = %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor)
    #ax.text(0.02,0.02,0.02, 'Average Suitability %.2f' % np.mean(Suitability_Distribution),fontsize=10*sf,color=labelcolor,transform=ax.transAxes)
    #fig.tight_layout()
    newax = fig.add_axes([0.75, 0.65, 0.10, 0.10], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)
    fig.savefig('Figures/Europa_3D-Plot.png')
    plt.show()

    # debugging breakpoint, comment-out to let things run through without interruption:
    #breakpoint()

    # Multi-plot showing distributions of key parameters
    # This will need to be optimizable from the module loaded, but now I specify the parameters
    N_iter = np.floor(len(Temperature_Distribution)).astype(int) # set number of iterations based on length of a posterior distribution array
    fig=plt.figure(figsize=(4.00, 2.00), dpi=400)
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].hist(Temperature_Distribution,bins=np.clip(math.floor(N_iter/60.), 5, 30))
    axs[0, 0].set_title('Temperature [K]')
    axs[0,0].set(xlabel='[K]', ylabel='y-label')
    # Matthew here -- I've commented these out to avoid errors because they don't really make sense for Europa,
    #    and aren't even calculated properly for such a plot like this anyways
    #axs[0, 1].hist(Surface_Pressure_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[0, 1].set_title('Surface Pressure [bar]')
    #axs[1, 0].hist(BondAlbedo_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[1, 0].set_title('Bond Albedo')
    #axs[1, 1].hist(GreenHouse_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
    #axs[1, 1].set_title('Greenhouse Warming [K]')
    #fig.tight_layout()

    #for ax in axs.flat:
    #    ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    #for ax in axs.flat:
    #    ax.label_outer()
    plt.show()


    return
