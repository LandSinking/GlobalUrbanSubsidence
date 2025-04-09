
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from matplotlib import font_manager
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.stats import gaussian_kde
import numpy as np

import matplotlib as mpl
mpl.rcParams['axes.formatter.use_mathtext'] = False




def read_color_scale_and_create_map(file_path):
    """
    
    :param file_path: file_path of colorbar
    :return: boundaries, colors , cmap , norm
    """
    boundaries = []
    colors = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue  
            
            parts = line.split(',')
            
            if len(parts) < 3:
                print(f"Skipping invalid line: {line}")
                continue
            
            try:
                boundary_start = float(parts[0].strip())
                boundary_end = float(parts[1].strip())
                color = parts[2].strip()
                

                boundaries.append(boundary_start)
                

                colors.append(color)
                
            except ValueError as e:
                print(f"Skipping invalid line: {line} due to error: {e}")
                continue


    if lines:  
        last_line = lines[-1].strip()
        if last_line:
            parts = last_line.split(',')
            if len(parts) >= 3:
                boundary_end = float(parts[1].strip())
                boundaries.append(boundary_end)

   
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(boundaries, ncolors=len(colors))
    

    return boundaries, colors, cmap, norm


def main():
    print(os.getcwd())
    ############################ 
    csv_path = r".\paixu.csv"
    data = pd.read_csv(csv_path)


    latitudes = data['Lat(N)']
    longitudes = data['Lon(E)']
    median_values = data['median']
    p10_values = data['p10']
    pth5_values = data['pth5']


    fig, axs = plt.subplots(3, 1, figsize=(8, 10), dpi=600, subplot_kw={'projection': ccrs.Robinson()},  gridspec_kw={'hspace': 0.2})  # 控制垂直间距

    extent = [-180, 180, -60, 90]  


    ############################ 

    color0_pth = r"./median_colorbar.txt"
    boundaries0, colors0, cmap0, norm0 = read_color_scale_and_create_map(color0_pth)
    

    kde_median = gaussian_kde(median_values)
    x_vals_median = np.linspace(min(median_values), max(median_values), 500)
    y_vals_median = kde_median(x_vals_median)


    sorted_data0 = data.sort_values(by='median', ascending=False)


    sorted_latitudes0 = sorted_data0['Lat(N)']
    sorted_longitudes0 = sorted_data0['Lon(E)']
    sorted_median_values = sorted_data0['median']



    axs[0].set_extent([-180, 180, -60, 90])
    axs[0].add_feature(cfeature.LAND, facecolor="#e2e1e4")
    scatter = axs[0].scatter(sorted_longitudes0, sorted_latitudes0, c=sorted_median_values, cmap=cmap0, norm=norm0, s=16, edgecolors='#404040',  linewidths=0.3, transform=ccrs.PlateCarree())



    axs[0].set_extent(extent)
    axs[0].add_feature(cfeature.LAND, facecolor="#e2e1e4")
    axs[0].spines['geo'].set_linewidth(0.4) 
    axs[0].text(0.01, 0.99, 'a', transform=axs[0].transAxes, fontsize=12, fontname='Arial', va='top', ha='left')

    cbar0 = fig.colorbar(scatter, ax=axs[0], orientation='horizontal', pad=0.05, fraction=0.025, aspect=40,  extend='both')


    ticks0 = [-10, -8, -6, -4, -2, 0, 2, 4] 
    cbar0.set_ticks(ticks0)  


    cbar0.ax.tick_params(width=0.2, length=2.2, direction='in', which='major')
    cbar0.ax.tick_params(which='minor', length=0)  

    for spine in cbar0.ax.spines.values():
        spine.set_linewidth(0.3)  



    cbar0.ax.text(0.5, -6, r'Median velocity ($\regular{V_{m}}$, mm/yr)', fontsize=10, fontname='Arial', ha='center', va='bottom', transform=cbar0.ax.transAxes)

    
    cbar0.ax.tick_params(labelsize=3, labelcolor='black') 
    for label in cbar0.ax.get_xticklabels():
        label.set_fontsize(8)
        label.set_fontname('Arial')


    inset_ax = inset_axes(axs[0], width="19%", height="30%", loc='lower left', borderpad=1.9)


    
        
    for i in range(len(boundaries0) - 1):
        inset_ax.fill_between(x_vals_median, 0, y_vals_median, 
                        where=(x_vals_median >= boundaries0[i]) & (x_vals_median < boundaries0[i + 1]),
                        color=colors0[i], alpha=1, interpolate=False, label=f'{boundaries0[i]}-{boundaries0[i+1]}')

 
    inset_ax.tick_params(axis='both', which='major', labelsize=6, direction='in', length=1, width=0.2)
    inset_ax.spines['top'].set_visible(False)  
    inset_ax.spines['right'].set_visible(False) 
    inset_ax.spines['left'].set_linewidth(False)  
    inset_ax.spines['bottom'].set_linewidth(0.15) 

    inset_ax.yaxis.set_ticks([]) 
    inset_ax.yaxis.set_ticklabels([])  


    inset_ax.set_xticks([-8,  -2,  4])  
    for label in inset_ax.get_xticklabels():
        label.set_fontsize(6)
        label.set_fontname('Arial')



    inset_ax.set_xlim([-20, 15])  
    


    inset_ax.tick_params(axis='x', which='both', labelsize=6, labelcolor='black')  
    inset_ax.tick_params(axis='y', which='both', labelsize=6, labelcolor='black') 


    median_value0 = np.median(median_values)
    inset_ax.axvline(median_value0, color='black', linestyle='--', linewidth=0.8, alpha=0.8, ymin=0.034, ymax=0.97)


    median_value0 = round(median_value0) 
    median_str = f"Median: {median_value0}".replace("-", "−")  

    
    inset_ax.text(median_value0 - 18.5, np.max(y_vals_median) * 0.8,
                median_str, fontsize=6, fontname='Arial', color='black', ha='left', va='top')
    
   



    ############################ 
    color1_pth = r"./pth5_colorbar.txt"

    boundaries1, colors1, cmap1, norm1 = read_color_scale_and_create_map(color1_pth)


    kde_pth5 = gaussian_kde(pth5_values)
    x_vals_pth5 = np.linspace(min(pth5_values), max(pth5_values), 500)
    y_vals_pth5 = kde_pth5(x_vals_pth5)


    sorted_data1 = data.sort_values(by='pth5', ascending=False)


    sorted_latitudes1 = sorted_data1['Lat(N)']
    sorted_longitudes1 = sorted_data1['Lon(E)']
    sorted_pth5_values = sorted_data1['pth5']

   
    axs[1].set_extent(extent)
   
    scatter = axs[1].scatter(sorted_longitudes1, sorted_latitudes1, c=sorted_pth5_values, cmap=cmap1, norm=norm1, s=16, edgecolors='#404040',  linewidths=0.3, transform=ccrs.PlateCarree())
    

    axs[1].add_feature(cfeature.LAND, facecolor="#e2e1e4")
    axs[1].spines['geo'].set_linewidth(0.3) 
    axs[1].text(0.01, 0.99, 'b', transform=axs[1].transAxes, fontsize=12, fontname='Franklin Gothic Medium', va='top', ha='left')
 
    cbar1 = fig.colorbar(scatter, ax=axs[1], orientation='horizontal', pad=0.05, fraction=0.025, aspect=40,  extend='both')
    cbar1.ax.tick_params(width=0.2, length=2.2, direction='in', which='major')
    cbar1.ax.tick_params(which='minor', length=0)

    ticks1 = [-135, -105, -75, -45, -15] 
    cbar1.set_ticks(ticks1)

    for spine in cbar1.ax.spines.values():
        spine.set_linewidth(0.3) 



    cbar1.ax.text(0.5, -6, r'5th percentile velocity ($\regular{V_{5th}}$, mm/yr)', fontsize=10, fontname='Arial', ha='center', va='bottom', transform=cbar1.ax.transAxes)



    
   


    cbar1.ax.tick_params(labelsize=3, labelcolor='black')  
    for label in cbar1.ax.get_xticklabels():
        label.set_fontsize(8)
        label.set_fontname('Arial')


    inset_ax = inset_axes(axs[1], width="19%", height="30%", loc='lower left', borderpad=1.9)

   
    for i in range(len(boundaries1) - 1):
        inset_ax.fill_between(x_vals_pth5, 0, y_vals_pth5, where=(x_vals_pth5 >= boundaries1[i]) & (x_vals_pth5 < boundaries1[i + 1]),
                            color=colors1[i], alpha=1, label=f'{boundaries1[i]}-{boundaries1[i+1]}')
  
    inset_ax.tick_params(axis='both', which='major', labelsize=6, direction='in', length=1, width=0.2)
    inset_ax.spines['top'].set_visible(False)  
    inset_ax.spines['right'].set_visible(False)  
    inset_ax.spines['left'].set_linewidth(False) 
    inset_ax.spines['bottom'].set_linewidth(0.15)  

  
    inset_ax.yaxis.set_ticks([])  
    inset_ax.yaxis.set_ticklabels([]) 


    inset_ax.set_xlim([-160, 10])  



    inset_ax.set_xticks([-135,  -75,  -15])  

    for label in inset_ax.get_xticklabels():
        label.set_fontsize(6)
        label.set_fontname('Arial')



  
    inset_ax.tick_params(axis='x', which='both', labelsize=6, labelcolor='black') 
    inset_ax.tick_params(axis='y', which='both', labelsize=6, labelcolor='black')  


   
    median_value1 = np.median(pth5_values)
 
    inset_ax.axvline(median_value1, color='black', linestyle='--', linewidth=0.8, alpha=0.8, ymin=0.034, ymax=0.97)


    
    median_value1 = int(median_value1)  
    median_str = f"Median: {median_value1}".replace("-", "−")  

    
    inset_ax.text(median_value1 - 94, np.max(y_vals_pth5) * 0.8,
                median_str, fontsize=6, fontname='Arial', color='black', ha='left', va='top')



        
    ############################ 
    color2_pth = r"./p10_colorbar.txt"
    boundaries2, colors2, cmap2, norm2 = read_color_scale_and_create_map(color2_pth)


    kde_p10 = gaussian_kde(p10_values)
    x_vals_p10 = np.linspace(min(p10_values), max(p10_values), 500)
    y_vals_p10 = kde_p10(x_vals_p10)

    
    sorted_data2 = data.sort_values(by='p10')

    sorted_latitudes2 = sorted_data2['Lat(N)']
    sorted_longitudes2 = sorted_data2['Lon(E)']
    sorted_p10_values = sorted_data2['p10']


    axs[2].set_extent(extent)
    scatter = axs[2].scatter(sorted_longitudes2, sorted_latitudes2, c=sorted_p10_values, cmap=cmap2, norm=norm2, s=16, edgecolors='#404040',  linewidths=0.3, transform=ccrs.PlateCarree())
   

    axs[2].add_feature(cfeature.LAND, facecolor="#e2e1e4")
    axs[2].spines['geo'].set_linewidth(0.4) 
    axs[2].text(0.01, 0.99, 'c', transform=axs[2].transAxes, fontsize=12, fontname='Franklin Gothic Medium', va='top', ha='left')

    cbar2 = fig.colorbar(scatter, ax=axs[2], orientation='horizontal', pad=0.05, fraction=0.025, aspect=40,  extend='max')
    cbar2.ax.tick_params(width=0.2, length=2.2, direction='in', which='major')
    cbar2.ax.tick_params(which='minor', length=0)  


    pos = cbar2.ax.get_position()

    cbar2.ax.set_position([0.137, pos.y0, pos.width, pos.height])

   
    ticks2 = [0, 0.1, 0.3, 0.5, 0.7, 0.9]  
    cbar2.set_ticks(ticks2) 

    cbar2.set_ticklabels(['0', '10', '30', '50', '70', '90']) 

    for spine in cbar2.ax.spines.values():
        spine.set_linewidth(0.3) 




    velocity_threshold = -10


    cbar2.ax.text(0.52, -6, r'Proportion of urban lands with a velocity < {} mm/yr ($\regular{{P_{{10}}}}$, %)'.format(velocity_threshold), 
                      fontsize=10, fontname='Arial', ha='center', va='bottom', transform=cbar2.ax.transAxes)
    
    
    cbar2.ax.tick_params(labelsize=3, labelcolor='black')  
    for label in cbar2.ax.get_xticklabels():
        label.set_fontsize(8)
        label.set_fontname('Arial')

    inset_ax = inset_axes(axs[2], width="19%", height="30%", loc='lower left', borderpad=1.9)


    for i in range(len(boundaries2) - 1):
        inset_ax.fill_between(x_vals_p10, 0, y_vals_p10, where=(x_vals_p10 >= boundaries2[i]) & (x_vals_p10 < boundaries2[i + 1]),
                            color=colors2[i], alpha=1, label=f'{boundaries2[i]}-{boundaries2[i+1]}')
   
  
    inset_ax.tick_params(axis='both', which='major', labelsize=6, direction='in', length=1, width=0.2)
    inset_ax.spines['top'].set_visible(False)  
    inset_ax.spines['right'].set_visible(False)  
    inset_ax.spines['left'].set_linewidth(False)  
    inset_ax.spines['bottom'].set_linewidth(0.15)  

  
    inset_ax.yaxis.set_ticks([]) 
    inset_ax.yaxis.set_ticklabels([])  

   

    inset_ax.set_xticks([0.1, 0.3,  0.5]) 
   
    inset_ax.set_xticklabels(['10', '30', '50'], fontsize=6, fontname='Arial')
    for label in inset_ax.get_xticklabels():
        label.set_fontsize(6)
        label.set_fontname('Arial')

  
    inset_ax.tick_params(axis='x', which='both', labelsize=6, labelcolor='black') 
    inset_ax.tick_params(axis='y', which='both', labelsize=6, labelcolor='black') 


    median_value2 = np.median(p10_values)
    inset_ax.axvline(median_value2, color='black', linestyle='--', linewidth=0.8, alpha=0.8, ymin=0.034, ymax=0.97)

    
    inset_ax.text(median_value2 + 0.06, np.max(y_vals_p10) * 0.8,  
              'Median: 5 %', fontsize=6, fontname='Arial', color='black', ha='left', va='top')

    plt.savefig(r"../plot_result/Fig1.tif", dpi=600, format='tif')




if __name__ == "__main__":
    main()
