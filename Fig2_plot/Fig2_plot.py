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
from matplotlib.patches import Rectangle


plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "bold" 
shp_folder = r"..\Regional_boundary"

color_list = ['#f2bcb5bf', '#b2d67cbf', '#d6e9b9bf', '#c2d1ecbf', '#cce4cabf',
             '#c0e8fbbf', '#f3d3e4bf', '#e7edaebf', '#efc7c7bf', '#f9f0c1bf']

shp_files = sorted(glob.glob(os.path.join(shp_folder, "*.shp")))

position = np.array([
    [5, 12],
    [29.8, 114.3],
    [48, 10],
    [40.5, -101.9],
    [-29, 133.3],
    [60, 75.3],
    [-19.6, -57.4],
    [15, 77.6],
    [-0.9, 113.7],
    [35.2, 51.0]
])


xls_path = r".\Fig2_data.xlsx"
data = pd.read_excel(xls_path, sheet_name="Region")


per_1 = data.Level_1
per_2 = data.Level_2
per_3 = data.Level_3
per_4 = data.Level_4

global_count = np.array([
    per_1.iloc[11],
    per_2.iloc[11],
    per_3.iloc[11],
    per_4.iloc[11]
])
global_count_position = np.array([-175, 5])
bar_colors = ['#4B74B2', '#90BEE0', '#FDE293', '#DB3124']


age_1 = data.Age_1
age_2 = data.Age_2
age_3 = data.Age_3
age_4 = data.Age_4

global_age = np.array([
    age_1.iloc[11],
    age_2.iloc[11],
    age_3.iloc[11],
    age_4.iloc[11]
])
global_age_position = np.array([-175, -40])
age_bar_colors = ['#018571', '#A7DAD2', '#E6D3A5', '#A6611A']


fig = plt.figure(figsize=(15, 10))
ax = fig.add_axes([0.015, 0.2, 0.98, 0.85], projection=ccrs.PlateCarree())


for i, shp_path in enumerate(shp_files):
    gdf = gpd.read_file(shp_path)
    color = color_list[i % len(color_list)]
    gdf.plot(ax=ax, facecolor=color, edgecolor=None, 
             transform=ccrs.PlateCarree())

for spine in ax.spines.values():
    spine.set_visible(False)      




for idx, (lat, lon) in enumerate(position):
    vals_ori = np.array([per_1.iloc[idx], per_2.iloc[idx], per_3.iloc[idx], per_4.iloc[idx]])
    vals_ori[0] = vals_ori[0] - 0.25 
    vals = vals_ori / vals_ori.sum()  

    age_ori = np.array([age_1.iloc[idx], age_2.iloc[idx], age_3.iloc[idx], age_4.iloc[idx]])
    age_ori[0] = age_ori[0] - 0.25
    age = age_ori / age_ori.sum()

    ax_inset = ax.inset_axes([lon, lat, 15, 15.0], transform=ax.transData)

    ax_inset.set_xticks([])
    ax_inset.set_facecolor("none")
    for spine in ax_inset.spines.values():
        spine.set_visible(False)

    bottom_val = 0
    for j, v in enumerate(vals):
        ax_inset.bar(0, v, bottom=bottom_val, color=bar_colors[j], width=5, edgecolor=None)
        bottom_val += v

    bottom_val = 0
    for j, v in enumerate(age):
        ax_inset.bar(6, v, bottom=bottom_val, color=age_bar_colors[j], width=5, edgecolor=None)
        bottom_val += v

    yticks_ori = np.array([0.25, 0.50, 0.75, 1.0])
    yticks = (yticks_ori - 0.25) / (1 - 0.25)
    ax_inset.set_yticks(yticks)
    ax_inset.set_yticklabels([f"{int(v*100)}%" for v in yticks_ori])
    ax_inset.set_ylim(yticks.min(), yticks.max())
    ax_inset.tick_params(axis='y', labelsize=14, labelcolor="#253A59")

    ax_inset.spines['left'].set_position(('data', -5))
    ax_inset.spines['left'].set_visible(True)
    ax_inset.spines['left'].set_color('#5F5F5F')
    ax_inset.spines['left'].set_linewidth(1.5)
    ax_inset.yaxis.set_tick_params(direction='in', length=3, width=1.5, color='#5F5F5F', labelcolor="#253A59")



ax_inset = ax.inset_axes([global_count_position[0], global_count_position[1], 70, 40], transform=ax.transData)
ax_inset.set_facecolor("none")

x = np.arange(len(global_count))
bars = ax_inset.bar(x, global_count, color=bar_colors, width=0.8, edgecolor=None)

for i, v in enumerate(global_count):
    ax_inset.text(i, v + 0.02, f"{v*100:.1f}%", ha='center', va='bottom', 
                  fontsize=14, color="#41669D", fontweight="bold")

ax_inset.set_ylim(0, 1) 
ax_inset.set_xticks([])
ax_inset.set_yticks([])
ax_inset.spines['left'].set_visible(False)
ax_inset.spines['top'].set_visible(False)
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['bottom'].set_visible(False)



ax_inset = ax.inset_axes([global_age_position[0], global_age_position[1], 70, 40], transform=ax.transData)
ax_inset.set_facecolor("none")

x = np.arange(len(global_age))
bars = ax_inset.bar(x, -global_age, color=age_bar_colors, width=0.8)

for i, v in enumerate(global_age):
    ax_inset.text(i, -(v + 0.02), f"{v*100:.1f}%", ha='center', va='top', 
                  fontsize=14, color="#41669D", fontweight="bold")

ax_inset.set_ylim(-1, 0) 
ax_inset.set_xticks([])
ax_inset.set_yticks([])
ax_inset.spines['left'].set_visible(False)
ax_inset.spines['top'].set_visible(False)
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['bottom'].set_visible(False)


bar_labels = ["Level IV (< -40) mm/yr", "Level III [-40, -20]", "Level II  [-20, -10]", "Level I   [-10,    0]"]
bar_patches = [mpatches.Patch(color=c, label=lab) for c, lab in zip(bar_colors[::-1], bar_labels)]


age_labels = ["75 + years ", "[50, 75]", "[25, 50]", "[0,   25]"]
age_patches = [mpatches.Patch(color=c, label=lab) for c, lab in zip(age_bar_colors[::-1], age_labels)]


region_labels = [
    "Africa", "East Asia", "Europe", "North America", "Oceania",
    "Russia", "South America", "South Asia", "Southeast Asia", "West-Central Asia"
]
region_patches = [mpatches.Patch(color=c, label=lab) for c, lab in zip(color_list, region_labels)]


legend1 = fig.legend(
    handles=bar_patches,
    title="  Proportion of population \n exposed to subsidence of:",
    loc="lower center",
    bbox_to_anchor=(0.16, 0.0), 
    ncol=1,
    frameon=False,
    fontsize=14,
    title_fontsize=16,
    handlelength=3,   
    handleheight=2,
    labelspacing=1,
    prop={'size':14,'weight':'bold'},
)
title_1 = legend1.get_title()
title_1.set_color("#253A59")  
title_1.set_fontweight("bold")    

for text in legend1.get_texts():
    text.set_fontsize(14)       
    text.set_color("#253A59") 

legend2 = fig.legend(
    handles=age_patches,
    title="Age-group-specific population\n      exposure to subsidence: ",
    loc="lower center",
    bbox_to_anchor=(0.41, 0.0),
    ncol=1,
    frameon=False,
    fontsize=14,
    title_fontsize=16,
    handlelength=3,   
    handleheight=2,
    labelspacing=1,
    prop={'size':14,'weight':'bold'},
) 
title_2 = legend2.get_title()
title_2.set_color("#253A59")  
title_2.set_fontweight("bold")    

for text in legend2.get_texts():
    text.set_fontsize(14)       
    text.set_color("#253A59")   

region_patches1 = region_patches[:5]  
region_patches2 = region_patches[5:]  


legend3a = fig.legend(
    handles=region_patches1,
    title="Region: ",
    loc="lower center",
    bbox_to_anchor=(0.68, 0.0),  
    ncol=1, 
    frameon=False,
    fontsize=14,
    title_fontsize=16,
    handlelength=3,
    handleheight=2,
    labelspacing=0.8,
    prop={'size':14,'weight':'bold'},
)
 

legend3a._legend_box.align = "left" 
title_3b = legend3a.get_title()
title_3b.set_color("#253A59")
title_3b.set_fontweight("bold")

for text in legend3a.get_texts():
    text.set_fontsize(14)       
    text.set_color("#253A59")  

legend3b = fig.legend(
    handles=region_patches2,
    loc="lower center",
    bbox_to_anchor=(0.87, 0.0),  
    ncol=1, 
    frameon=False,
    fontsize=14,
    handlelength=3,
    handleheight=2,
    labelspacing=0.8,
    prop={'size':14,'weight':'bold'},
)

for text in legend3b.get_texts():
    text.set_fontsize(14)      
    text.set_color("#253A59")   

fig.add_artist(legend1)
fig.add_artist(legend2)
fig.add_artist(legend3a)
fig.add_artist(legend3b)


all_legends = [legend1, legend2, legend3a, legend3b]


fig_width, fig_height = fig.get_size_inches()
fig_dpi = fig.dpi


border_rect = Rectangle(
    (0.02, 0.01),  
    0.96,           
    0.27,         
    linewidth=1.5,
    edgecolor="#808080",
    facecolor="none",
    linestyle="--",
    transform=fig.transFigure,  
    zorder=10
)
fig.patches.append(border_rect)


x_line = 0.56  
y_start = 0.01  
y_end = 0.28    

fig.lines.append(
    plt.Line2D(
        [x_line, x_line],
        [y_start, y_end],
        color="#808080",
        linestyle="--",
        linewidth=1.5,
        transform=fig.transFigure,
        zorder=11
    )
)



plt.savefig(r".\Fig2_plot.tif", dpi=600, format='tif')


