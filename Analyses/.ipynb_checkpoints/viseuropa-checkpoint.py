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
    print(keyparams.Ice_Thickness)
    plt.rcParams.update({'font.size': 4})
    fig, ax = plt.subplots(figsize=(2.00, 3.00), dpi=400)
    # Suitability vs. negative Depth 
    #   negative Depth so that it is 'elevation' instead
    #   above surface = positive, below surface = negative
    ax.plot(Suitability_Plot,-np.asarray(Variable), alpha=0.8,color='black',markersize=1.1)
    # Limit suitability axis
    ax.set_xlim([0.,1.2])
    # Limit elevation
    ax.set_ylim([-135_000,15_000]) 
    # indicate the ice layer
    ax.plot([0., 1.2],[-keyparams.Ice_Thickness,-keyparams.Ice_Thickness], linestyle='--',linewidth=0.5,color='darkblue')
    ax.fill_between([0., 1.2],[0,0], [-keyparams.Ice_Thickness,-keyparams.Ice_Thickness], color='lightblue')
    ax.text(0.9,-6_000.,'Ice', fontsize=6, color='darkblue')
    # indicate the ocean layer
    ax.text(0.9,-70_000.,'Ocean', fontsize=6, color='darkblue')
    # indicate rocky interior (lower boundary)
    ax.text(0.65,-132000.,'Rocky Interior', fontsize=6, color='white')
    ax.plot([-100.,-128000],[0.,0.], linestyle='--', linewidth=0.5, color='gray')
    ax.fill_between([0., 1.2],[-128_000,-128_000], [-136_000,-136_000],color='lightgray')
    ax.plot([-100.,100],[0.,0.], linestyle='--', linewidth=0.5, color='red')
    ax.text(0.1,-4000.,'Surface', fontsize=4, color='darkred')
    # indicate space (above surface)
    ax.fill_between([0., 1.2],[0_000,0_000], [15_000,15_000],color='black')
    ax.text(0.9,8_000.,'Space', fontsize=6, color='white')

    ax.set_title('Habitat Suitability for Europa Subsurface \n '+ keyparams.runid, fontsize=3.5)
    ax.set_ylabel('Elevation [m]')
    ax.set_xlabel('Probability of Habitat Suitability')

    # Add logo of the habitat
    im = plt.imread(HabitatLogo)
    newax = fig.add_axes([0.75, 0.55, 0.15, 0.15], anchor='NE')
    newax.set_axis_off()
    newax.imshow(im)

    fig.tight_layout()
    fig.savefig('Figures/Europa_HS-Depth.png')
    plt.show()

    ### ======================================================================================= ##
    ##    3D Suitability vs. Temperature vs. Depth scatter plot
    ### ======================================================================================= ##    


    ax = plt.axes(projection='3d')#,figsize=(4.00, 2.00), dpi=400)
    fig = ax.get_figure()
    fig.set_size_inches(8, 8)
    ax.scatter3D(Temperature_Distribution, -np.array(Depth_Distribution), Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=1.7,alpha=0.3);
    plt.rcParams.update({'font.size': 10})
    if screen: ax.scatter3D(Temperature_Distribution, -np.array(Depth_Distribution), Suitability_Distribution, c=Suitability_Distribution, cmap='seismic',s=4.9,alpha=0.1,fontsize=10*sf,);
    # temperature axis:
    ax.set_xlabel('Temperature [K]',fontsize=10*sf)
    ax.tick_params(labelsize=8*sf)
    ax.axes.set_xlim3d(left=50, right=np.max(Temperature_Distribution)+200.0)
    # depth / elevation axis:
    ax.set_ylabel('Elevation [m]',fontsize=10*sf)
    ax.axes.set_ylim3d(bottom=-128_000, top=0)
    # Suitability axis:
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
#     N_iter = np.floor(len(Temperature_Distribution)).astype(int) # set number of iterations based on length of a posterior distribution array
#     fig=plt.figure(figsize=(4.00, 2.00), dpi=400)
#     fig, axs = plt.subplots(2, 2)
#     axs[0, 0].hist(Temperature_Distribution,bins=np.clip(math.floor(N_iter/60.), 5, 30))
#     axs[0, 0].set_title('Temperature [K]')
#     axs[0,0].set(xlabel='[K]', ylabel='y-label')
#     # Matthew here -- I've commented these out to avoid errors because they don't really make sense for Europa,
#     #    and aren't even calculated properly for such a plot like this anyways
#     #axs[0, 1].hist(Surface_Pressure_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
#     #axs[0, 1].set_title('Surface Pressure [bar]')
#     #axs[1, 0].hist(BondAlbedo_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
#     #axs[1, 0].set_title('Bond Albedo')
#     #axs[1, 1].hist(GreenHouse_Distribution, bins=np.clip(math.floor(N_iter/60.), 5, 30))
#     #axs[1, 1].set_title('Greenhouse Warming [K]')
#     #fig.tight_layout()

#     #for ax in axs.flat:
#     #    ax.set(xlabel='x-label', ylabel='y-label')

#     # Hide x labels and tick labels for top plots and y ticks for right plots.
#     #for ax in axs.flat:
#     #    ax.label_outer()
#     plt.show()
    
    # ## plot the thermal profile
    # Depth_Distribution = np.asarray(Depth_Distribution)     
    
    # fig, ax = plt.subplots(figsize=(8,4), dpi=400)
    # niters = len(np.where(Depth_Distribution == max(Depth_Distribution))[0])
    # avgdepths = np.average(np.asarray(Depth_Distribution).reshape(-1, niters), axis=1) 
    # ax.plot(Depth_Distribution[::niters], Temperature_Distribution[::niters], c='black', zorder=10, alpha=0.25, label='Temperature Profiles')
    # avgtemps = np.average(np.asarray(Temperature_Distribution).reshape(-1,niters), axis=1)
    # #
    # ax.plot(avgdepths, avgtemps, c='black', zorder=10, label='Average Thermal Profile')
    # ax.axvline(keyparams.Ice_Thickness, c='lightblue')
    # ax.fill_betweenx(y=np.linspace(min(Temperature_Distribution)-50, max(Temperature_Distribution)+50, 50),
    #                  x1=keyparams.Ice_Thickness, x2=0, facecolor='lightblue', alpha=0.5, edgecolor='lightblue',label='Ice')
    # ax.set_xlabel('Depth [m]', fontsize=12)
    # ax.set_xlim(0., max(Depth_Distribution)+10000)
    # ax.set_ylabel('Temperature [K]', fontsize=12)
    # ax.set_ylim(min(Temperature_Distribution)-20, max(Temperature_Distribution)+20)
    # ax.legend(loc='best')
    # plt.show()


    return
