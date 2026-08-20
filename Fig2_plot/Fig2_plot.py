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
        s=22,
        edgecolors='#404040',
        linewidths=0.3,
        transform=ccrs.PlateCarree()
    )

    ax.add_feature(cfeature.LAND, facecolor="#e2e1e4")
    ax.spines['geo'].set_linewidth(0.5)

    # 
    ax.text(
        0.02, 0.98,
        tag,
        transform=ax.transAxes,
        fontsize=14,
        fontname='Arial',
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
        fraction=0.020,
        aspect=40,
        extend='neither'  
    )

    cbar.ax.tick_params(
        labelsize=9,
        width=0.3,
        length=2,
        direction='in'
    )

    plt.setp(cbar.ax.get_xticklabels(), fontname='Arial', fontsize=10)

    for spine in cbar.ax.spines.values():
        spine.set_linewidth(0.5)

   
    cbar.ax.set_xlabel(
        cbar_label,
        fontsize=14,
        fontname='Arial',
        labelpad=6
    )

    return sc


def main():

    xls_path = r".\Fig2_data.xlsx"
    data = pd.read_excel(xls_path, header=[0, 1])

    lon = data[('Lon.(°E)', 'Unnamed: 3_level_1')]
    lat = data[('Lat.(°N)', 'Unnamed: 4_level_1')]

    rlls = data['InSAR-derived RLLS']
    vlm  = data['VLM-aligned land subsidence']

    val_rlls = rlls['Composite severity score [0,100]']
    val_vlm  = vlm['Composite severity score [0,100]']

    cmap, norm = read_color_scale_and_create_map("./p10_colorbar.txt")

    fig, axs = plt.subplots(
        2, 1,
        figsize=(8, 9.6),
        dpi=600,
        subplot_kw={'projection': ccrs.Robinson()},
        gridspec_kw={'hspace': 0.15}
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

    #plt.savefig("Fig2_plot.tif", dpi=600, bbox_inches='tight', format='tif')
    plt.savefig("Fig2_plot.png", dpi=600, bbox_inches='tight', format='png')
          

    plt.close()


if __name__ == "__main__":
    main()