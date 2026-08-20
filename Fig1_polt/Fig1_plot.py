import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.stats import gaussian_kde
import numpy as np
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

    # print(os.getcwd())
    
    xls_path = r".\Fig1_data.xlsx"

    data = pd.read_excel(xls_path, header=[0,1])

    # print(data.columns)

    lon = data[('Lon.(°E)', 'Unnamed: 3_level_1')]
    lat = data[('Lat.(°N)', 'Unnamed: 4_level_1')]

    rlls = data['InSAR-derived RLLS']
    vlm  = data['VLM-aligned land subsidence']

    rlls_vm   = rlls['Vm (mm/yr)']
    rlls_v5th = rlls['V5th (mm/yr)']
    rlls_p10  = rlls['P10 (%)']

    vlm_vm   = vlm['Vm (mm/yr)']
    vlm_v5th = vlm['V5th (mm/yr)']
    vlm_p10  = vlm['P10 (%)']

    
    fig, axs = plt.subplots(
        3, 2, 
        figsize=(14, 10), 
        dpi=600, 
        subplot_kw={'projection': ccrs.Robinson()},  
        gridspec_kw={'hspace': 0.2, 'wspace': 0.08}
    )  

    extent = [-180, 180, -60, 90]  

    # =========================

    def plot_panel(
        ax,
        values,
        lon,
        lat,
        color_file,
        panel_label,
        cbar_label,
        fig,
        ticks,
        extend,
        inset_xlim,
        inset_xticks,
        median_shift,
        borderpad=1.9,
        cbar_move=None,
        ascending=False
    ):

        boundaries, colors, cmap, norm = \
            read_color_scale_and_create_map(color_file)

        values_clean = values.dropna()

        sorted_idx = np.argsort(values)

        if not ascending:
            sorted_idx = sorted_idx[::-1]

        sc = ax.scatter(
            lon.iloc[sorted_idx],
            lat.iloc[sorted_idx],
            c=values.iloc[sorted_idx],
            cmap=cmap,
            norm=norm,
            s=16,
            edgecolors='#404040',
            linewidths=0.3,
            transform=ccrs.PlateCarree()
        )

        ax.set_extent([-180,180,-60,90])

        ax.add_feature(
            cfeature.LAND,
            facecolor="#e2e1e4"
        )

        ax.spines['geo'].set_linewidth(0.4)

        ax.text(
            0.01,
            0.99,
            panel_label,
            transform=ax.transAxes,
            fontsize=12,
            fontname='Arial',
            va='top',
            ha='left'
        )

        # ==========================
        # colorbar
        # ==========================

        cbar = fig.colorbar(
            sc,
            ax=ax,
            orientation='horizontal',
            pad=0.05,
            fraction=0.025,
            aspect=40,
            extend=extend
        )

        if ticks is not None:
            cbar.set_ticks(ticks)

        cbar.ax.tick_params(
            width=0.2,
            length=2.2,
            direction='in',
            which='major'
        )

        cbar.ax.tick_params(
            which='minor',
            length=0
        )

        for spine in cbar.ax.spines.values():
            spine.set_linewidth(0.3)

        cbar.ax.text(
            0.5,
            -6,
            cbar_label,
            fontsize=10,
            fontname='Arial',
            ha='center',
            va='bottom',
            transform=cbar.ax.transAxes
        )

        cbar.ax.tick_params(
            labelsize=3,
            labelcolor='black'
        )

        for label in cbar.ax.get_xticklabels():
            label.set_fontsize(8)
            label.set_fontname('Arial')

        # P10
        if cbar_move is not None:

            pos = cbar.ax.get_position()

            cbar.ax.set_position([
                pos.x0 + cbar_move,
                pos.y0,
                pos.width,
                pos.height
            ])

        # ==========================
        # KDE 
        # ==========================

        inset_ax = inset_axes(
            ax,
            width="19%",
            height="30%",
            loc='lower left',
            borderpad=borderpad
        )

        kde = gaussian_kde(values_clean)

        x_vals = np.linspace(
            values_clean.min(),
            values_clean.max(),
            500
        )

        y_vals = kde(x_vals)

        for i in range(len(boundaries)-1):

            inset_ax.fill_between(
                x_vals,
                0,
                y_vals,
                where=(
                    (x_vals >= boundaries[i]) &
                    (x_vals < boundaries[i+1])
                ),
                color=colors[i],
                alpha=1
            )

        inset_ax.tick_params(
            axis='both',
            which='major',
            labelsize=6,
            direction='in',
            length=1,
            width=0.2
        )

        inset_ax.spines['top'].set_visible(False)
        inset_ax.spines['right'].set_visible(False)

        inset_ax.spines['left'].set_linewidth(0)
        inset_ax.spines['bottom'].set_linewidth(0.15)

        inset_ax.yaxis.set_ticks([])
        inset_ax.yaxis.set_ticklabels([])

        inset_ax.set_xlim(inset_xlim)

        inset_ax.set_xticks(inset_xticks)

        for label in inset_ax.get_xticklabels():
            label.set_fontsize(6)
            label.set_fontname('Arial')

        inset_ax.tick_params(
            axis='x',
            which='both',
            labelsize=6,
            labelcolor='black'
        )

        median_val = np.median(values_clean)

        inset_ax.axvline(
            median_val,
            color='black',
            linestyle='--',
            linewidth=0.8,
            alpha=0.8,
            ymin=0.034,
            ymax=0.97
        )

        median_str = (
            f"Median: {round(median_val)}"
            .replace("-", "−")
        )

        inset_ax.text(
            median_val + median_shift,
            np.max(y_vals)*0.8,
            median_str,
            fontsize=6,
            fontname='Arial',
            color='black',
            ha='left',
            va='top'
        )

        return sc
   
    # ======================
    # a
    # ======================

    plot_panel(
        axs[0,0],
        rlls_vm,
        lon,
        lat,
        "./median_colorbar.txt",
        "a",
        r"Median velocity ($\regular{V_m}$, mm/yr)",
        fig,
        ticks=[-10,-8,-6,-4,-2,0,2,4],
        extend='both',
        inset_xlim=[-20,15],
        inset_xticks=[-8,-2,4],
        median_shift=-18.5
    )

    # ======================
    # b
    # ======================

    plot_panel(
        axs[1,0],
        rlls_v5th,
        lon,
        lat,
        "./pth5_colorbar.txt",
        "b",
        r"5th percentile velocity ($\regular{V_{5th}}$, mm/yr)",
        fig,
        ticks=[-135,-105,-75,-45,-15],
        extend='both',
        inset_xlim=[-160,10],
        inset_xticks=[-135,-75,-15],
        median_shift=-95
    )

    # ======================
    # c
    # ======================

    plot_panel(
        axs[2,0],
        rlls_p10,
        lon,
        lat,
        "./p10_colorbar.txt",
        "c",
        r"Proportion of urban lands with a velocity < -10 mm/yr ($\regular{P_{10}}$, %)",
        fig,
        ticks=[0,10,30,50,70,90],
        extend='max',
        inset_xlim=[0,100],
        inset_xticks=[10,30,50],
        median_shift=6,
        cbar_move=0.01,
        ascending=True
    )

    # ======================
    # d
    # ======================

    plot_panel(
        axs[0,1],
        vlm_vm,
        lon,
        lat,
        "./median_colorbar.txt",
        "d",
        r"Median velocity ($\regular{V_m}$, mm/yr)",
        fig,
        ticks=[-10,-8,-6,-4,-2,0,2,4],
        extend='both',
        inset_xlim=[-20,15],
        inset_xticks=[-8,-2,4],
        median_shift=-18.5
    )

    # ======================
    # e
    # ======================

    plot_panel(
        axs[1,1],
        vlm_v5th,
        lon,
        lat,
        "./pth5_colorbar.txt",
        "e",
        r"5th percentile velocity ($\regular{V_{5th}}$, mm/yr)",
        fig,
        ticks=[-135,-105,-75,-45,-15],
        extend='both',
        inset_xlim=[-160,10],
        inset_xticks=[-135,-75,-15],
        median_shift=-95
    )

    # ======================
    # f
    # ======================

    plot_panel(
        axs[2,1],
        vlm_p10,
        lon,
        lat,
        "./p10_colorbar.txt",
        "f",
        r"Proportion of urban lands with a velocity < -10 mm/yr ($\regular{P_{10}}$, %)",
        fig,
        ticks=[0,10,30,50,70,90],
        extend='max',
        inset_xlim=[0,100],
        inset_xticks=[10,30,50],
        median_shift=6,
        cbar_move=0.01,
        ascending=True
    )

    axs[0,0].set_title(
    "InSAR-derived RLLS",
    fontsize=14,
    fontname='Arial',
    pad=12
    )

    axs[0,1].set_title(
        "VLM-aligned land subsidence",
        fontsize=14,
        fontname='Arial',
        pad=12
    )


    
    # plt.savefig(r".\Fig1_plot.tif", dpi=600, format='tif')
    plt.savefig(r".\Fig1_plot.png", dpi=600, format='png')


if __name__ == "__main__":
    main()