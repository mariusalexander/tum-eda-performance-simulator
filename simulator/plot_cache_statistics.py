import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import sys

__xtext=0.94
__ytext=0.96

logy  = False
width = 1.0
annotate = False

# annotate maximum hit count
def annote_max(xmax, ymax, text, ax=None):
    global __xtext, __ytext
    if not annotate: return
    
    text=text.format(xmax, ymax) #'idx={hex(xmax)[2:]}, hits={ymax}'
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
            arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(__xtext, __ytext), **kw)
    __ytext -= 0.05

files = sys.argv[1:]
if len(files) == 0: exit()

for file_name in files:
    ### inits
    ax = None
    
    ### read data frame    
    df = pd.read_csv(file_name)
    print(file_name)
    print(df)

    ### prepare x-ticks
    indicies = df['index']
   
    xticks   = np.arange(15, len(indicies), 16)
    if len(xticks) == 0: 
        xticks = np.arange(0, len(indicies), 1)
    xlabels = [str(hex(indicies[i])[2:]) for i in xticks]
            
    ### plot total hits
    data = df['total_hits']
    meanHits = data.mean()
    
    ax = df.plot(kind='bar', x=indicies.name, y=data.name, color='red', logy=logy, ax=ax, width=width)
    ax.set(xticks=xticks, xticklabels=xlabels)
    #ax.fill_between(x=df.index, y1=df.hits, y2=0, where=df.hits > 0, interpolate=True, color='pink')

    # highlight max hits
    xmax = data.idxmax()
    ymax = data[xmax]
    print('max hits:', (xmax, ymax))
    annote_max(xmax, ymax, text='idx={0:X}, hits={1}', ax=ax)

    ### plot evictions
    data = df['evictions']
    meanEvictions = data.mean()
    
    ax = df.plot(kind='bar', x=indicies.name, y=data.name, color='blue', logy=logy, ax=ax, width=width)
    ax.set(xticks=xticks, xticklabels=xlabels)
    
    # highlight max evictions
    xmax = data.idxmax()
    ymax = data[xmax]
    print('max evictions:', (xmax, ymax))    
    annote_max(xmax, ymax, text='idx={0:X}, evictions={1}', ax=ax)

    ### mean line
    print('mean hits:', meanHits)
    print('mean evictions:', meanEvictions)
    plt.plot([0, xticks[-1]], [meanHits, meanHits], color='crimson', label=f'avg {meanHits:.1f} hits' , linestyle='--')
    plt.plot([0, xticks[-1]], [meanEvictions, meanEvictions], color='darkblue', label=f'avg {meanEvictions:.1f} evictions' , linestyle='--')
    
    ### plotting settings
    plt.grid(color='#EEEEEE')
    plt.xlabel("cache block no.")
    plt.ylabel("access count")
    plt.legend(loc='upper left')
    plt.title(file_name)
    
    __ytext=0.96


plt.show()
