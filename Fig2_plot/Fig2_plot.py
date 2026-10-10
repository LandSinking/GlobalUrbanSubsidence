import os
import numpy as np
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
                continue

            try:
                boundaries.append(float(parts[0]))
                colors.append(parts[2].strip())
            except ValueError:
                continue

        last = lines[-1].strip()
        if last:
            parts = last.split(',')
            if len(parts) >= 2:
                boundaries.append(float(parts[1]))

    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(boundaries, ncolors=len(colors))

    return cmap, norm


def plot_panel(ax, lon, lat, values, cmap, norm, tag, fig, cbar_label):

    ax.set_global()
    ax.set_extent([-180, 180, -60, 90])

    sorted_idx = np.argsort(values)

    sc = ax.scatter(
        lon.iloc[sorted_idx],
        lat.iloc[sorted_idx],
        c=values.iloc[sorted_idx],
        cmap=cmap,
        norm=norm,
        s=12, #22
        #edgecolors='#404040',
        edgecolors="#6A6A6A",
        linewidths=0.12, # 0.3
        transform=ccrs.PlateCarree()
    )

    ax.add_feature(cfeature.LAND, facecolor="#e2e1e4")
    #ax.spines['geo'].set_linewidth(0.5)
    ax.spines['geo'].set_linewidth(0.2)

    # 
    ax.text(
        0.02, 0.98,
        tag,
        transform=ax.transAxes,
        fontsize=7,
        fontname='Arial',
        fontweight='bold',
        va='top',
        ha='left'
    )

    # =========================
    # colorbar
    # =========================
    cbar = fig.colorbar(
        sc,
        ax=ax,
        orientation='horizontal',
        pad=0.05,
        fraction=0.025, # 0.020
        aspect=40,
        extend='neither'  
    )

    cbar.ax.tick_params(
        labelsize=9,
        width=0.3,
        length=2,
        direction='in'
    )

   

    plt.setp(cbar.ax.get_xticklabels(), fontname='Arial', fontsize=5)

    for spine in cbar.ax.spines.values():
        spine.set_linewidth(0.5)

    cbar.outline.set_linewidth(0.3)
   
    cbar.ax.set_xlabel(
        cbar_label,
        fontsize=6,
        fontname='Arial',
        labelpad= 3 #6
    )

    return sc


def main():

    xls_path = r"./Fig2_data.xlsx"
    data = pd.read_excel(xls_path, header=[0, 1])

    lon = data[('Lon.(°E)')]
    lat = data[('Lat.(°N)')]

    rlls = data['InSAR-derived RLLS']
    vlm  = data['VLM-aligned land subsidence']

    val_rlls = rlls['Composite severity score [0,100]']
    val_vlm  = vlm['Composite severity score [0,100]']

    cmap, norm = read_color_scale_and_create_map("./p10_colorbar.txt")


    """ fig, axs = plt.subplots(
        2, 1,
        figsize=(8, 9.6),
        dpi=600,
        subplot_kw={'projection': ccrs.Robinson()},
        gridspec_kw={'hspace': 0.15}
    ) """
    


    width = 180
    height = 120

    # 1英寸=2.54厘米=254毫米
    # Matplotlib 的 figsize 单位是英寸(inch)

    fig, axs = plt.subplots(
        2, 1,
        figsize=(width/25.4, height/25.4),
        dpi=600,
        subplot_kw={'projection': ccrs.Robinson()},
        gridspec_kw={'hspace': 0.18}
    )

    fig.subplots_adjust(
        top=0.97,
        bottom=0.06,
        left=0.2,
        right=0.8
    )



    plot_panel(
        axs[0], lon, lat, val_rlls,
        cmap, norm,
        tag="a",
        fig=fig,
        cbar_label="Composite severity score of InSAR-derived RLLS"
    )

    plot_panel(
        axs[1], lon, lat, val_vlm,
        cmap, norm,
        tag="b",
        fig=fig,
        cbar_label="Composite severity score of VLM-aligned land subsidence"
    )

    plt.rcParams['pdf.fonttype'] = 42

    plt.savefig("./Fig2_plot.tif", dpi=600, format='tif')
    plt.savefig("./Fig2_plot.png", dpi=600, format='png')
    plt.savefig("./Fig2_plot.pdf", dpi=600, format='pdf')
          

    plt.close()


if __name__ == "__main__":
    main()