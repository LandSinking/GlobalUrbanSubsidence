import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib as mpl
mpl.rcParams['axes.formatter.use_mathtext'] = False


def read_color_scale_and_create_map(file_path):

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

    xls_path = r".\Fig2_data.xlsx"
    data = pd.read_excel(xls_path)

    fig, ax = plt.subplots(
        1, 1,
        figsize=(8, 5),
        dpi=600,
        subplot_kw={'projection': ccrs.Robinson()}
    )

    extent = [-180, 180, -60, 90]

    color_pth = r"./p10_colorbar.txt"
    boundaries, colors, cmap, norm = read_color_scale_and_create_map(color_pth)

    sorted_data = data.sort_values(by='Composite severity score [0,100]')
    sorted_latitudes = sorted_data['Lat.(°N)']
    sorted_longitudes = sorted_data['Lon.(°E)']
    sorted_p10_values = sorted_data['Composite severity score [0,100]']

    ax.set_extent(extent)

    scatter = ax.scatter(
        sorted_longitudes,
        sorted_latitudes,
        c=sorted_p10_values,
        cmap=cmap,
        norm=norm,
        s=16,
        edgecolors='#404040',
        linewidths=0.3,
        transform=ccrs.PlateCarree()
    )

    ax.add_feature(cfeature.LAND, facecolor="#e2e1e4")
    ax.spines['geo'].set_linewidth(0.4)


    cbar = fig.colorbar(
        scatter, ax=ax,
        orientation='horizontal',
        pad=0.04,
        fraction=0.016, 
        aspect=40
    )

    cbar.ax.tick_params(width=0.2, length=2.2, direction='in', which='major')
    cbar.ax.tick_params(which='minor', length=0)

    ticks = [0, 10, 30, 50, 70, 90, 100]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(['0', '10', '30', '50', '70', '90', '100'])

    for spine in cbar.ax.spines.values():
        spine.set_linewidth(0.3)

    cbar.ax.text(
        0.5, -5.6,
        'Composite severity score',
        fontsize=10,
        fontname='Arial',
        ha='center',
        va='bottom',
        transform=cbar.ax.transAxes
    )

    for label in cbar.ax.get_xticklabels():
        label.set_fontsize(8)
        label.set_fontname('Arial')



    # plt.savefig(r".\Fig2_plot.png", dpi=600, format='png')
    plt.savefig(r".\Fig2_plot.tif", dpi=600, format='tif')
    plt.close()



if __name__ == "__main__":
    main()