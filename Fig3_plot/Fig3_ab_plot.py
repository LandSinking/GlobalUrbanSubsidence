import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import glob
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar


plt.rcParams["font.family"] = "Arial"


shp_folder = r"..\Regional_boundary"
color_list_red = ['#f4ecee', '#ddc2c9', '#c698a3', '#ae6d7e', '#974358']
color_list_blue = ['#dde4ed', '#bac9da', '#97adc8', '#7492b5', '#5176a2']


# Africa, East Asia, Europe, North America, Oceania, Russia, South America, South Asia, Southeast Asia, West-Central Asia
shp_files = sorted(glob.glob(os.path.join(shp_folder, "*.shp")))

xls_path = r".\Fig3_data.xlsx"
data = pd.read_excel(xls_path, sheet_name="Region")


position = np.array([
    [12, 3],        
    [29, 115.6],   
    [49, 2],       
    [43.5, -110],  
    [-27, 122],    
    [60, 75.3],      
    [-11, -68], 
    [25, 66],     
    [3.6, 113.6],   
    [33, 38]     
])

####
dece_ratio = data.Deceleration_ratio.iloc[:10]
acce_ratio = data.Acceleration_ratio.iloc[:10]

dece_magn_Q1 = data.Deceleration_Q1.iloc[:10]
dece_magn_median = data.Deceleration_median.iloc[:10]
dece_magn_Q3 = data.Deceleration_Q3.iloc[:10]

acce_magn_Q1 = data.Acceleration_Q1.iloc[:10]
acce_magn_median = data.Acceleration_median.iloc[:10]
acce_magn_Q3 = data.Acceleration_Q3.iloc[:10]

dece_weighted_data_Q1 = dece_ratio * dece_magn_Q1
dece_weighted_data_median = dece_ratio * dece_magn_median
dece_weighted_data_Q3 = dece_ratio * dece_magn_Q3

acce_weighted_data_Q1 = acce_ratio * acce_magn_Q1
acce_weighted_data_median = acce_ratio * acce_magn_median
acce_weighted_data_Q3 = acce_ratio * acce_magn_Q3



dece_weighted_data = dece_weighted_data_median
acce_weighted_data = acce_weighted_data_median

dece_weighted_data_1 = dece_weighted_data.round(1)
acce_weighted_data_1 = acce_weighted_data.round(1)



abs_dece = dece_weighted_data_1.abs()
dece_class = pd.cut(
    abs_dece,
    bins=5,
    labels=[1, 2, 3, 4, 5],
    include_lowest=True
).astype(int)


abs_acce = acce_weighted_data_1.abs()
acce_class = pd.cut(
    abs_acce,
    bins=5,
    labels=[1, 2, 3, 4, 5],
    include_lowest=True
).astype(int)


result = pd.DataFrame({
    "dece_original": dece_weighted_data_1,
    "dece_abs": abs_dece,
    "dece_class": dece_class,
    "acce_original": acce_weighted_data_1,
    "acce_abs": abs_acce,
    "acce_class": acce_class
})

# print(result)



fig, axes = plt.subplots(2, 1, figsize=(12, 10), subplot_kw={'projection': ccrs.PlateCarree()})

plt.subplots_adjust(hspace=-0.16)  


fig.subplots_adjust(
    left=0.02,    
    right=0.98,   
    top=0.9,    
    bottom=0.1 
)




for ax in axes:
    for spine in ax.spines.values():
        spine.set_visible(False)




configs = [
    ("dece_class", color_list_blue, "Deceleration Weighted Class", result["dece_abs"], 'black'), 
    ("acce_class", color_list_red, "Acceleration Weighted Class", result["acce_abs"], 'black')   
]


for ax, (class_col, color_list, title, abs_values, text_color) in zip(axes, configs):
    ax.set_global()

    for i, shp_file in enumerate(shp_files):
        gdf = gpd.read_file(shp_file)

        class_id = result.loc[i, class_col]  
        facecolor = color_list[class_id - 1]  

        gdf.plot(
            ax=ax,
            facecolor=facecolor,
            edgecolor="none",
            transform=ccrs.PlateCarree(),
            zorder=2
        )




    if class_col == "dece_class":
        Q1_list = dece_weighted_data_Q1
        Q3_list = dece_weighted_data_Q3
    else:
        Q1_list = acce_weighted_data_Q1
        Q3_list = acce_weighted_data_Q3


    for idx, ((lat, lon), value) in enumerate(zip(position, abs_values)):
        

        ax.text(
            lon, lat, f"{value:.1f}",
            transform=ccrs.PlateCarree(),
            fontsize=10,                   
            fontweight='bold',
            style='italic',
            ha='center', va='center',
            color=text_color,
            zorder=10
        )

 
        q1_raw = abs(Q1_list.iloc[idx])
        q3_raw = abs(Q3_list.iloc[idx])

        Q_low, Q_high = sorted([q1_raw, q3_raw])  


        ax.text(
            lon + 17, lat+2 ,
            f"[{Q_low:.1f}, {Q_high:.1f}]",
            transform=ccrs.PlateCarree(),
            fontsize=8,
            fontweight='bold',
            style='italic',
            ha='center', va='top',
            color="#404040", 
            zorder=10
        )

    

    axins = inset_axes(ax,
                   width=0.18,  
                   height=1.0,  
                   loc='lower left',
                   bbox_to_anchor=(0.08, 0.3, 1, 1), 
                   bbox_transform=ax.transAxes,
                   borderpad=0)
    
  


    cmap = mcolors.ListedColormap(color_list[::-1]) 
    bounds = np.arange(1, 7)  
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
   

   
    cb = mcolorbar.ColorbarBase(axins, cmap=cmap, norm=norm,
                                orientation='vertical',
                                ticks=np.arange(1.5, 6.5),  
                                spacing='uniform')
    cb.ax.invert_yaxis() 

    axins.yaxis.set_ticks_position('right')

    axins.tick_params(
        which='both',     
        length=0,       
        left=False,       
        right=False       
    )
  

    axins.set_frame_on(False)
    axins.axis('off') 



plt.savefig(r".\Fig3_ab.png", dpi=600, format='png')

# plt.show()