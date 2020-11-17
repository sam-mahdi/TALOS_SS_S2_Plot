# TALOS_SS_S2_Plot
Script plots both TALOS SS and S2 using bar and line graphs

***TALOS RCI appears to also add values even for unassigned peaks, bargraph script has been modified so it does not plot the RCI values for these residues***

Exporting Talos plots doesn't always work, and replotting the values using excel can have limitations. This script generates 2 plots. A bar graph with the same colors at TALOS, and the option to even color unassigned peaks or amibous picks. And a line graph where probabilities for sheets and helices are plotted inversly of one another. There is also a smoothening function added for aesthetic purposes. 

The S2 values in one function as dots connected by lines, and in another a smooth continous line. 

Every parameter may be modified (labels, font size for axis labels, colors, etc.). 
