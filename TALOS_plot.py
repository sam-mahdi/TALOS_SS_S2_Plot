import matplotlib.pyplot as plt
import re
import numpy as np

def bargraph():
    fig, axs = plt.subplots(2)
    plt.subplots_adjust(wspace=1, hspace=0.001)
    with open('predSS.txt') as file:
        for lines in file:
            search=re.search('^\d+',lines.strip())
            if search != None:
                split_lines=lines.split()
                if split_lines[8] == 'L':
                    axs[0].bar(int(split_lines[0]), 0, color = 'y', width = 0.50)
                elif split_lines[8] == 'H':
                    axs[0].bar(int(split_lines[0]), float(split_lines[4]), color = 'r', width = 0.50)
                elif split_lines[8] == 'E':
                    axs[0].bar(int(split_lines[0]), float(split_lines[5]), color = 'b', width = 0.50)
                else:
                    axs[0].bar(int(split_lines[0]), 0, color = 'g', width = 0.50)
    x = []
    y = []
    with open('predS2.tab') as file:
        for lines in file:
            search = re.search('^\d+', lines.strip())
            if search != None:
                split_lines = lines.split()
                x.append(int(split_lines[0]))
                y.append(float(split_lines[4]))

    axs[1].plot(x, y, c='black',markerfacecolor='lime',markeredgecolor='black',marker='o',linestyle='-',linewidth=1, markersize=5)
    """Paramters"""
    x_ticks=np.arange(1,242,20)
    y_ticks=np.arange(0,1.1,0.5)
    y_ticks2=np.arange(0.5,1.1,0.5)
    plt.xticks(x_ticks)
    axs[0].set_yticks(y_ticks2)
    axs[0].set_ylabel('Predicted Secondary Structure',fontsize=15)
    axs[0].set_yticklabels(y_ticks2, fontsize=15 )
    axs[1].set_xticklabels(x_ticks,fontsize=15)
    axs[1].set_yticks(y_ticks)
    axs[1].set_ylabel('S2',fontsize=15)
    axs[1].set_xlabel('Residue Number',fontsize=15)
    axs[1].set_yticklabels(y_ticks, fontsize=15 )
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
