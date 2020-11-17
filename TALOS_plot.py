import matplotlib.pyplot as plt
import re
import numpy as np


"""
Modifications to the bar graph for TALOS secondary structure predictions.
You may modify the color and width of the bars themselves.
"""
secondary_strucutre_helix_color='r'
secondary_strucutre_helix_bar_width=0.5
secondary_strucutre_sheet_color='b'
secondary_strucutre_sheet_bar_width=0.5

"""
You may also wish to display unassigned regions as well, or regions that were ambigious in TALOS
"""
secondary_structure_ambigious_bar_values=0
secondary_structure_ambigious_bar_color='y'
secondary_structure_ambigious_bar_width=0.5
secondary_structure_unassigned_peak_values=0
secondary_structure_unassigned_peak_color='g'
secondary_structure_unassigned_peak_bar_width=0.5

"""
Modifications to the dynamics plot graph for RCI
You may modify the lines connecting the dots, the color around the dot, the size of the dots, etc.
You may change the format of the line as well (i.e. '-' is a single line, '--' is dashed)
You may change the shape of the dots as well (i.e. 'o' is circle, 'x' is an x)
"""

dynamics_line_color='black'
dynamics_dot_color='lime'
dynamics_dot_size=5
dynamics_dot_shape='o'
dynamics_dot_color_border='black'
dynamics_line_style='-'
dynamics_line_width=1

"""
Modifications to the x-axis ticks and labels
"""

x_axis_range_start=0
x_axis_range_end=242
x_axis_range_interval=20
x_axis_fontsize=20
x_axis_label='Residue Number'
x_axis_label_fontsize=20

"""
Modifications to the predicted secondary structure y-axis ticks and labels
"""
secondary_structure_y_axis_start=0
secondary_structure_y_axis_end=1.1
secondary_structure_y_axis_interval=0.5
secondary_structure_y_axis_fontsize=20
secondary_structure_y_axis_label='Secondary Structure'
secondary_structure_y_axis_label_fontsize=20

"""
Modifications to the RCI S2 y-axis ticks and labels
"""

dynamics_y_axis_start=0.5
dynamics_y_axis_end=1.1
dynamics_y_axis_interval=0.5
dynamics_y_axis_fontsize=20
dynamics_y_axis_label=f'S\N{SUPERSCRIPT TWO}'



def bargraph():
    fig, axs = plt.subplots(2)
    plt.subplots_adjust(wspace=1, hspace=0.001)
    unassigned=[]
    with open('predSS.txt') as file:
        for lines in file:
            search=re.search('^\d+',lines.strip())
            if search != None:
                split_lines=lines.split()
                if split_lines[8] == 'L':
                    axs[0].bar(int(split_lines[0]), secondary_structure_ambigious_bar_values, color = secondary_structure_ambigious_bar_color, width = secondary_structure_ambigious_bar_width)
                elif split_lines[8] == 'H':
                    axs[0].bar(int(split_lines[0]), float(split_lines[4]), color = secondary_strucutre_helix_color, width = secondary_strucutre_helix_bar_width)
                elif split_lines[8] == 'E':
                    axs[0].bar(int(split_lines[0]), float(split_lines[5]), color = secondary_strucutre_sheet_color, width = secondary_strucutre_sheet_bar_width)
                else:
                    axs[0].bar(int(split_lines[0]), secondary_structure_unassigned_peak_values, color = secondary_structure_unassigned_peak_color, width = secondary_structure_unassigned_peak_bar_width)
                    unassigned.append(int(split_lines[0]))
    x = []
    y = []
    with open('predS2.tab') as file:
        for lines in file:
            search = re.search('^\d+', lines.strip())
            if search != None:
                split_lines = lines.split()
                if int(split_lines[0]) in unassigned:
                    continue
                x.append(int(split_lines[0]))
                y.append(float(split_lines[4]))

    axs[1].plot(x, y, c=dynamics_line_color,markerfacecolor=dynamics_dot_color,markeredgecolor=dynamics_dot_color_border,marker=dynamics_dot_shape,linestyle=dynamics_line_style,linewidth=dynamics_line_width, markersize=dynamics_dot_size)
    x_ticks=np.arange(x_axis_range_start,x_axis_range_end,x_axis_range_interval)
    y_ticks=np.arange(secondary_structure_y_axis_start,secondary_structure_y_axis_end,secondary_structure_y_axis_interval)
    y_ticks2=np.arange(dynamics_y_axis_start,dynamics_y_axis_end,dynamics_y_axis_interval)
    plt.xticks(x_ticks)
    axs[0].set_yticks(y_ticks2)
    axs[0].set_ylabel(secondary_structure_y_axis_label,fontsize=secondary_structure_y_axis_label_fontsize)
    axs[0].set_yticklabels(y_ticks2, fontsize=secondary_structure_y_axis_fontsize )
    axs[1].set_xticklabels(x_ticks,fontsize=x_axis_fontsize)
    axs[1].set_yticks(y_ticks)
    axs[1].set_ylabel(dynamics_y_axis_label,fontsize=dynamics_y_axis_fontsize)
    axs[1].set_xlabel(x_axis_label,fontsize=x_axis_label_fontsize)
    axs[1].set_yticklabels(y_ticks, fontsize=20 )
    plt.show()
bargraph()

def smooth_lines():
    from scipy.interpolate import make_interp_spline, BSpline
    fig, axs = plt.subplots(2)
    plt.subplots_adjust(wspace=0, hspace=0)
    residues=[]
    sheets=[]
    helix=[]
    with open('predSS.txt') as file:
        for lines in file:
            search=re.search('^\d+',lines.strip())
            if search != None:
                split_lines=lines.split()
                if split_lines[8] == 'L':
                    residues.append((int(split_lines[0])))
                    sheets.append(0)
                    helix.append(0)
                elif split_lines[8] == 'H':
                    residues.append((int(split_lines[0])))
                    helix.append((-1*float(split_lines[4])))
                    sheets.append(float(split_lines[5]))
                elif split_lines[8] == 'E':
                    residues.append((int(split_lines[0])))
                    sheets.append(float(split_lines[5]))
                    helix.append((-1*float(split_lines[4])))
                else:
                    residues.append((int(split_lines[0])))
                    sheets.append(0)
                    helix.append(0)

    smooth_x=np.linspace(min(np.array(residues)),max(np.array(residues)),900)
    smooth_y=make_interp_spline(np.array(residues), np.array(sheets), k=3)
    smooth_y2=make_interp_spline(np.array(residues), np.array(helix), k=3)
    smooth_function_y1=smooth_y(smooth_x)
    smooth_function_y2=smooth_y2(smooth_x)
    smooth_function_y1[smooth_function_y1<0]=0
    smooth_function_y2[smooth_function_y2>0]=0
    axs[0].plot(smooth_x,smooth_function_y1)
    axs[0].plot(smooth_x,smooth_function_y2)
    axs[0].set_ylabel('Probability Sheet    Probability Helix')
    y_ticks=np.arange(-1,1.1,1)
    axs[0].set_yticks(y_ticks)
    x = []
    y = []
    with open('predS2.tab') as file:
        for lines in file:
            search = re.search('^\d+', lines.strip())
            if search != None:
                split_lines = lines.split()
                x.append(int(split_lines[0]))
                y.append(float(split_lines[4]))
    #Uncomment this to get same S2 plot as in bargraph
    #axs[1].plot(x, y, c='black',markerfacecolor='lime',markeredgecolor='black',marker='o',linestyle='-',linewidth=1, markersize=5)
    smooth_x1=np.linspace(min(np.array(x)),max(np.array(x)),300)
    smooth_y1=make_interp_spline(np.array(x), np.array(y), k=3)
    axs[1].plot(smooth_x1, smooth_y1(smooth_x1), c='blue',linestyle='-')
    x_ticks=np.arange(1,242,10)
    plt.xticks(x_ticks)
    axs[1].set_yticks(np.arange(0,1.1,0.5))
    axs[1].set_ylabel('S2')
    axs[1].set_xlabel('Residue Number')
    plt.show()
smooth_lines()
